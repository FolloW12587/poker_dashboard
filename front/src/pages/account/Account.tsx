import { useState } from "react";
import {
  getBalanceChanges,
  type Account,
  type BalanceChange,
} from "../../api/accounts";
import {
  Button,
  Flex,
  Segmented,
  Space,
  Typography,
  DatePicker,
  type TimeRangePickerProps,
} from "antd";
import ChangesTable from "./ChangesTable";
import dayjs from "dayjs";
import type { Dayjs } from "dayjs";
import BalanceChart from "./BalanceChart";
import BalanceDiffChart from "./BalanceDiffChart";

const { Text, Title } = Typography;
const { RangePicker } = DatePicker;

const contentViewOptions = ["table", "balance chart", "balance diff chart"];

interface AccountProps extends Account {
  onBackClick?: () => void;
}

const today = dayjs();

const rangePresets: TimeRangePickerProps["presets"] = [
  { label: "7 дней", value: [today.add(-7, "d"), today] },
  { label: "14 дней", value: [today.add(-14, "d"), today] },
  { label: "30 дней", value: [today.add(-30, "d"), today] },
  { label: "90 дней", value: [today.add(-90, "d"), today] },
];

export default function AccountPage({
  id,
  name,
  current_balance,
  last_balance_update,
  onBackClick,
}: AccountProps) {
  const [changes, setChanges] = useState<BalanceChange[]>([]);
  const [loading, setLoading] = useState(false);
  const [contentViewOption, setContentViewOption] = useState(
    contentViewOptions[0]
  );
  const [dateTo, setDateTo] = useState<Dayjs>(today);
  const [dateFrom, setDateFrom] = useState<Dayjs>(today);

  async function loadChangesForAccount() {
    setLoading(true);
    const startOfDay = dateFrom.toDate();
    startOfDay.setHours(0, 0, 0, 0);

    const endOfDay = dateTo.toDate();
    endOfDay.setHours(23, 59, 59, 999);

    const isoFrom = startOfDay.toISOString();
    const isoTo = endOfDay.toISOString();

    const results = await getBalanceChanges(id, isoFrom, isoTo).then((list) => {
      return list;
    });

    setChanges(results);
    setLoading(false);
  }

  const onRangeChange = (
    dates: null | (Dayjs | null)[],
    dateStrings: string[]
  ) => {
    if (dates && dates[0] && dates[1]) {
      console.log("From: ", dates[0], ", to: ", dates[1]);
      console.log("From: ", dateStrings[0], ", to: ", dateStrings[1]);
      setDateFrom(dates[0]);
      setDateTo(dates[1]);
    } else {
      console.log("Clear");
    }
  };

  return (
    <Flex
      vertical
      style={
        {
          maxWidth: 800,
          margin: "40px auto",
          padding: "0 20px",
        } as React.CSSProperties
      }
    >
      <Flex justify="space-between" align="flex-start">
        <Space style={{ padding: "55px 0" }}>
          <Button onClick={onBackClick} color="cyan" variant="text">
            Назад
          </Button>
        </Space>
        <Flex vertical style={{ padding: "20px 0px" }} align="flex-end">
          <Title>{name}</Title>
          <Text>Баланс: {current_balance}$</Text>
          <Text>
            Последнее обновление баланса:{" "}
            {dayjs(last_balance_update).locale("ru").fromNow()}
          </Text>
        </Flex>
      </Flex>
      <Flex justify={"space-between"}>
        <Segmented
          options={contentViewOptions}
          onChange={(value) => setContentViewOption(value)}
        ></Segmented>
        <Space>
          <RangePicker
            presets={rangePresets}
            onChange={onRangeChange}
            defaultValue={[today, today]}
          ></RangePicker>
          <Button
            onClick={loadChangesForAccount}
            loading={loading}
            disabled={loading}
          >
            Обновить
          </Button>
        </Space>
      </Flex>
      {contentViewOption == contentViewOptions[0] && (
        <ChangesTable changes={changes}></ChangesTable>
      )}

      {contentViewOption == contentViewOptions[1] && (
        <BalanceChart changes={changes}></BalanceChart>
      )}

      {contentViewOption == contentViewOptions[2] && (
        <BalanceDiffChart changes={changes}></BalanceDiffChart>
      )}
    </Flex>
  );
}
