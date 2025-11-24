import { apiRequest } from "./http";

export interface Token {
  access_token: string;
  token_type: string; // всегда "bearer"
}

export interface LoginPayload {
  username: string;
  password: string;
}

export function login(data: LoginPayload): Promise<Token> {
  return apiRequest<Token>("/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function register(data: LoginPayload): Promise<Token> {
  return apiRequest<Token>("/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
