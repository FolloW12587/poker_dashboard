import { useEffect, useState } from "react";
import { getBalanceChanges, type Account } from "../../api/accounts";
import dayjs from "dayjs";
import "dayjs/locale/ru";
import relativeTime from "dayjs/plugin/relativeTime";
import { Skeleton } from "antd";

dayjs.extend(relativeTime);

interface CardProps extends Account {
  onClick?: () => void;
}

export default function Card({
  id,
  name,
  current_balance,
  last_balance_update,
  onClick,
}: CardProps) {
  const [change, setChange] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadChangesForAccount();
  }, []);

  // const dateStr = last_balance_update.replace(/\.\d+Z$/, "Z");
  // const date = new Date(dateStr);
  const timeSince = dayjs(last_balance_update).locale("ru").fromNow(); // Используем dayjs для красивого формата

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

    const results = await getBalanceChanges(id, isoFrom, isoTo).then((list) => {
      return list.reduce((sum, x) => sum + x.balance_diff, 0);
    });

    setChange(results);
    setLoading(false);
  }

  return (
    <div key={id} className="card fade-in" onClick={onClick}>
      <div style={styles.left}>{name}</div>
      <div style={styles.right}>
        <div style={styles.balanceWrapper}>
          <div style={styles.balance}>{current_balance}$</div>
          <div style={styles.lastUpdate}>{timeSince}</div>
        </div>
        <div style={styles.changeBox}>
          {loading ? (
            <Skeleton.Button active />
          ) : (
            <div style={colorStyle}>
              {change >= 0 ? "+" : ""}
              {change.toFixed(2)}$
            </div>
          )}
          <div style={styles.lastUpdate}>за 24ч</div>
        </div>
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
};
