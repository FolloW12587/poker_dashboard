import { Table, Tag, Typography } from "antd";
import type { TableProps } from "antd";
import {
  BalanceChangeState,
  BalanceChangeStateMapping,
  type BalanceChange,
} from "../../api/accounts";
import dayjs from "dayjs";

interface ChangesTableProps {
  changes: BalanceChange[];
}

const BalanceChangeStateColors: Record<BalanceChangeState, string> = {
  money_request: "purple",
  money_received: "lime",
  money_withdraw: "orange",
  update: "geekblue",
};

const columns: TableProps<BalanceChange>["columns"] = [
  {
    title: "Время",
    dataIndex: "created_at",
    key: "created_at",
    render: (value) => dayjs(value).format("YYYY-MM-DD HH:mm:ss"),
  },
  {
    title: "Тип события",
    dataIndex: "state",
    key: "state",
    render: (value: BalanceChange["state"]) => {
      return (
        <Tag color={BalanceChangeStateColors[value]}>
          {BalanceChangeStateMapping[value]}
        </Tag>
      );
    },
  },
  {
    title: "Баланс",
    dataIndex: "balance",
    key: "balance",
  },
  {
    title: "Изменение баланса",
    dataIndex: "balance_diff",
    key: "balance_diff",
    render: (value) => {
      const type = value == 0 ? "secondary" : value > 0 ? "success" : "danger";
      return <Typography.Text type={type}>{value}$</Typography.Text>;
    },
  },
];

export default function ChangesTable({ changes }: ChangesTableProps) {
  const reduced = changes.reduce(
    (prev, current) => (prev += current.balance_diff),
    0
  );
  const type = reduced == 0 ? "secondary" : reduced > 0 ? "success" : "danger";
  return (
    <Table
      columns={columns}
      dataSource={changes}
      footer={() => (
        <Typography.Text>
          Итого: <Typography.Text type={type}>{reduced}$</Typography.Text>
        </Typography.Text>
      )}
    ></Table>
  );
}
