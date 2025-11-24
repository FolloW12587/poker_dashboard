import { useAuth } from "../store/auth";
import { useEffect, useState } from "react";
import { login } from "../api/auth";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const setToken = useAuth((s) => s.setToken);
  const token = useAuth((s) => s.token);

  const navigate = useNavigate();

  // Если пользователь уже залогинен, сразу редиректим
  useEffect(() => {
    if (token) {
      navigate("/dashboard");
    }
  }, [token, navigate]);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await login({ username, password });
      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);

      // console.log("Успешный логин:", data);

      navigate("/dashboard"); // редирект после логина
    } catch (err: any) {
      setError(err.message || "Ошибка авторизации");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleLogin} style={styles.form}>
      <h2>Вход</h2>

      {error && <p style={styles.error}>{error}</p>}

      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={styles.input}
      />

      <input
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={styles.input}
      />

      <button type="submit" disabled={loading} style={styles.button}>
        {loading ? "Входим..." : "Войти"}
      </button>
    </form>
  );
}

const styles = {
  form: {
    maxWidth: 300,
    margin: "80px auto",
    display: "flex",
    flexDirection: "column",
    gap: 12,
  } as React.CSSProperties,
  input: {
    padding: 10,
    fontSize: 16,
  } as React.CSSProperties,
  button: {
    padding: 10,
    fontSize: 16,
    cursor: "pointer",
  } as React.CSSProperties,
  error: {
    color: "red",
  } as React.CSSProperties,
};
