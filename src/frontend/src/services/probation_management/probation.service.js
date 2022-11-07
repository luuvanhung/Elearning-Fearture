import BaseService from "../base";

class ProbationService extends BaseService {
  get entity() {
    return "probation";
  }

  async create(data) {
    return await this.request().post(`/${this.entity}/`, data);
  }

  async update(data, id) {
    return await this.request().put(`/${this.entity}/${id}`, data);
  }

  async getCurrentProbation(id) {
    try {
      return await this.request().get(`${this.entity}/${id}`);
    } catch (e) {
      console.log(e);
    }
  }

  async getProbation(id) {
    try {
      return await this.request().get(`${this.entity}/${id}`);
    } catch (e) {
      console.log(e);
    }
  }

  async getEvaluationCompetencesAssessorRole(evaluation_template_id) {
    try {
      return await this.request().get(
        `${this.entity}/evaluation_template/get_competence_assessor_role?evaluation_template_id=${evaluation_template_id}`
      );
    } catch (e) {
      console.log(e);
    }
  }

  async getEvaluationOverallsAssessorRole(evaluation_template_id) {
    try {
      return await this.request().get(
        `${this.entity}/evaluation_template/get_overall_assessor_role?evaluation_template_id=${evaluation_template_id}`
      );
    } catch (e) {
      console.log(e);
    }
  }

  async getEvaluationCompetences(
    evaluation_template_id,
    employee_id = null,
    probation_line_manager_id = null
  ) {
    try {
      return await this.request().get(
        `${this.entity}/evaluation_template/get_evaluation_competence_and_role`,
        {
          params: {
            evaluation_template_id: evaluation_template_id,
            employee_id: employee_id,
            probation_line_manager_id: probation_line_manager_id,
          },
        }
      );
    } catch (e) {
      console.log(e);
    }
  }

  async getEvaluationOverall(
    evaluation_template_id,
    employee_id = null,
    probation_line_manager_id = null
  ) {
    try {
      return await this.request().get(
        `${this.entity}/evaluation_template/get_evaluation_overall_comment_and_role`,
        {
          params: {
            evaluation_template_id: evaluation_template_id,
            employee_id: employee_id,
            probation_line_manager_id: probation_line_manager_id,
          },
        }
      );
    } catch (e) {
      console.log(e);
    }
  }

  async getAllActiveTemplate() {
    try {
      return await this.request().get(
        `${this.entity}/evaluation_template/list_active`
      );
    } catch (e) {
      console.log(e);
    }
  }
}

export default new ProbationService();
