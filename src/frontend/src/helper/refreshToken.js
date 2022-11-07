export function refreshToken() {
  const store = require("../store");
  return store.default.getters["scope/tokenInfo"].refresh_token || undefined;
}
