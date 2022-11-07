import moment from "moment/moment";

export const FORMAT = {
  DATE: "YYYY-MM-DD",
  DATE_TIME: "YYYY-MM-DD hh:mm:ss",
};

export function formatDate(value, format = null) {
  if (!value) {
    return null;
  }
  if (format) {
    return moment(String(value)).format(format);
  }
  return moment(String(value)).format(FORMAT.DATE);
}
