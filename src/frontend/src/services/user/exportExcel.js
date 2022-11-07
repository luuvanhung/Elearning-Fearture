import BaseService from "../base";

class ExportExcelService extends BaseService {
  get entity() {
    return "user/get_non_paginate";
  }

  get() {
    const res = this.request().get(`${this.entity}`);
    return res;
  }

  search(name, email, birthdayMonth, joinDate, gender, title, team, active) {
    let temp_active = active === true ? 1 : 0;
    const res = this.request().get(`user/search_non_paginate`, {
      params: {
        email: email,
        name: name,
        title: title,
        birthday: birthdayMonth,
        joindate: joinDate,
        gender: gender,
        team: team,
        active: temp_active,
      },
    });
    return res;
  }
}

export default new ExportExcelService();
