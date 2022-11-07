import BaseService from "../base";

class PhotoService extends BaseService {
  get entity() {
    return "photo";
  }

  create(data) {
    const photo = this.request().post(`user/${this.entity}`, data);
    return photo;
  }

  get(profileId) {
    const photo = this.request()
      .get(`user/${this.entity}/${profileId}`)
      .catch((err) => console.log(err));
    return photo;
  }
}

export default new PhotoService();
