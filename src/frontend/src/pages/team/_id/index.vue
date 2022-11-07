<template>
  <div data-app class="m-4">
    <div class="text-danger">{{ errors }}</div>
    <div>
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">General Information</span>
          <template
            v-if="
              (hasScope('team:edit_my_team') && teamLeader === user_id) ||
              hasScope('team:edit_all_team')
            "
          >
            <el-button
              v-if="!isEditing"
              class="edit-button"
              type="text"
              @click="editTeam()"
            >
              <img
                :src="require('@/static/images/IconCardEdit.svg')"
                class="edit-icon"
                alt="edit"
              />
            </el-button>
            <el-button
              v-else
              class="edit-button"
              type="text"
              @click="submitForm('ruleForm')"
            >
              <img
                :src="require('@/static/images/IconCardSave.svg')"
                class="edit-icon"
                alt="save"
              />
            </el-button>
          </template>
        </div>
        <div class="text item mx-2">
          <el-form :model="teamData" ref="ruleForm" :rules="rules" status-icon>
            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2 re">Name:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !teamData.team_name ? NO_DATA : teamData.team_name }}
                </div>
                <el-form-item v-else prop="team_name">
                  <el-input
                    placeholder="Please input"
                    size="small"
                    maxlength="100"
                    type="text"
                    v-model="teamData.team_name"
                  ></el-input>
                </el-form-item>
              </div>
            </div>
            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Email:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !teamData.team_email ? NO_DATA : teamData.team_email }}
                </div>
                <el-form-item v-else prop="team_email">
                  <el-input
                    placeholder="Please input"
                    size="small"
                    type="email"
                    v-model="teamData.team_email"
                  ></el-input>
                </el-form-item>
              </div>
            </div>
            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Group:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !teamData.group ? NO_DATA : teamData.group.name }}
                </div>
                <el-form-item v-else prop="group">
                  <el-select
                    v-model="teamData.group"
                    placeholder="Select Group"
                    required
                  >
                    <el-option
                      v-for="group in groups"
                      :label="group.name"
                      :value="group.id"
                      :key="group.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </div>
            </div>

            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Office:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !teamData.office ? NO_DATA : teamData.office.name }}
                </div>
                <el-form-item v-else prop="office">
                  <el-select
                    v-model="teamData.office"
                    placeholder="Select Office"
                    required
                  >
                    <el-option
                      v-for="office in offices"
                      :label="office.name"
                      :value="office.id"
                      :key="office.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </div>
            </div>
            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Department:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{
                    !teamData.department ? NO_DATA : teamData.department.name
                  }}
                </div>
                <el-form-item v-else prop="department">
                  <el-select
                    v-model="teamData.department"
                    placeholder="Select Department"
                    required
                  >
                    <el-option
                      v-for="department in departments"
                      :label="department.name"
                      :value="department.id"
                      :key="department.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </div>
            </div>
            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2">Slack Channel:</div>
              <div class="col-7 col-xl-10 text-dark my-2">
                <div v-if="!isEditing">
                  {{
                    !teamData.slack_channel ? NO_DATA : teamData.slack_channel
                  }}
                </div>
                <el-form-item v-else prop="department">
                  <el-input
                    placeholder="Please input"
                    size="small"
                    type="text"
                    v-model="teamData.slack_channel"
                  ></el-input>
                </el-form-item>
              </div>
            </div>
            <div class="row mb-1">
              <div class="col-5 col-xl-2 my-2 re">Team Leader:</div>
              <div v-if="!isEditing" class="col-7 col-xl-2 text-dark my-2">
                <div v-if="!isEditing">
                  {{ !teamLeader ? "No Leader" : teamData.leader_name }}
                </div>
              </div>
              <div v-else class="col-7 d-flex text-dark flex-row">
                <el-form-item prop="team_leader">
                  <el-select
                    filterable
                    reserve-keyword
                    remote
                    :remote-method="remoteMethod"
                    v-model="teamData.team_leader"
                    placeholder="Select Team Leader"
                    required
                    size="large"
                  >
                    <div v-for="group in filteredUsers" :key="group.team.team">
                      <div class="background">
                        <div class="ml-3">{{ group.team.team }}</div>
                      </div>
                      <el-option
                        v-if="group.members.length === 0"
                        :value="NO_DATA"
                        :label="NO_DATA"
                        disabled
                      ></el-option>
                      <el-option
                        v-else
                        v-for="member in group.members"
                        :key="member.index"
                        :value="member.id"
                        :label="member.profile.name"
                      >
                        <span style="float: left">{{
                          member.profile.name
                        }}</span>
                        <span
                          style="float: right; color: #8c8c8c; font-size: 11px"
                        >
                          {{ member.profile.personal_email }}
                        </span>
                      </el-option>
                    </div>
                  </el-select>
                </el-form-item>
                <div class="align-self-start">
                  <el-radio-group v-model="searchByNameOrTeam">
                    <el-radio-button label="Team" />
                    <el-radio-button label="Name" />
                  </el-radio-group>
                </div>
              </div>
            </div>
          </el-form>
        </div>
      </el-card>

      <div
        v-if="
          (hasScope('team:edit_my_team') && teamLeader === user_id) ||
          hasScope('team:edit_all_team')
        "
      >
        <div class="justify-xl-end d-flex justify-content-end">
          <router-link
            :to="'/addMember/' + teamId"
            style="color: #ffffff; text-decoration: none"
          >
            <el-button type="primary">
              <font-awesome-icon :icon="['fas', 'user-plus']" /> Add Member
            </el-button>
          </router-link>
        </div>
      </div>
    </div>
    <div class="table-responsive mt-3">
      <el-table
        highlight-current-row
        :data="members"
        header-cell-class-name="bg-header-table"
        border
      >
        <el-table-column sortable label="Member Name">
          <template prop="name" slot-scope="scope">
            <router-link
              :to="'/profile/' + scope.row.user"
              title="Click to go to Profile page"
            >
              <strong class="text-dark">{{ scope.row.name }}</strong>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="email" sortable label="Member Email">
          <template slot-scope="scope">
            <el-link
              :href="'mailto:' + scope.row.email"
              title="Click to send mail"
              >{{ scope.row.email }}</el-link
            >
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="Phone"></el-table-column>
        <el-table-column label="Action" width="180">
          <template
            v-if="
              (hasScope('team:edit_my_team') && teamLeader === user_id) ||
              hasScope('team:edit_all_team')
            "
            slot-scope="scope"
          >
            <div class="text-center">
              <el-button
                size="mini"
                plain
                type="primary"
                class="btn m-1 btn-sm"
                @click="showMoveTeamModal(scope.row)"
                v-show="scope.row.title !== 'Leader'"
                title="Click to move this member to another team"
              >
                <font-awesome-icon
                  class="fa-fw text-info"
                  :icon="['fas', 'exchange-alt']"
                />
              </el-button>
              <el-button
                size="mini"
                plain
                type="primary"
                class="btn m-1 btn-sm"
                @click="showModal(scope.row)"
                v-show="scope.row.title !== 'Leader'"
                title="Click to remove this member"
              >
                <font-awesome-icon
                  class="fa-fw text-danger"
                  :icon="['fas', 'user-times']"
                />
              </el-button>
            </div>
            <div v-if="scope.row.title === 'Leader'">
              <div class="text-center">Team Leader</div>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="text-center col-sm-12" v-show="members.length === 0">
      <label class="col-sm-12 col-form-label alert alert-danger"
        >This team has no member</label
      >
    </div>
    <div class="text-center">
      <el-dialog :visible.sync="dialog" width="500" title="Team Management">
        <el-container class="fixed-top">
          <el-card class="mx-auto" max-width="500">
            <div slot="header" style="color: #25c9d0">
              <h3>Removing member</h3>
            </div>
            <div class="d-block text-center mb-4">
              Do you want to remove
              <p class="text-danger d-inline">{{ selectedUser.name }}</p>
              from team?
            </div>
            <el-button type="danger" @click="closeDialog()">Cancel</el-button>
            <el-button type="primary" @click="del()">Confirm</el-button>
          </el-card>
        </el-container>
      </el-dialog>
    </div>
    <div class="text-center">
      <el-dialog :visible.sync="dialogMove" width="500" title="Team Management">
        <el-container class="fixed-top">
          <el-card class="mx-auto" max-width="500">
            <div slot="header" style="color: #25c9d0">
              <h3>Moving member</h3>
            </div>
            <div class="col-sm-12 ml-2">
              <div class="text-center m-2">Please choose new team:</div>
              <el-select v-model="newTeam" type="text" class="mb-2 mt-2">
                <el-option
                  v-for="team in newTeams"
                  :key="team.id"
                  :label="team.team_name"
                  placeholder="Teams"
                  :value="team.id"
                ></el-option>
              </el-select>
            </div>
            <el-button type="danger" @click="closeDialogMove()"
              >Cancel</el-button
            >
            <el-button type="primary" @click="move()">Confirm</el-button>
          </el-card>
        </el-container>
      </el-dialog>
    </div>
    <div class="text-center">
      <el-dialog :visible.sync="dialogLead" width="500" title="Team Management">
        <el-container class="fixed-top">
          <el-card class="mx-auto" max-width="500">
            <div slot="header" style="color: #25c9d0">
              <h3>Set Leader</h3>
            </div>
            <div class="d-block text-center mb-4">
              Do you want to set
              <p class="text-danger d-inline">{{ selectedUser.name }}</p>
              as leader?
            </div>
            <el-button type="danger" @click="hideModalLead()">Cancel</el-button>
            <el-button type="primary" @click="lead()">Confirm</el-button>
          </el-card>
        </el-container>
      </el-dialog>
      <el-dialog title="Confirm" :visible.sync="isConfirming" width="30%">
        <span>Do you want to save this change?</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="closeDialogConfirm">Cancel</el-button>
          <el-button type="primary" @click="saveData">Save</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import TeamServices from "@/services/team/team.services.js";
import officeServices from "@/services/office/office.service";
import departmentServices from "@/services/office/department.service";
import groupServices from "@/services/office/group.service";
import { mapGetters } from "vuex";
import UserService from "@/services/user/user";
const { validateEmail } = require("../../../utils/validation");
const NO_DATA = "No data";
export default {
  name: "id_team_table",
  middleware: "authentication",
  data() {
    return {
      rules: {
        team_name: [
          {
            required: true,
            trigger: ["blur", "change"],
            validator: (_rule, value, callback, _source, _options) => {
              if (value.trim().length === 0) {
                callback(new Error("Team name is required"));
              } else if (value.trim().length > 100 || value.trim().length < 3) {
                callback(
                  new Error("Team name  must be between 3 and 100 characters")
                );
              }
              callback();
            },
          },
        ],
        team_email: [
          {
            trigger: ["blur", "change"],
            validator: (rule, value, callback, source, options) => {
              if (value.trim().length === 0) {
                callback();
              } else if (!validateEmail(value)) {
                callback(new Error("Team email is Invalid"));
              }
              callback();
            },
          },
        ],
        team_leader: [
          {
            required: true,
            message: "Please select Team leader!",
            trigger: "blur",
          },
        ],
      },
      teamData: {
        team_name: null,
      },
      teamMembers: [],
      searchByNameOrTeam: "Team",
      NO_DATA,
      isEditing: false,
      isConfirming: false,
      dialog: false,
      dialogLead: false,
      dialogMove: false,
      show: true,
      memberEmail: "",
      memberRows: [],
      teamId: "",
      teamLeader: null,
      offices: [],
      departments: [],
      groups: [],
      allTeamsExcludeCurrentTeam: [],
      selectedUser: "",
      admin: localStorage.getItem("is_admin"),
      user_id: localStorage.getItem("user_id"),
      borderRadius: {
        borderradius: "1.25rem",
        textAlign: "center",
        width: "100%",
      },
      color: {
        color: "#25c9d0",
        fontSize: "40px",
      },
      colorEmail: {
        color: "#25c9d0",
        fontSize: "16px",
      },
      text: {
        fontSize: "20px",
      },
      errors: "",
      newTeams: [],
      newTeam: "",

      //my code
      team: {},
      members: [],
      pms: [],
      currentPM: {},
      filteredUsers: [],
      showButton: true,
    };
  },

  computed: {
    ...mapGetters({
      tokenInfo: "scope/tokenInfo",
    }),
  },
  methods: {
    handleClassRequired() {
      let elements = document.querySelectorAll(".re");
      if (this.isEditing) {
        elements.forEach((e) => e.classList.add("required"));
      } else {
        elements.forEach((e) => e.classList.remove("required"));
      }
    },
    async getData() {
      this.teamId = this.$route.params.id;
      const response = await TeamServices.get(`${this.teamId}`);
      if (response && response.status === 200) {
        this.teamData = response.data;
        this.teamLeader = this.teamData.team_leader;
        this.members = this.teamData.employee_list;
      }
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.isConfirming = true;
        } else {
          this.$toast.error("Input is invalid!");
          return false;
        }
      });
    },
    listMembersTeam() {
      this.teamMembers = [];
      let allMembers = this.filteredUsers;
      let teamSuggest = this.teamData;
      let allTeamsExcludeSuggestTeam = this.allTeamsExcludeCurrentTeam;

      let groupNoneTeam = {
        team: {
          team: "Other",
        },
        members: [],
      };

      let groupSuggestTeam = {
        team: {
          team: teamSuggest.team_name,
        },
        members: [],
      };

      for (let team of allTeamsExcludeSuggestTeam) {
        let groupTeam = {
          team: {
            team: team.team_name,
          },
          members: [],
        };

        for (let member of allMembers) {
          if (member.profile.teams.length <= 0) {
            groupNoneTeam.members.push(member);
            allMembers.splice(allMembers.indexOf(member), 1);
          }
          if (
            member.profile.teams.some(
              (items) => items.name === teamSuggest.team_name
            )
          ) {
            if (!groupSuggestTeam.members.includes(member)) {
              groupSuggestTeam.members.push(member);
            }
          }
          if (
            member.profile.teams.some((items) => items.name === team.team_name)
          ) {
            groupTeam.members.push(member);
          }
        }
        this.teamMembers.push(groupTeam);
      }

      this.teamMembers.unshift(groupSuggestTeam);
      this.teamMembers.push(groupNoneTeam);
      this.filteredUsers = this.teamMembers;
    },

    remoteMethod(query) {
      const keyword = query.toLowerCase();

      if (this.searchByNameOrTeam === "Team") {
        this.filteredUsers = this.teamMembers.filter((item) => {
          return item.team.team.toLowerCase().includes(keyword);
        });
      } else {
        this.filteredUsers = this.teamMembers.map((item) => {
          return {
            team: item.team,
            members: item.members.filter((member) => {
              return member.profile.name.toLowerCase().includes(keyword);
            }),
          };
        });
      }
    },
    async saveData() {
      this.teamData.current_leader = this.teamLeader;
      await TeamServices.update(this.teamId, this.teamData)
        .then((res) => {
          if (res.status === 200) {
            this.$toast.success("Updated Successfully");
          }
          this.closeDialogConfirm();
        })
        .catch(() => {
          this.$toast.error("Updated Failed");
          this.isConfirming = false;
        });
      this.handleClassRequired();
    },
    closeDialogConfirm() {
      this.getData();
      this.isConfirming = false;
      this.isEditing = false;
    },
    editTeam() {
      this.isEditing = true;
      this.teamData.group = this.teamData.group ? this.teamData.group.id : null;
      this.teamData.department = this.teamData.department
        ? this.teamData.department.id
        : null;
      this.teamData.office = this.teamData.office
        ? this.teamData.office.id
        : null;
      this.errors = "";
      this.handleClassRequired();
    },
    cancel: function () {
      this.errors = "";
      this.show = !this.show;
    },
    showModal(user) {
      this.selectedUser = user;
      this.dialog = true;
      this.errors = "";
    },
    closeDialog() {
      this.selectedUser = "";
      this.dialog = false;
    },
    async showMoveTeamModal(user) {
      this.dialogMove = true;
      let response = await TeamServices.getNewTeams(user.user);
      this.newTeams = response.data;
      this.errors = "";
      this.selectedUser = user;
    },
    hideModal() {
      this.$refs.mymodal.hide();
    },
    showModalLead(user) {
      this.selectedUser = user;
      this.dialogLead = true;
    },
    hideModalLead() {
      this.selectedUser = false;
      this.dialogLead = false;
    },
    async lead() {
      const formData = new FormData();
      const teamId = this.$route.params.id;
      this.show = true;
      this.errors = "";
      formData.append("email", this.selectedUser.email);
      let response = await TeamServices.setLeader(teamId, formData);
      if (response.data && response.data.Success) {
        this.$toast.success("Success");
        await this.getData();
      } else {
        this.$toast.error("Error");
      }
      this.selectedUser = "";
      this.dialogLead = false;
    },
    async del() {
      const formData = new FormData();
      this.errors = "";
      formData.append("email", this.selectedUser.email);
      let response = await TeamServices.removeMember(
        this.$route.params.id,
        formData
      );
      if (response.data && response.data.Success) {
        this.members.splice(this.members.indexOf(this.selectedUser), 1);
        this.$toast.success("Deleted Successfully");
      } else {
        this.$toast.error("Delete Failed");
      }
      this.selectedUser = "";
      this.dialog = false;
    },
    async move() {
      const formData = new FormData();
      formData.append("current_team_id", this.$route.params.id);
      formData.append("user_id", this.selectedUser.user);
      formData.append("new_team_id", this.newTeam);
      let response = await TeamServices.moveTeam(formData);
      if (response.data && response.data.Success) {
        this.members.splice(this.members.indexOf(this.selectedUser), 1);
        this.$toast.success("Moved Success");
      } else {
        this.$toast.error("Move Failed");
      }
      this.dialogMove = false;
    },
    closeDialogMove() {
      this.dialogMove = false;
      this.selectedUser = "";
    },
    async getTeams() {
      const res = await TeamServices.getAll();
      this.allTeamsExcludeCurrentTeam = res.data;
      this.allTeamsExcludeCurrentTeam.splice(
        this.allTeamsExcludeCurrentTeam.findIndex(
          (team) => team.id === this.teamData.id
        ),
        1
      );
    },
    async getOffices() {
      const res = await officeServices.getOffices();
      this.offices = res.data.results;
    },
    async getGroups() {
      const res = await groupServices.getAll();
      this.groups = res.data;
    },
    async getDepartments() {
      const res = await departmentServices.getAll();
      this.departments = res.data;
    },
    async getAllUsers() {
      const res = await UserService.getAllEmployees();
      this.filteredUsers = res.data;
    },
    hasScope(scope) {
      return this.tokenInfo["scope"].indexOf(scope) !== -1;
    },
  },

  async created() {
    await this.getData();
    await this.getAllUsers();
    await this.getTeams();
    await this.getOffices();
    await this.getGroups();
    await this.getDepartments();
    this.listMembersTeam();
  },
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
