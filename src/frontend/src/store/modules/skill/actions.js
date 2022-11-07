import skillService from "@/services/skill/positionSkill.services";

export default {
  async getSkill({ commit }) {
    const skill = await skillService.getSkill();
    const filter = skill.data;
    commit("setSkill", filter);
    return filter;
  },

  async getPosition({ commit }) {
    const position = await skillService.getPosition();
    const filter = position.data;
    commit("setPosition", filter);
    return filter;
  },
};
