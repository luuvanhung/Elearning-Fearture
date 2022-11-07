import BaseService from "../base";

class ProbationService extends BaseService {
  get entity() {
    return "probation";
  }

  async createEvaluationTemplate(data) {
    try {
      return await this.request().post(
        `${this.entity}/evaluation_template`,
        data
      );
    } catch (e) {
      return e.response;
    }
  }

  async getEvaluationTemplate() {
    try {
      return await this.request().get(`${this.entity}/evaluation_template`);
    } catch (e) {
      return e.response;
    }
  }

  async getListProbations() {
    try {
      return await this.request().get(`${this.entity}/`);
    } catch (e) {
      return e.response;
    }
  }

  async deleteProbation(id) {
    try {
      return await this.request().delete(`${this.entity}/${id}`);
    } catch (e) {
      return false;
    }
  }

  async getManagementTemplate(
    page = 1,
    pageSize = 12,
    id = "",
    office = "",
    name = "",
    create_at = "",
    update_at = "",
    status = 1
  ) {
    try {
      const request = await this.request().get(
        `/${this.entity}/evaluation_template`,
        {
          params: {
            id: id,
            office: office,
            name: name,
            create_at: create_at,
            update_at: update_at,
            status: status,
            page: page,
            page_size: pageSize,
          },
        }
      );
      return request;
    } catch (error) {
      return [];
    }
  }

  async updateEvaluationTemplate(data) {
    try {
      return await this.request().put(
        `${this.entity}/evaluation_template/${data["id"]}`,
        data
      );
    } catch (e) {
      return e.response;
    }
  }

  async deleteEvaluationTemplate(id) {
    try {
      return await this.request().delete(
        `/${this.entity}/evaluation_template/${id}`
      );
    } catch (e) {
      return e.response;
    }
  }

  handleTemplateActive(id) {
    return this.request().patch(`${this.entity}/evaluation_template/${id}`);
  }

  async getPage(params) {
    const res = await this.request().get(`/${this.entity}/`, { params });
    const probations = res.data;
    if (probations) {
      return probations;
    } else return [];
  }
}

export default new ProbationService();
