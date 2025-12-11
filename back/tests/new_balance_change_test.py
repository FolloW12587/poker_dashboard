from datetime import datetime
import pytest
import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.usecase.errors import InvalidInputError
from domain.entity.account import Account

from app.usecase.balance_change import BalanceChangeUseCase
from app.dto.balance_change import NewBalanceChangeRequest, BalanceChangeState
from infra.db.account import AccountRepository
from infra.db.balance_change import BalanceChangeRepository


async def clean_tables(db_session: AsyncSession):
    await db_session.execute(delete(Account))
    await db_session.commit()


@pytest_asyncio.fixture
async def account() -> Account:
    return Account(name="account", balance=100, last_balance_update=datetime.now())


@pytest_asyncio.fixture
async def ready_db_session(db_session: AsyncSession, account: Account):
    """Фикстура для очистки базы данных перед каждым тестом."""
    await clean_tables(db_session)
    db_session.add(account)
    await db_session.commit()
    await db_session.refresh(account)

    return db_session, account


def get_usecase(session: AsyncSession) -> BalanceChangeUseCase:
    account_repo = AccountRepository(session)
    balance_change_repo = BalanceChangeRepository(session)

    return BalanceChangeUseCase(account_repo, balance_change_repo)


@pytest.mark.asyncio
async def test_balance_change_update(ready_db_session: tuple[AsyncSession, Account]):
    session, account = ready_db_session

    usecase = get_usecase(session)
    # account gained
    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.UPDATE, balance=200
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 100
    assert output.state == BalanceChangeState.UPDATE

    await session.refresh(account)
    assert not account.is_balance_fixed
    assert account.balance == dto.balance

    # account lost
    dto.balance = 50
    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == -150
    assert output.state == BalanceChangeState.UPDATE

    await session.refresh(account)
    assert not account.is_balance_fixed
    assert account.balance == dto.balance

    # account didn't gane or lose
    output = await usecase.new_balance_update(dto)

    assert output.balance_diff == 0
    assert output.state == BalanceChangeState.UPDATE
    await session.refresh(account)
    assert not account.is_balance_fixed
    assert account.balance == dto.balance
    assert account.is_active


@pytest.mark.asyncio
async def test_balance_change_update_fixed_dep(
    ready_db_session: tuple[AsyncSession, Account],
):
    session, account = ready_db_session

    usecase = get_usecase(session)
    account.is_balance_fixed = True
    account = await usecase.account_repository.update(account)

    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.UPDATE, balance=200
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 100
    assert output.state == BalanceChangeState.DEPOSIT

    await session.refresh(account)
    assert not account.is_balance_fixed
    assert account.is_active


@pytest.mark.asyncio
async def test_balance_change_update_fixed_same_balance(
    ready_db_session: tuple[AsyncSession, Account],
):
    session, account = ready_db_session

    usecase = get_usecase(session)
    # Аккуант активный
    account.is_balance_fixed = True
    account = await usecase.account_repository.update(account)

    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.UPDATE, balance=100
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 0
    assert output.state == BalanceChangeState.UPDATE

    await session.refresh(account)
    # при активном аккаунте фикс должен остаться
    assert account.is_balance_fixed
    assert account.is_active

    account.is_active = False
    account = await usecase.account_repository.update(account)

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 0
    assert output.state == BalanceChangeState.UPDATE

    await session.refresh(account)
    # при неактивном аккаунте фикс должен сняться
    assert not account.is_balance_fixed
    assert account.is_active


@pytest.mark.asyncio
async def test_balance_change_update_fixed_withdraw(
    ready_db_session: tuple[AsyncSession, Account],
):
    session, account = ready_db_session

    usecase = get_usecase(session)
    account.is_balance_fixed = True
    account = await usecase.account_repository.update(account)

    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.UPDATE, balance=50
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == -50
    assert output.state == BalanceChangeState.WITHDRAW

    await session.refresh(account)
    assert not account.is_balance_fixed
    assert account.is_active


@pytest.mark.asyncio
async def test_balance_change_invalid_state(
    ready_db_session: tuple[AsyncSession, Account],
):
    session, account = ready_db_session

    usecase = get_usecase(session)

    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.DEPOSIT, balance=200
    )

    with pytest.raises(InvalidInputError):
        await usecase.new_balance_update(dto)

    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.WITHDRAW, balance=250
    )

    with pytest.raises(InvalidInputError):
        await usecase.new_balance_update(dto)

    await session.refresh(account)
    assert account.balance == 100
    assert not account.is_balance_fixed
    assert account.is_active


@pytest.mark.asyncio
async def test_balance_change_lock(ready_db_session: tuple[AsyncSession, Account]):
    session, account = ready_db_session

    usecase = get_usecase(session)
    # account gained
    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.LOCK, balance=200
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 100
    assert output.state == BalanceChangeState.LOCK

    await session.refresh(account)
    assert account.is_balance_fixed
    assert account.balance == dto.balance
    assert account.is_active


@pytest.mark.asyncio
async def test_balance_change_lock_fixed(
    ready_db_session: tuple[AsyncSession, Account],
):
    session, account = ready_db_session

    usecase = get_usecase(session)
    # активный аккаунт
    account.is_balance_fixed = True
    account = await usecase.account_repository.update(account)
    # account gained
    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.LOCK, balance=200
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 100
    assert output.state == BalanceChangeState.DEPOSIT

    await session.refresh(account)
    assert account.is_balance_fixed
    assert account.balance == dto.balance
    assert account.is_active

    # неактивный аккаунт
    account.balance = 100
    account.is_active = False
    account = await usecase.account_repository.update(account)

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 100
    assert output.state == BalanceChangeState.DEPOSIT

    await session.refresh(account)
    assert account.is_balance_fixed
    assert account.balance == dto.balance
    assert account.is_active


@pytest.mark.asyncio
async def test_balance_change_lock_fixed_same_balance(
    ready_db_session: tuple[AsyncSession, Account],
):
    session, account = ready_db_session

    # активный аккаунт
    usecase = get_usecase(session)
    account.is_balance_fixed = True
    account = await usecase.account_repository.update(account)

    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.LOCK, balance=100
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 0
    assert output.state == BalanceChangeState.LOCK

    await session.refresh(account)
    assert account.is_balance_fixed
    assert account.is_active

    # неактивный аккаунт
    usecase = get_usecase(session)
    account.is_active = False
    account = await usecase.account_repository.update(account)

    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.LOCK, balance=100
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 0
    assert output.state == BalanceChangeState.LOCK

    await session.refresh(account)
    assert account.is_balance_fixed
    assert account.is_active


@pytest.mark.asyncio
async def test_balance_change_shutdown(ready_db_session: tuple[AsyncSession, Account]):
    session, account = ready_db_session

    usecase = get_usecase(session)
    # account gained
    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.SHUTDOWN, balance=200
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 100
    assert output.state == BalanceChangeState.SHUTDOWN

    await session.refresh(account)
    assert account.is_balance_fixed
    assert account.balance == dto.balance
    assert not account.is_active


@pytest.mark.asyncio
async def test_balance_change_shutdown_fixed(
    ready_db_session: tuple[AsyncSession, Account],
):
    session, account = ready_db_session

    usecase = get_usecase(session)
    # активный аккаунт
    account.is_balance_fixed = True
    account = await usecase.account_repository.update(account)
    # account gained
    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.SHUTDOWN, balance=200
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 100
    assert output.state == BalanceChangeState.DEPOSIT

    await session.refresh(account)
    assert account.is_balance_fixed
    assert account.balance == dto.balance
    assert not account.is_active

    # неактивный аккаунт
    account.balance = 100
    account.is_active = False
    account = await usecase.account_repository.update(account)

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 100
    assert output.state == BalanceChangeState.DEPOSIT

    await session.refresh(account)
    assert account.is_balance_fixed
    assert account.balance == dto.balance
    assert not account.is_active


@pytest.mark.asyncio
async def test_balance_change_shutdown_fixed_same_balance(
    ready_db_session: tuple[AsyncSession, Account],
):
    session, account = ready_db_session

    # активный аккаунт
    usecase = get_usecase(session)
    account.is_balance_fixed = True
    account = await usecase.account_repository.update(account)

    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.SHUTDOWN, balance=100
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 0
    assert output.state == BalanceChangeState.SHUTDOWN

    await session.refresh(account)
    assert account.is_balance_fixed
    assert not account.is_active

    # неактивный аккаунт
    usecase = get_usecase(session)
    account.is_active = False
    account = await usecase.account_repository.update(account)

    dto = NewBalanceChangeRequest(
        account_name=account.name, state=BalanceChangeState.SHUTDOWN, balance=100
    )

    output = await usecase.new_balance_update(dto)
    assert output.balance_diff == 0
    assert output.state == BalanceChangeState.SHUTDOWN

    await session.refresh(account)
    assert account.is_balance_fixed
    assert not account.is_active
