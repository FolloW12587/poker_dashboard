import { Bar, BarChart, ReferenceLine, Tooltip, XAxis, YAxis } from "recharts";
import { BalanceChangeState, type BalanceChange } from "../../api/accounts";
import dayjs from "dayjs";

interface BalanceDiffChartProps {
  changes: BalanceChange[];
}

const CustomBarShape: React.FC<any> = (props) => {
  let { x, y, width, height, value } = props;

  const color = value >= 0 ? "#4caf50" : "#f44336";

  // Если высота отрицательная — нормализуем
  if (height < 0) {
    y = y + height; // переносим верхнюю точку вниз
    height = Math.abs(height);
  }

  return <rect x={x} y={y} width={width} height={height} fill={color} rx={2} />;
};

export default function BalanceDiffChart({ changes }: BalanceDiffChartProps) {
  const prepareBalanceDiffChart = () => {
    const excluded: BalanceChangeState[] = ["deposit", "withdraw"];

    return changes
      .filter((b) => !excluded.includes(b.state))
      .map((b) => ({
        date: dayjs(b.created_at).toDate(),
        diff: b.balance_diff,
        // state: BalanceChangeStateMapping[b.state],
      }));
  };

  return (
    <BarChart width={600} height={300} data={prepareBalanceDiffChart()}>
      <XAxis dataKey="date" tickFormatter={(d) => d.toLocaleDateString()} />
      <YAxis domain={["dataMin", "dataMax"]} />
      <ReferenceLine y={0} stroke="#000" strokeWidth={2} /> {/* линия 0 */}
      <Tooltip />
      <Bar dataKey="diff" shape={<CustomBarShape />} />
    </BarChart>
  );
}
