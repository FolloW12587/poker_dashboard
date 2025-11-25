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
