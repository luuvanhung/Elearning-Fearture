import ApiService from "../ApiService";
import { accessToken } from "@/helper/accessToken";
import { decodeToken } from "@/utils/decodeToken";

export class ScopeService extends ApiService {
  get entity() {
    return `oauth2/applications/retrieve_all_scopes`;
  }

  getScopes() {
    const options = {
      method: "get",
      url: `${this.entity}`,
    };
    return this.request(options) || [];
  }

  getScopesFromStorage() {
    try {
      if (accessToken()) {
        return decodeToken(accessToken());
      } else return null;
    } catch (e) {
      console.log(e);
    }
  }
}

export default new ScopeService();
