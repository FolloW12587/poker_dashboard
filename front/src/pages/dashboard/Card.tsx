import { useEffect, useState } from "react";
import { getBalanceChanges, type Account } from "../../api/accounts";
import { FiChevronRight } from "react-icons/fi";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { useNavigate } from "react-router";

dayjs.extend(relativeTime);

export default function Card(acc: Account) {
  const [change, setChange] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadChangesForAccount();
  }, []);

  const dateStr = acc.last_balance_update.replace(/\.\d+Z$/, "Z");
  const date = new Date(dateStr);
  const timeSince = isNaN(date.getTime())
    ? "неизвестно"
    : dayjs(date).fromNow(); // Используем dayjs для красивого формата

  const colorStyle =
    change == 0
      ? styles.textNeutral
      : change > 0
      ? styles.textGreen
      : styles.textRed;

  async function loadChangesForAccount() {
    const dateTo = new Date();
    const dateFrom = new Date(dateTo.getTime() - 24 * 60 * 60 * 1000);

    const isoFrom = dateFrom.toISOString();
    const isoTo = dateTo.toISOString();

    const results = await getBalanceChanges(acc.id, isoFrom, isoTo).then(
      (list) => {
        return list.reduce((sum, x) => sum + x.balance_diff, 0);
      }
    );

    setChange(results);
    setLoading(false);
  }

  const handleClick = (id: string) => {
    navigate(`/accounts/${id}`);
  };

  return (
    <div
      key={acc.id}
      className="card fade-in"
      onClick={() => handleClick(acc.id)}
    >
      <div style={styles.left}>{acc.name}</div>
      <div style={styles.right}>
        <div style={styles.balanceWrapper}>
          <div style={styles.balance}>{acc.current_balance}$</div>
          <div style={styles.lastUpdate}>{timeSince}</div>
        </div>
        <div style={styles.changeBox}>
          {loading ? (
            <div className="skeleton" style={styles.skeleton}></div>
          ) : (
            <div style={colorStyle}>
              {change >= 0 ? "+" : ""}
              {change.toFixed(2)}$
            </div>
          )}
          <div style={styles.lastUpdate}>last 24h</div>
        </div>
        <FiChevronRight style={styles.icon} />
      </div>
    </div>
  );
}

const styles = {
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

  textRed: {
    fontSize: 12,
    color: "#EE4B2B",
    lineHeight: "18pt",
  } as React.CSSProperties,

  textGreen: {
    fontSize: 12,
    color: "#00D100",
  } as React.CSSProperties,

  textNeutral: {
    fontSize: 12,
    color: "#aaa",
  } as React.CSSProperties,

  changeBox: {
    minWidth: 80,
    textAlign: "right",
  } as React.CSSProperties,

  skeleton: {
    width: 50,
    height: 14,
    marginLeft: "auto",
    borderRadius: 4,
  } as React.CSSProperties,
};
