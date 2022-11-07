<template>
  <div class="mt-3">
    <div class="mt-2">
      <el-input
        v-model="search"
        style="width: 25%"
        placeholder="Search available employees"
      >
      </el-input>
    </div>
    <div class="main-profile row">
      <div class="mx-auto col-md-6">
        <h5 class="card-header bg-info text-center py-4">
          <strong class="header-title">Available Employees</strong>
        </h5>
        <div
          class="my-card"
          v-for="member_row in filteredList"
          :key="member_row.id"
        >
          <div>
            {{ member_row.name }}
            <span class="email">{{ ` (${member_row.email})` }}</span>
          </div>
          <img
            @click="add(member_row)"
            class="img-action"
            :src="require('@/static/images/send-to-right.svg')"
          />
        </div>
      </div>
      <div class="col-md-6 mx-auto">
        <h5 class="card-header bg-info py-4 text-center">
          <strong class="header-title">Team Members</strong>
        </h5>
        <div
          class="my-card justify-content-start"
          v-for="row in teamMembers"
          :key="row.id"
        >
          <img
            v-if="row.id !== teamLeaderId"
            @click="remove(row)"
            class="img-action"
            :src="require('@/static/images/send-to-left.svg')"
          />
          <img
            v-else
            class="img-action"
            :src="require('@/static/images/crown.svg')"
          />
          <div class="mx-5">
            {{ row.name }}
            <span class="email">{{ ` (${row.email})` }}</span>
          </div>
        </div>
        <div class="text-center mt-3">
          <el-button type="primary" @click="send()">Save</el-button>
          <router-link :to="'/teams/' + teamId" class="ml-3">
            <el-button type="danger">Cancel</el-button>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import TeamService from "@/services/team/team.services";

export default {
  name: "id_edit_team",
  middleware: "authentication",
  data() {
    return {
      teamMembers: [],
      availableMembers: [],
      teamId: "",
      search: "",
      teamLeaderId: "",
    };
  },
  computed: {
    filteredList() {
      if (this.search === "") {
        let arr = this.availableMembers;
        return arr;
      }
      const newArray = this.availableMembers.filter((name) =>
        this.isEmployee(name)
      );
      return newArray;
    },
  },
  methods: {
    async asyncData() {
      const res = await TeamService.get(`${this.$route.params.id}`);
      res.data.employee_list.forEach((member) => {
        member.id = member.user;
      });
      this.teamMembers = res.data.employee_list;
      this.teamId = this.$route.params.id;
      this.teamLeaderId = res.data.team_leader;
      this.moveLeaderToFirst();
    },
    moveLeaderToFirst() {
      const leader = this.teamMembers.find(
        (member) => member.id === this.teamLeaderId
      );
      if (leader) {
        this.teamMembers.splice(this.teamMembers.indexOf(leader), 1);
        this.teamMembers.unshift(leader);
      }
    },

    async getFloatMembers() {
      const res = await TeamService.getFloatMembers();
      this.availableMembers = res.data;
    },
    add(member) {
      this.teamMembers.push(member);
      this.availableMembers.splice(this.availableMembers.indexOf(member), 1);
    },
    remove(member) {
      this.availableMembers.push(member);
      this.teamMembers.splice(this.teamMembers.indexOf(member), 1);
    },
    async send() {
      const formData = new FormData();
      let arr = [];
      for (let i in this.teamMembers) {
        arr.push(this.teamMembers[i].id);
      }
      formData.append("ids", arr.join(","));
      let response = await TeamService.modifyMembers(
        this.$route.params.id,
        formData
      );
      if (response && response.status == 200) {
        this.$toast.success("Added Successfully");
      } else {
        this.$toast.error("Error: " + response.data.detail);
      }
    },
    isEmployee(value) {
      return value.name.toLowerCase().includes(this.search.toLowerCase());
    },
  },
  created() {
    this.asyncData();
    this.getFloatMembers();
  },
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
