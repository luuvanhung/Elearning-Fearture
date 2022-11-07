import BaseService from "../base";
let percentage = null;
class EmbedAttachmentsService extends BaseService {
  get entity() {
    return "embed/attachments";
  }
  async get(id) {
    try {
      return await this.request().get(`${this.entity}/${id}`);
    } catch (e) {
      return null;
    }
  }

  async getFile(url) {
    try {
      return await this.request().get(`${url}`);
    } catch (e) {
      return null;
    }
  }

  async getTranscript(id) {
    try {
      return await this.request().get(`${this.entity}/${id}/get_transcripts`);
    } catch (e) {
      return null;
    }
  }
}

export default new EmbedAttachmentsService();
