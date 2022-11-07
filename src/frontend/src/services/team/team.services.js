import BaseService from "../base";

class TeamService extends BaseService {
  get entity() {
    return "team";
  }

  create(data) {
    const team = this.request().post(`/${this.entity}/`, data);
    return team;
  }

  importTeams(data) {
    return this.request().post(`${this.entity}/import-teams`, data);
  }

  getTeams(page, page_size) {
    return this.request().get(
      `/${this.entity}/?page=${page}&page_size=${page_size}`
    );
  }

  getAll() {
    return this.request().get(`/${this.entity}/get_all`);
  }

  get(id) {
    const team = this.request().get(`/${this.entity}/${id}`);
    return team;
  }

  update(id, data) {
    return this.request().put(`${this.entity}/${id}`, data);
  }

  delete(id) {
    return this.request().delete(`${this.entity}/${id}`);
  }

  addMember(id, data) {
    return this.request().put(`${this.entity}/${id}/add_member`, data);
  }

  modifyMembers(id, data) {
    return this.request().put(`${this.entity}/${id}/modify_members`, data);
  }

  removeMember(id, data) {
    return this.request().put(`${this.entity}/${id}/remove_member`, data);
  }

  getNewTeams(userId) {
    return this.request().get(`${this.entity}/${userId}/get_new_teams`);
  }

  getLeaders(name) {
    return this.request().get(`${this.entity}/send_leader?name=${name}`);
  }

  moveTeam(data) {
    return this.request().put(`${this.entity}/move_team`, data);
  }

  setLeader(teamId, data) {
    return this.request().put(`${this.entity}/${teamId}/set_leader`, data);
  }

  setManager(teamId, data) {
    return this.request().put(
      `${this.entity}/${teamId}/set_project_manager`,
      data
    );
  }

  searchRequest(key, page, page_size) {
    return this.request().get(
      `/${this.entity}/search?key=${key}&page=${page}&page_size=${page_size}`
    );
  }

  removeTeam(teamId) {
    return this.request().delete(`${this.entity}/${teamId}`);
  }

  deleteTeams(ids) {
    return this.request().post(`/${this.entity}/destroy_multi_teams`, {
      team_ids: ids,
    });
  }

  getFloatMembers() {
    return this.request().get(`${this.entity}/float_members`);
  }

  getMyTeams() {
    try {
      return this.request().get(`${this.entity}/get_my_teams`);
    } catch {
      return null;
    }
  }
}

export default new TeamService();
