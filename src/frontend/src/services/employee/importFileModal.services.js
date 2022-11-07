import BaseService from "../base";

class importFileModalServices extends BaseService {
  get entity() {
    return "admins";
  }

  async handleFileUploadAPI(data) {
    const response = await this.request().post(
      `${this.entity}/check-file`,
      data,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response;
  }

  async submitFileAPI(data) {
    const response = this.request().post(`${this.entity}/import-file`, data);
    return response;
  }
}

export default new importFileModalServices();
