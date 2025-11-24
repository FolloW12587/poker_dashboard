import { create } from "zustand";

interface AuthStore {
  token: string | null;
  setToken: (t: string | null) => void;
}

export const useAuth = create<AuthStore>((set) => ({
  token: null,
  setToken: (token) => set({ token }),
}));
