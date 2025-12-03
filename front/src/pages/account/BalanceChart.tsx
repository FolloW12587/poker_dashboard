import { Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";
import { type BalanceChange } from "../../api/accounts";
import dayjs from "dayjs";

interface BalanceChartProps {
  changes: BalanceChange[];
}

export default function BalanceChart({ changes }: BalanceChartProps) {
  const prepareBalanceHistory = () => {
    return [...changes].map((b) => ({
      date: dayjs(b.created_at).toDate(),
      balance: b.balance,
    }));
  };

  return (
    <LineChart width={600} height={300} data={prepareBalanceHistory()}>
      <XAxis dataKey="date" tickFormatter={(d) => d.toLocaleDateString()} />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="balance" stroke="#8884d8" />
    </LineChart>
  );
}
