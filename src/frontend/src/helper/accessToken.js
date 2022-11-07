export function accessToken() {
  const store = require("../store");
  return store.default.getters["scope/tokenInfo"].access_token || null;
}
