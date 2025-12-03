import { useEffect, useState } from "react";
import { getAccounts, type Account } from "../../api/accounts";
import "./Dashboard.css"; // Для анимации fade-in
import Card from "./Card";
import AccountPage from "../account/Account";

export default function Dashboard() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [accountSelected, setAccountSelected] = useState<Account | null>(null);

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

  if (loading) return <p style={{ textAlign: "center" }}>Загрузка...</p>;
  if (error)
    return <p style={{ color: "red", textAlign: "center" }}>{error}</p>;

  return (
    <div>
      {!accountSelected && (
        <div style={styles.wrapper}>
          <input
            type="text"
            placeholder="Поиск аккаунта"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={styles.search}
          />

          <div style={styles.list}>
            {filteredAccounts.map((acc) => (
              <Card
                {...acc}
                onClick={() => setAccountSelected(acc)}
                key={acc.id}
              />
            ))}
          </div>
        </div>
      )}

      {accountSelected && (
        <AccountPage
          {...accountSelected}
          onBackClick={() => setAccountSelected(null)}
        ></AccountPage>
      )}
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
};
