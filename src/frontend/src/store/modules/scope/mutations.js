import decodeToken from "jwt-decode";

export default {
  GET_TOKEN_INFO: (state, payload) => {
    state.tokenInfo = payload;
  },
  GET_APPLICATION_SCOPE: (state, payload) => {
    state.applicationScope = payload;
  },
  SET_TOKEN_INFO: (state, { access_token, refresh_token }) => {
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
    state.tokenInfo = token;
  },

  LOGOUT: (state) => {
    state.tokenInfo = null;
  },
};
