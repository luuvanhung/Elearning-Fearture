import BaseService from "../base";

class ProfileService extends BaseService {
  get entity() {
    return "user/profile";
  }

  async createProfile(data) {
    try {
      const profile = await this.request().post(`${this.entity}`, data);
      return profile;
    } catch (e) {
      return e.response;
    }
  }

  async removeLineManager(id) {
    try {
      return await this.request().delete(
        `${this.entity}/${id}/remove_line_manager`
      );
    } catch (e) {
      return e.response;
    }
  }

  async setLineManager(id, personal_email) {
    try {
      return await this.request().post(
        `${this.entity}/${id}/set_line_manager`,
        {
          personal_email: personal_email,
        }
      );
    } catch (e) {
      return e.response;
    }
  }

  async setLevelApprove(id, level) {
    try {
      return await this.request().post(
        `${this.entity}/${id}/set_level_approved`,
        {
          level: level,
        }
      );
    } catch (e) {
      return e.response;
    }
  }

  async getOneProfile(id) {
    try {
      const profile = await this.request().get(`${this.entity}/${id}`);
      return profile;
    } catch (e) {
      return e.response;
    }
  }

  async updateProfile(id, data) {
    try {
      const profile = await this.request().put(`${this.entity}/${id}`, data);
      return profile;
    } catch (e) {
      return e.response;
    }
  }

  async getAllProfile() {
    const res = await this.request().get(`${this.entity}`);
    const profiles = res.data;
    if (profiles) {
      return profiles;
    }
    return [];
  }

  async getAutoBookingLunchProfile() {
    try {
      return await this.request().get(
        `${this.entity}/get_auto_booking_lunch_profiles`
      );
    } catch (e) {
      return e.response;
    }
  }

  async deleteProfile(id) {
    try {
      const res = await this.request().delete(`${this.entity}/${id}`);
      return res;
    } catch (e) {
      return e.response;
    }
  }

  async updateAutoBookingLunch(id, data) {
    try {
      const res = await this.request().put(
        `${this.entity}/${id}/update_auto_booking`,
        data
      );
      return res;
    } catch (e) {
      return e.response;
    }
  }

  async updateListAutoBookingLunch(data) {
    try {
      const res = await this.request().put(
        `${this.entity}/update_list_auto_booking`,
        data
      );
      return res;
    } catch (e) {
      return e.response;
    }
  }

  async updateUserVeggie(id, data) {
    try {
      const res = await this.request().put(
        `${this.entity}/${id}/update_veggie_user`,
        data
      );
      return res;
    } catch (e) {
      return e.response;
    }
  }
}

export default new ProfileService();
