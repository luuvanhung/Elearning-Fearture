export function convertDuration(time) {
  return new Date(1000 * time).toISOString().substr(11, 8);
}
