import axios from "axios";

const getSkillLevels = () => axios.get("/skill/level");

const addSkillLevels = (data) => axios.post("/skill/level", data);

const deleteSkillLevels = (id) => axios.delete(`/skill/level/${id}`);

const editSkillLevels = (id, data) => axios.put(`/skill/level/${id}`, data);

export default {
  getSkillLevels,
  addSkillLevels,
  editSkillLevels,
  deleteSkillLevels,
};
