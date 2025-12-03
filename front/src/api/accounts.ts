import { apiRequest } from "./http";

export interface Account {
  id: string;
  name: string;
  current_balance: number;
  last_balance_update: string; // ISO string
}

export const BalanceChangeState = {
  MONEY_REQUEST: "money_request",
  MONEY_RECEIVED: "money_received",
  MONEY_WITHDRAW: "money_withdraw",
  UPDATE: "update",
} as const;

export type BalanceChangeState =
  (typeof BalanceChangeState)[keyof typeof BalanceChangeState];

export interface BalanceChange {
  id: string;
  created_at: string; // ISO string
  account_id: string;
  state: BalanceChangeState;
  balance: number;
  balance_diff: number;
}

export const BalanceChangeStateMapping: Record<BalanceChangeState, string> = {
  money_request: "Запрос пополнения баланса",
  money_received: "Пополнение баланса",
  money_withdraw: "Вывод средств",
  update: "Обновление баланса",
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
