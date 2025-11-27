import { motion, AnimatePresence } from "framer-motion";
import { useEffect, useState } from "react";
import { getAccounts, type Account } from "../../api/accounts";
import "./Dashboard.css"; // Для анимации fade-in
import Card from "./Card";

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
    <div style={{ position: "relative" }}>
      <AnimatePresence mode="sync">
        {!accountSelected && (
          <motion.div
            key="list"
            initial={{ opacity: 1 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            style={styles.wrapper}
          >
            <input
              type="text"
              placeholder="Поиск аккаунта"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={styles.search}
            />

            <div style={styles.list}>
              {filteredAccounts.map((acc) => (
                <motion.div key={acc.id} layoutId={acc.id}>
                  <Card
                    showChevron={true}
                    {...acc}
                    onClick={() => setAccountSelected(acc)}
                  />
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {accountSelected && (
          <motion.div
            key="single"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            // style={{ paddingTop: "40px" }}
          >
            {/* ВАЖНО: тот же layoutId */}
            <motion.div layoutId={accountSelected.id}>
              <Card
                showChevron={false}
                {...accountSelected}
                onClick={() => {}}
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
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
