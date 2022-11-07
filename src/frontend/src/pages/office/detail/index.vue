<template>
  <div>
    <div class="my-4">
      <div class="row">
        <div class="col-12">
          <div class="border-title p-2">
            <div class="col-12 col-sm-5 col-md-3 col-xl-2">
              <div class="bg-logo">
                <img
                  src="@/static/images/symbol.png"
                  alt="Logo Company"
                  class="logo-image"
                />
              </div>
            </div>
            <div
              class="col-12 col-sm-7 col-md-9 col-xl-10 d-flex align-items-center"
            >
              <h1>{{ data.name }}</h1>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-card class="box-card mb-4 card-detail">
      <div slot="header" class="clearfix">
        <span class="card-title">General Profile</span>
        <el-button
          class="edit-button"
          type="text"
          @click="showEditForm"
          v-if="!generalInfo.isShowForm"
        >
          <restricted-view :scopes="['office:edit']">
            <template v-slot:default>
              <img
                :src="require('@/static/images/IconCardEdit.svg')"
                class="edit-icon"
              />
            </template>
          </restricted-view>
        </el-button>
        <el-button class="edit-button" type="text" @click="saveForm" v-else>
          <img
            :src="require('@/static/images/IconCardSave.svg')"
            class="edit-icon"
          />
        </el-button>
      </div>
      <div class="text item">
        <div class="row">
          <div class="col-5 col-xl-2 my-2">Name:</div>
          <div class="col-7 col-xl-10 text-dark my-2">
            <div v-if="!generalInfo.isShowForm">
              {{ data.name }}
            </div>
            <el-input
              v-else
              placeholder="Please input"
              size="small"
              v-model="data.name"
              required
            >
            </el-input>
          </div>
          <div class="col-5 col-xl-2 my-2">Established date:</div>
          <div class="col-7 col-xl-10 text-dark my-2">
            <div v-if="!generalInfo.isShowForm">
              {{ data.established_date }}
            </div>
            <el-date-picker
              v-else
              size="small"
              placeholder="Please input"
              v-model="data.established_date"
              type="date"
              value-format="yyyy-MM-dd"
            >
            </el-date-picker>
          </div>
          <div class="col-5 col-xl-2 my-2">Manager:</div>
          <div class="col-7 col-xl-10 text-dark my-2">
            <div v-if="!generalInfo.isShowForm">
              {{ managerName }}
            </div>
            <el-select
              v-else
              v-model="data.manager"
              placeholder="Select Manager"
              size="mini"
              required
            >
              <el-option
                v-for="item in usersList"
                :key="item.id"
                :label="item.user_name + ' - ' + item.user_title"
                :value="item.id"
              >
              </el-option>
            </el-select>
          </div>
          <div class="col-5 col-xl-2 my-2">Email:</div>
          <div class="col-7 col-xl-10 text-dark my-2">
            <div v-if="!generalInfo.isShowForm">
              {{ data.email }}
            </div>
            <el-input
              v-else
              placeholder="Please input"
              size="small"
              v-model="data.email"
            >
            </el-input>
          </div>
          <div class="col-5 col-xl-2 my-2">Address:</div>
          <div class="col-7 col-xl-10 text-dark my-2">
            <div v-if="!generalInfo.isShowForm">
              {{ data.address }}
            </div>
            <el-input
              v-else
              placeholder="Please input"
              size="small"
              v-model="data.address"
            >
            </el-input>
          </div>
          <div class="col-5 col-xl-2 my-2">Phone:</div>
          <div class="col-7 col-xl-10 text-dark my-2">
            <div v-if="!generalInfo.isShowForm">
              {{ data.phone }}
            </div>
            <el-input
              v-else
              placeholder="Please input"
              size="small"
              v-model="data.phone"
            >
            </el-input>
          </div>
        </div>
      </div>
    </el-card>
    <el-card class="box-card card-detail mb-4">
      <div slot="header" class="clearfix">
        <span class="card-title">Holidays</span>
      </div>
      <div class="text item">
        <holiday />
      </div>
    </el-card>
    <el-card class="box-card card-detail mb-4">
      <div slot="header" class="clearfix">
        <span class="card-title">Sessions</span>
        <el-button
          class="edit-button"
          type="text"
          @click="showEditForm"
          v-if="!generalInfo.isShowForm"
        >
          <restricted-view :scopes="['office:edit']">
            <template v-slot:default>
              <img
                :src="require('@/static/images/IconCardEdit.svg')"
                class="edit-icon"
              />
            </template>
          </restricted-view>
        </el-button>
        <el-button class="edit-button" type="text" @click="saveForm" v-else>
          <img
            :src="require('@/static/images/IconCardSave.svg')"
            class="edit-icon"
          />
        </el-button>
      </div>
      <div class="text item">
        <session :showAddSession="!generalInfo.isShowForm"></session>
      </div>
    </el-card>
    <el-dialog title="Confirm" :visible.sync="updatedConfirm" width="30%">
      <span>Do you want to save this change?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancel">Cancel</el-button>
        <el-button type="primary" @click="saveData">Save</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import officeService from "@/services/office/office.service.js";
import userService from "@/services/user/user.js";
import message from "@/services/office/responseMessage.js";
import holiday from "@/pages/office/holiday/index.vue";
import session from "../session/index";
import RestrictedView from "@/components/RestrictedView";

export default {
  middleware: "authentication",
  components: {
    holiday,
    session,
    RestrictedView,
  },
  data() {
    return {
      usersList: [],
      data: "",
      updatedConfirm: false,
      generalInfo: {
        isShowForm: false,
        isSaveComfirm: false,
      },
    };
  },
  methods: {
    showEditForm() {
      this.generalInfo.isShowForm = true;
    },
    saveForm() {
      this.updatedConfirm = true;
      this.generalInfo.isSaveComfirm = true;
    },
    cancel() {
      this.updatedConfirm = false;
      this.generalInfo.isSaveComfirm = false;
    },
    async saveData() {
      try {
        const dataForm = new FormData();
        dataForm.append("name", this.data.name);
        dataForm.append("manager", this.data.manager);
        if (!this.data.name || !this.data.manager) {
          return this.$toast.error(message.VALIDATION);
        }

        if (this.generalInfo.isSaveComfirm) {
          dataForm.append("established_date", this.data.established_date);
          dataForm.append("email", this.data.email);
          dataForm.append("address", this.data.address);
          dataForm.append("phone", this.data.phone);

          this.generalInfo.isShowForm = false;
          this.generalInfo.isSaveComfirm = false;
        }
        const responeData = await officeService.editAllFiledOffice(
          dataForm,
          this.$route.params.id
        );

        if (responeData.status == 200) {
          this.updatedConfirm = false;
          this.$toast.success("Updated Successfully");
        }
      } catch (error) {
        this.updatedConfirm = false;
        let errorContent =
          error.response.status == 400 && error.response.data
            ? error.response.data
            : "Update Failed";
        this.$toast.error(errorContent);
      }
    },
    async getData() {
      let usersListData = await userService.getUsersIncludeNameAndTitle();
      this.usersList = usersListData.data;

      let responseData = await officeService.getDetailOffice(
        this.$route.params.id
      );
      this.data = responseData.data;
    },
  },
  async created() {
    return this.getData();
  },
  computed: {
    managerName() {
      let managerData = this.usersList.find((d) => d.id === this.data?.manager);
      return managerData?.user_name;
    },
  },
};
</script>
<style lang="scss" scope>
@import "index.scss";
</style>
