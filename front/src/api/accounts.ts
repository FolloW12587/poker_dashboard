import { apiRequest } from "./http";

export interface Account {
  id: string;
  name: string;
  current_balance: number;
  last_balance_update: string; // ISO string
}

export interface BalanceChange {
  id: string;
  created_at: string; // ISO string
  account_id: string;
  state: "money_request" | "money_received" | "money_withdraw" | "update";
  balance: number;
  balance_diff: number;
}

// Получить список аккаунтов
export function getAccounts(): Promise<Account[]> {
  return apiRequest<Account[]>("/accounts", { method: "GET" });
}

// Получить изменения баланса для конкретного аккаунта
export function getBalanceChanges(accountId: string): Promise<BalanceChange[]> {
  return apiRequest<BalanceChange[]>(`/balance_change/${accountId}`, {
    method: "GET",
  });
}
