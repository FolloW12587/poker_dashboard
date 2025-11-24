import type { JSX } from "react";
import { useAuth } from "../store/auth";
import { Navigate } from "react-router-dom";

export function PrivateRoute({ children }: { children: JSX.Element }) {
  const token = useAuth((s) => s.token);

  // Пока token === null → показываем загрузку (или null)
  // Если token === undefined → тоже можно показывать загрузку
  if (token === null) return <p>Загрузка...</p>;

  if (!token) return <Navigate to="/login" />;

  return children;
}
