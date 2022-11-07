<template>
  <div class="d-flex justify-content-center">
    <div class="table-responsive p-3 col-md-7">
      <el-form
        label-width="120px"
        :model="formData"
        :rules="rules"
        ref="formData"
      >
        <el-form-item label="Team Name" prop="team_name">
          <el-input v-model="formData.team_name" placeholder="Team Name" />
        </el-form-item>
        <el-form-item label="Team Email" prop="team_email">
          <el-input v-model="formData.team_email" placeholder="Email" />
        </el-form-item>
        <el-form-item label="Team Leader" prop="team_leader">
          <el-select
            v-model="formData.team_leader"
            filterable
            placeholder="Team Leader"
          >
            <el-option
              v-for="user in filteredUsers"
              :value="user.email"
              :key="user.id"
              :label="user.profile.name"
            >
              <span style="float: left">{{ user.profile.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">{{
                user.email
              }}</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Office">
          <div>
            <el-select v-model="formData.office" placeholder="Office">
              <el-option
                v-for="office in offices"
                :label="office.name"
                :value="office.id"
                :key="office.id"
              ></el-option>
            </el-select>
          </div>
        </el-form-item>
        <el-form-item label="Slack Channel">
          <el-input
            v-model="formData.slack_channel"
            placeholder="Team Slack Channel"
          />
        </el-form-item>
        <br />
        <el-form-item>
          <el-button type="primary" @click="submit('formData')"
            >Create</el-button
          >
          <router-link to="/teams" class="ml-3">
            <el-button type="danger">Cancel</el-button>
          </router-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
import TeamService from "@/services/team/team.services";
import officeServices from "@/services/office/office.service";
import { mapGetters } from "vuex";
import { validateEmail } from "@/utils/validation";

export default {
  name: "CreateTeam",
  middleware: "authentication",
  data() {
    return {
      formData: {
        team_name: "",
        team_email: "",
        team_leader: "",
        slack_channel: "",
        office: "",
      },
      offices: [],
      filteredUsers: [],
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
            validator: (rule, value, callback, source, options) => {
              if (value.trim().length === 0) {
                callback();
              } else if (!validateEmail(value)) {
                callback(new Error("Team email is Invalid"));
              }
              callback();
            },
            trigger: ["blur", "change"],
          },
        ],
        team_leader: [
          {
            required: true,
            message: "Please input team leader",
            trigger: "change",
          },
        ],
      },
    };
  },
  created() {
    this.getOffices();
    this.filteredUsers = this.allUsers;
  },
  computed: {
    ...mapGetters("user", ["allUsers"]),
  },
  methods: {
    submit(formData) {
      this.$refs[formData].validate(async (valid) => {
        if (valid) {
          try {
            const result = await TeamService.create(this.formData);
            if (result) {
              await this.$router.push("/teams");
              this.$toast.success("Added Successfully");
            } else {
              this.$toast.error("Add Failed");
            }
          } catch (error) {
            let errorContent = error.response.data.detail
              ? error.response.data.detail
              : "Add Failed";
            this.$toast.error(errorContent);
          }
        } else {
          return false;
        }
      });
    },

    async getOffices() {
      const res = await officeServices.getOffices();
      this.offices = res.data.results;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
