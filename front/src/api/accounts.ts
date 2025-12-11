import { apiRequest } from "./http";

export interface Account {
  id: string;
  name: string;
  balance: number;
  is_active: boolean;
  last_balance_update: string; // ISO string
}

export const BalanceChangeState = {
  LOCK: "lock",
  DEPOSIT: "deposit",
  WITHDRAW: "withdraw",
  UPDATE: "update",
  SHUTDOWN: "shutdown",
} as const;

export type BalanceChangeState =
  (typeof BalanceChangeState)[keyof typeof BalanceChangeState];

export interface BalanceChange {
  id: string;
  created_at: string; // ISO string
  account_id: string;
  state: BalanceChangeState;
  state_raw: BalanceChangeState;
  balance: number;
  balance_diff: number;
}

export const BalanceChangeStateMapping: Record<BalanceChangeState, string> = {
  lock: "Блокировка баланса до следующего изменения",
  deposit: "Пополнение баланса",
  withdraw: "Вывод средств",
  update: "Обновление баланса",
  shutdown: "Выключение и обновление баланса",
};

// Получить список аккаунтов
export function getAccounts(): Promise<Account[]> {
  return apiRequest<Account[]>("/accounts", { method: "GET" });
}

export function getBalanceChanges(
  accountId: string,
  dateFrom: string,
  dateTo: string
): Promise<BalanceChange[]> {
  return apiRequest<BalanceChange[]>(
    `/balance_change/${accountId}?date_from=${encodeURIComponent(
      dateFrom
    )}&date_to=${encodeURIComponent(dateTo)}`,
    {
      method: "GET",
    }
  );
}
