import { useEffect, useState } from "react";
import { getAccounts, type Account } from "../api/accounts";
import { useNavigate } from "react-router-dom";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { FiChevronRight } from "react-icons/fi";
import "./Dashboard.css"; // Для анимации fade-in

dayjs.extend(relativeTime);

export default function Dashboard() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchAccounts() {
      try {
        const data = await getAccounts();
        setAccounts(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchAccounts();
  }, []);

  const filteredAccounts = accounts.filter((acc) =>
    acc.name.toLowerCase().includes(search.toLowerCase())
  );

  const handleClick = (id: string) => {
    navigate(`/accounts/${id}`);
  };

  if (loading) return <p style={{ textAlign: "center" }}>Загрузка...</p>;
  if (error)
    return <p style={{ color: "red", textAlign: "center" }}>{error}</p>;

  return (
    <div style={styles.wrapper}>
      <input
        type="text"
        placeholder="Поиск аккаунта"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={styles.search}
      />

      <div style={styles.list}>
        {filteredAccounts.map((acc) => {
          const dateStr = acc.last_balance_update.replace(/\.\d+Z$/, "Z");
          const date = new Date(dateStr);

          const timeSince = isNaN(date.getTime())
            ? "неизвестно"
            : dayjs(date).fromNow(); // Используем dayjs для красивого формата

          return (
            <div
              key={acc.id}
              className="card fade-in"
              onClick={() => handleClick(acc.id)}
            >
              <div style={styles.left}>{acc.name}</div>
              <div style={styles.right}>
                <div style={styles.balanceWrapper}>
                  <div style={styles.balance}>{acc.current_balance}</div>
                  <div style={styles.lastUpdate}>{timeSince}</div>
                </div>
                <FiChevronRight style={styles.icon} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    maxWidth: 800,
    margin: "40px auto",
    padding: "0 20px",
  } as React.CSSProperties,

  search: {
    width: "calc(100% - 26px)",
    padding: 12,
    marginBottom: 20,
    borderRadius: 8,
    border: "1px solid #444",
    backgroundColor: "#1e1e1e",
    color: "#f0f0f0",
    fontSize: 16,
  } as React.CSSProperties,

  list: {
    display: "flex",
    flexDirection: "column",
    gap: 12,
  } as React.CSSProperties,

  left: {
    fontWeight: 500,
    fontSize: 16,
  } as React.CSSProperties,

  right: {
    textAlign: "right",
    display: "flex",
    alignItems: "center",
  } as React.CSSProperties,

  balanceWrapper: {
    marginRight: 24,
  } as React.CSSProperties,

  balance: {
    fontWeight: "bold",
    fontSize: 18,
  } as React.CSSProperties,

  lastUpdate: {
    fontSize: 12,
    color: "#aaa",
  } as React.CSSProperties,

  icon: {
    fontSize: 20,
    color: "#aaa",
  } as React.CSSProperties,
};
