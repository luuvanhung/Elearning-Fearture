import moment from "moment/moment";

const getLunarDays = (calendarApi) => {
  let lunarDays = [];
  let dateCalendar = calendarApi.getDate();
  let year = dateCalendar.getFullYear();
  let month = dateCalendar.getMonth();
  for (let day = 0; day < 32; day++) {
    let lunarDate = moment()
      .year(year)
      .month(month)
      .date(day)
      .lunar()
      .format("DD");
    if (lunarDate === "15" || lunarDate === "01") {
      let date = `${year}-${month + 1}-${day}`;
      let nextDate = `${year}-${month + 1}-${day + 1}`;
      if (month < 9) {
        date = `${year}-0${month + 1}-${day}`;
        nextDate = `${year}-0${month + 1}-${day + 1}`;
        if (day === 31) {
          nextDate = `${year}-0${month + 2}-01`;
        }
        if (day < 10) {
          date = `${year}-0${month + 1}-0${day}`;
          nextDate = `${year}-0${month + 1}-0${day + 1}`;
        }
      } else {
        if (day === 31) {
          nextDate = `${year}-${month + 2}-01`;
        }
        if (day < 10) {
          date = `${year}-${month + 1}-0${day}`;
          nextDate = `${year}-${month + 1}-0${day + 1}`;
        }
      }
      let dataDay = {
        start: date,
        end: nextDate,
        display: "background",
        backgroundColor: "#45BCF3",
      };
      lunarDays.push(dataDay);
    }
  }
  return lunarDays;
};

export { getLunarDays };
