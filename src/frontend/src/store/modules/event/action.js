import UserLunchService from "@/services/company_calendar/user-lunch";

export default {
  async getUserLunches({ commit }) {
    const userLunches = await UserLunchService.get();
    const filter = userLunches.data.map((e) => ({
      title: e.has_veggie ? "Veggie Lunch" : "Lunch",
      id: e.id,
      start: e.date,
      end: e.date,
      has_veggie: e.has_veggie,
      color: e.has_veggie ? "#90BE6D" : "#F9C74F",
    }));
    commit("SET_USER_lUNCHES", filter);
    return filter;
  },
};
