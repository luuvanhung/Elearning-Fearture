import axios from "axios";

const getSkillDefinitions = () => axios.get("/skill/definition");

const addSkillDefinition = (data) => axios.post("/skill/definition", data);

const deleteSkillDefinition = (id) =>
  axios.delete(`/skill/definition/delete_all_skill_id?skill_id=${id}`);

const editSkillDefinition = (id, data) => axios.put(`/skill/level/${id}`, data);

const editSkill = (id, data) => axios.put(`/skill/${id}`, data);

export default {
  getSkillDefinitions,
  addSkillDefinition,
  editSkillDefinition,
  deleteSkillDefinition,
  editSkill,
};
