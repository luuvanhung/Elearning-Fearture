import ApiService from "../ApiService";

class EvaluationTemplateTypeServices extends ApiService {
  get entity() {
    return "probation/evaluation_template_type";
  }

  async getAll() {
    return await this.request().get(`${this.entity}`);
  }

  async add(data) {
    const option = {
      method: "post",
      url: `/${this.entity}`,
      data: data,
    };
    return this.request(option);
  }

  async edit(id, data) {
    const option = {
      method: "put",
      url: `/${this.entity}/${id}`,
      data: data,
    };
    return this.request(option);
  }

  async delete(id) {
    const option = {
      method: "delete",
      url: `/${this.entity}/${id}`,
    };
    return this.request(option);
  }
}

export default new EvaluationTemplateTypeServices();
