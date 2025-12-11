import { Table, Tag, Typography, Switch, Space } from "antd";
import type { TableProps } from "antd";
import {
  BalanceChangeState,
  BalanceChangeStateMapping,
  type BalanceChange,
} from "../../api/accounts";
import dayjs from "dayjs";
import { useState } from "react";

interface ChangesTableProps {
  changes: BalanceChange[];
}

const BalanceChangeStateColors: Record<BalanceChangeState, string> = {
  lock: "red",
  deposit: "lime",
  withdraw: "orange",
  update: "geekblue",
  shutdown: "gold",
};

export default function ChangesTable({ changes }: ChangesTableProps) {
  const [showRaw, setShowRaw] = useState(false);

  const columns: TableProps<BalanceChange>["columns"] = [
    {
      title: "Время",
      dataIndex: "created_at",
      key: "created_at",
      render: (value) => dayjs(value).format("YYYY-MM-DD HH:mm:ss"),
    },
    {
      title: "Тип события",
      dataIndex: showRaw ? "state_raw" : "state",
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
        const type =
          value === 0 ? "secondary" : value > 0 ? "success" : "danger";
        return <Typography.Text type={type}>{value}$</Typography.Text>;
      },
    },
  ];

  const prepareBalanceHistory = (balanceChanges: BalanceChange[]) => {
    return [...balanceChanges].sort((a, b) =>
      dayjs(b.created_at).diff(dayjs(a.created_at))
    );
  };

  const reduced = changes.reduce(
    (prev, current) => (prev += current.balance_diff),
    0
  );
  const type = reduced === 0 ? "secondary" : reduced > 0 ? "success" : "danger";

  return (
    <Space orientation="vertical" style={{ padding: "10px 0" }}>
      <Typography.Text>Показать сырой тип события</Typography.Text>
      <Switch checked={showRaw} onChange={setShowRaw} />
      <Table
        columns={columns}
        dataSource={prepareBalanceHistory(changes)}
        rowKey="id"
        footer={() => (
          <Typography.Text>
            Итого: <Typography.Text type={type}>{reduced}$</Typography.Text>
          </Typography.Text>
        )}
      />
    </Space>
  );
}
