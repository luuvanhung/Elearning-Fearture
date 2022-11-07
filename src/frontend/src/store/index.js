import Vue from "vue";
import Vuex from "vuex";
import user from "./modules/user";
import events from "./modules/event";
import eventCollapse from "./modules/eventCollapse";
import offTypeGroup from "./modules/offTypeGroup";
import skill from "./modules/skill";
import offType from "./modules/offType";
import role from "./modules/role";
import probation from "./modules/probation";
import leaveService from "../services/leave_management/managementLeave.service";
import scope from "./modules/scope";
import title from "./modules/title";
import team from "./modules/team";
import squad from "./modules/squad";
import createPersistedState from "vuex-persistedstate";
import elearning from "./modules/elearning";
const cookieparser = require("cookieparser");

Vue.use(Vuex);

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    token: null,
    countNoti: 0,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    add(state) {
      state.countNoti += 1;
    },
    subtract(state) {
      state.countNoti -= 1;
    },
    setCountNoti(state, count) {
      state.countNoti = count.count;
    },
  },
  actions: {
    nuxtServerInit({ commit }, { req }) {
      let token = null;
      if (req.headers.cookie) {
        const parsed = cookieparser.parse(req.headers.cookie);
        try {
          token = JSON.parse(parsed.token);
        } catch (err) {
          // No valid cookie found
        }
      }
      commit("setToken", token);
    },
    async setCountNoti({ commit }) {
      const count = await leaveService.countRequest();
      commit("setCountNoti", count);
    },
  },
  getters: {
    showNotification(state) {
      return state.countNoti;
    },
  },
  modules: {
    user: user,
    event: events,
    collapse: eventCollapse,
    offType: offType,
    offTypeGroup: offTypeGroup,
    skill: skill,
    role: role,
    scope: scope,
    probation: probation,
    title: title,
    elearning: elearning,
    team: team,
    squad: squad,
  },
});
