import { daysOfWeek } from "@/const/daysOfWeek";
import _ from "lodash";

export function handleDataAPI(dataAPI) {
  const uniqueDay = _.uniqBy(dataAPI, "dow");
  return uniqueDay.map((dayArray) => {
    const newData = {
      daysOfWeek: daysOfWeek.find((item) => item.dow === dayArray.dow),
      data: [],
    };
    dataAPI.forEach((item) => {
      if (item.dow === dayArray.dow) {
        newData.data.push(item);
      }
    });
    return newData;
  });
}
