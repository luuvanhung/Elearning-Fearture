import ApiService from "@/services/ApiService";

class TopicService extends ApiService {
  get entity() {
    return "elearning/topics";
  }

  // createMultiple(data) {
  //   return this.request().post(
  //     `/elearning/${this.entity}`,
  //     data
  //   );
  // }

  async create(data) {
    const option = {
      method: "post",
      url: this.entity,
      data: data,
    };
    const response = await this.request(option);
    return response ? response : null;
  }

  async getAll(params) {
    try {
      const res = await this.request().get(this.entity, {
        params,
      });
      const topics = res.data;
      return topics;
    } catch (error) {
      return [];
    }
  }

  async search(params) {
    try {
      const res = await this.request().get(this.entity, {
        params,
      });
      const topics = res.data;
      return topics;
    } catch (error) {
      return [];
    }
  }
  // get(id) {
  //   return this.request({ auth: true }).get(`elearning/${this.entity}/${id}`);
  // }
  //
  async update(topic) {
    const option = {
      method: "put",
      url: `${this.entity}/${topic.id}`,
      data: topic,
    };
    const response = await this.request(option);
    return response ? response : null;
  }

  async delete(id) {
    const option = {
      method: "delete",
      url: `${this.entity}/${id}`,
    };
    const response = await this.request(option);
    return response ? response : null;
  }
}

export default new TopicService();
