import { useEffect, useState } from "react";
import { useAuth } from "./store/auth";

export function AppInitializer({ children }: { children: React.ReactNode }) {
  const setToken = useAuth((s) => s.setToken);
  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("token");
    if (saved) {
      setToken(saved);
    }
    setInitialized(true);
  }, [setToken]);

  if (!initialized) return null; // пока не загружен токен, ничего не рендерим

  return <>{children}</>;
}
