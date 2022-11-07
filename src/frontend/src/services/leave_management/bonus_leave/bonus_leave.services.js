import BaseService from "../../base";

class BonusLeaveService extends BaseService {
  get entity() {
    return "workday/bonus-leave";
  }

  get(page_size, page) {
    const res = this.request().get(
      `${this.entity}?page_size=${page_size}&page=${page}`
    );
    return res;
  }

  getBonusLeaveUserInYear(userId) {
    const res = this.request().get(
      `${this.entity}/bonus_leave_user_year?id=${userId}`
    );
    return res;
  }

  edit(data) {
    return this.request().put(`${this.entity}/${data.id}`, data);
  }

  create(data) {
    const res = this.request().post(`${this.entity}`, data);
    return res;
  }

  delete(id) {
    return this.request().delete(`${this.entity}/${id}`);
  }

  deleteBonusLeaves(ids) {
    return this.request().post(`/${this.entity}/destroy_multi_bonus`, {
      bonus_leave_ids: ids,
    });
  }

  searchRequest(reason, name, bonusTypeId, fromDate, toDate, page, page_size) {
    const res = this.request().get(`${this.entity}/search`, {
      params: {
        reason: reason,
        name: name,
        bonus_type_id: bonusTypeId,
        from_date: fromDate,
        to_date: toDate,
        page: page,
        page_size: page_size,
      },
    });
    return res;
  }
}

export default new BonusLeaveService();
