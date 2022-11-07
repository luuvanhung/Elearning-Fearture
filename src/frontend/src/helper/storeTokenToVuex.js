import { decodeToken } from "../utils/decodeToken";

export function storeTokenToVuex(access_token, refresh_token) {
  const { sub, iat, exp, nbf, scope } = decodeToken(access_token);
  const token = {
    access_token: access_token,
    refresh_token: refresh_token,
    sub: sub,
    iat: iat,
    exp: exp,
    nbf: nbf,
    scope: scope,
  };
  const store = require("../store");
  store.default.dispatch("scope/getTokenInfo", token);
  return token;
}
