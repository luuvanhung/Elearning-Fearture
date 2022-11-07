<template>
  <restricted-view :scopes="['application:list', 'application:create']">
    <template v-slot:default>
      <div class="my-2 ma-auto main-content">
        <div class="bg-light">
          <restricted-view :scope="['application:create']">
            <template v-slot:default>
              <!-- BUTTON CREATE APPLICATION -->
              <div class="justify-xl-end d-flex justify-content-end">
                <el-button
                  class="btn_add"
                  plain
                  icon="el-icon-plus"
                  @click="showCreateAppDialog"
                >
                  <span class="ml-2">Create Application</span></el-button
                >
              </div>
            </template>
          </restricted-view>

          <restricted-view :scope="['application:list']">
            <template v-slot:default>
              <!-- TABLE APPLICATION  -->
              <el-table
                header-cell-class-name="bg-header-table"
                style="width: 100%"
                class="mt-2"
                stripe
                border
                :data="listAppData.rows"
              >
                <el-table-column prop="name" label="Name App"></el-table-column>
                <el-table-column prop="client_id" label="Client ID">
                </el-table-column>
                <restricted-view
                  :scopes="['application:update', 'application:retrieve']"
                >
                  <template v-slot:default>
                    <el-table-column
                      label="Action"
                      width="150"
                      fixed="right"
                      align="center"
                    >
                      <!-- BUTTON EDIT APPLICATION  -->
                      <template v-slot="scope">
                        <el-button
                          circle
                          style="cursor: pointer"
                          @click="handleEditApp(scope.row)"
                          type="primary"
                          icon="el-icon-edit"
                        ></el-button>
                        <el-button
                          circle
                          style="cursor: pointer"
                          type="danger"
                          icon="el-icon-delete"
                          @click="handleDeleteApp(scope.row.client_id)"
                        />
                      </template>
                    </el-table-column>
                  </template>
                </restricted-view>
              </el-table>

              <!-- PAGINATION  -->
              <div class="d-flex justify-content-center mt-5">
                <el-pagination
                  background
                  layout="prev, pager, next"
                  :page-size="pageSize"
                  :page-count="listAppData.totalPage"
                  :current-page="listAppData.currentPage"
                  :total="listAppData.count"
                  @current-change="setPage"
                >
                </el-pagination>
              </div>
            </template>
          </restricted-view>
        </div>
        <div style="overflow: hidden">
          <!-- DIALOG CREATE APP -->
          <el-dialog
            :model="createItem"
            :visible.sync="createDialog"
            append-to-body
          >
            <div class="d-block text-center text-danger mb-4">
              <h3>Create Application</h3>
            </div>
            <el-form label-width="120px" :rules="rules" :model="createItem">
              <el-form-item label="Name" prop="name">
                <el-input v-model="createItem.name"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  @click="createSubmit"
                  :disabled="$v.createItem.$invalid"
                >
                  Create
                </el-button>
              </el-form-item>
            </el-form>
          </el-dialog>

          <!-- DIALOG UPDATE -->
          <el-dialog
            top="-5vh"
            :model="appUpdate"
            :visible.sync="updateDialog"
            append-to-body
          >
            <div style="max-height: 78vh; overflow-y: auto; overflow-x: hidden">
              <el-form label-width="200px" rules="rules">
                <el-form-item label="Name*" props="name">
                  <el-input v-model="appUpdate.name"></el-input>
                  <div class="error" v-if="!$v.appUpdate.name.required">
                    Field is required
                  </div>
                </el-form-item>
                <el-form-item label="Client Secret*">
                  <el-input
                    v-model="appUpdate.client_secret"
                    disabled
                  ></el-input>
                </el-form-item>
                <el-form-item label="Client Type*">
                  <el-input v-model="appUpdate.client_type"></el-input>
                  <div class="error" v-if="!$v.appUpdate.client_type.required">
                    Field is required
                  </div>
                </el-form-item>
                <el-form-item label="Authorization Grant Type*">
                  <el-input
                    v-model="appUpdate.authorization_grant_type"
                  ></el-input>
                  <div
                    class="error"
                    v-if="!$v.appUpdate.authorization_grant_type.required"
                  >
                    Field is required
                  </div>
                </el-form-item>
                <el-form-item label="User">
                  <el-input v-model="appUpdate.user"></el-input>
                </el-form-item>
                <el-form-item label="Redirect URI">
                  <el-input v-model="appUpdate.redirect_uris"></el-input>
                </el-form-item>
                <el-form-item label="Algorithm">
                  <el-input v-model="appUpdate.algorithm"></el-input>
                </el-form-item>
                <el-form-item label="Skip Authorization">
                  <el-checkbox
                    v-model="appUpdate.skip_authorization"
                  ></el-checkbox>
                </el-form-item>
                <restricted-view :scopes="['application:update']">
                  <template v-slot:default>
                    <!-- BUTTON CHOOSE SCOPES -->
                    <el-form-item label="Scopes">
                      <ScopesSelector
                        ref="appSelectScopes"
                        :scopes="allScopeConst"
                        :selectedScopes="appUpdate.scope"
                        @handleUpdateScopes="handleUpdateScopes"
                      />
                    </el-form-item>
                    <!-- COMPONENT API KEY -->
                    <APIKey
                      :allScopeConst="allScopeConst"
                      :currApp="appUpdate"
                    />
                    <el-form-item>
                      <el-button
                        type="primary"
                        :disabled="$v.appUpdate.$invalid"
                        @click="handleUpdateApp"
                      >
                        Update
                      </el-button>
                      <el-button type="danger" @click="hideDialogUpdateApp">
                        Close
                      </el-button>
                    </el-form-item>
                  </template>
                </restricted-view>
              </el-form>
            </div>
          </el-dialog>
          <!-- DIALOG DELETE -->
          <el-dialog
            title="Delete"
            :visible.sync="dialogDelete"
            width="30%"
            class="dialog"
          >
            <span>Do you want to delete this template ?</span>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogDelete = false">Cancel</el-button>
              <el-button type="primary" @click="deleteApp()">Confirm</el-button>
            </span>
          </el-dialog>
        </div>
      </div>
    </template>
  </restricted-view>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import Application from "@/services/application/application.service";
import ScopeService from "@/services/role/scope_service";
import RestrictedView from "@/components/RestrictedView";
import ScopesSelector from "./ScopesSelector.vue";
import APIKey from "./APIKey/index.vue";

export default {
  name: "IntegratedApplication",
  middleware: "authentication",
  components: {
    RestrictedView,
    ScopesSelector,
    APIKey,
  },
  data() {
    return {
      listAppData: {
        rows: [],
        totalPage: 1,
        currentPage: 1,
        count: 0,
      },
      allScopeConst: {},
      appUpdate: {
        id: "",
        client_id: "",
        name: "",
        client_secret: "",
        client_type: "",
        authorization_grant_type: "",
        user: "",
        redirect_uris: "",
        algorithm: "",
        skip_authorization: false,
        scope: [],
      },
      createItem: {
        name: "",
        client_type: "confidential",
        authorization_grant_type: "password",
      },
      createDialog: false,
      updateDialog: false,
      titleDialog: "",
      pageSize: 8,
      page: 1,
      dialogDelete: false,
      deleteId: "",
      rules: {
        name: [
          {
            required: true,
            message: "Please input Application name",
            trigger: "blur",
          },
          {
            min: 1,
            max: 100,
            message: "Length should be 1 to 100",
            trigger: "blur",
          },
        ],
      },
    };
  },
  validations: {
    appUpdate: {
      name: { required },
      client_type: { required },
      authorization_grant_type: { required },
    },
    createItem: {
      name: { required },
    },
  },
  async mounted() {
    await this.getAllScope();
    await this.getListApp();
  },
  methods: {
    async setPage(page) {
      this.page = page;
      await this.getListApp();
    },
    async getAllScope() {
      let res = await ScopeService.getScopes();
      if (res && res.status === 200) this.allScopeConst = res.data.scope;
    },
    async getListApp() {
      const res = await Application.getListApp(this.page, this.pageSize);
      if (res && res.status === 200) {
        this.listAppData.rows = [];
        this.listAppData.count = res.data.count;
        this.listAppData.currentPage = res.data.current;
        this.listAppData.totalPage = res.data.page_number;
        const apps = res.data.results;
        if (!apps) return;

        apps.forEach((app) => {
          if (app.scope === "__all__") app.scope = this.allScopeConst.arr;
          else app.scope = app.scope.split(" ");
        });
        this.listAppData.rows = apps;
      }
    },
    showCreateAppDialog() {
      this.createDialog = true;
    },
    async createSubmit() {
      try {
        const res = await Application.addNewApp(this.createItem);
        await this.getListApp();
        this.$toast.success("Created Successfully");
        this.createItem.name = "";
        this.createDialog = false;
      } catch (e) {
        this.$toast.error("Create Failed");
      }
    },
    async handleEditApp(app) {
      this.showDialogUpdateApp();
      app.scope = await this.getAppScopesByClientId(app.client_id);
      this.appUpdate = { ...app };
      this.resetAppSelectScopes();
    },
    resetAppSelectScopes() {
      let selectScopes = this.getComponent("appSelectScopes");
      selectScopes.reset_all = false;
      selectScopes.select_all = false;
      selectScopes.resetCollapse();
    },
    async handleUpdateApp() {
      try {
        const data = {
          name: this.appUpdate.name,
          client_type: this.appUpdate.client_type,
          authorization_grant_type: this.appUpdate.authorization_grant_type,
          user: this.appUpdate.user,
          redirect_uris: this.appUpdate.redirect_uris,
          algorithm: this.appUpdate.algorithm,
          skip_authorization: this.appUpdate.skip_authorization,
          scope: this.strAppUpdateScopes,
        };
        await Application.editApp(this.appUpdate.client_id, data).then(
          (res) => {
            if (res.status !== 200) return;
            this.getListApp();
            this.$toast.success("Updated Successfully");
            this.hideDialogUpdateApp();
          }
        );
      } catch (e) {
        this.$toast.error("Update Failed");
      }
    },
    handleDeleteApp(client_id) {
      this.dialogDelete = true;
      this.deleteId = client_id;
    },
    deleteApp() {
      Application.deleteApp(this.deleteId)
        .then((res) => {
          if (res.status === 204) {
            this.$toast.success("Deleted Successfully");
          } else {
            this.$toast.error("Delete Failed");
          }
        })
        .catch(() => {
          this.$toast.error("An error occurred");
        })
        .then(() => {
          this.getListApp();
          this.dialogDelete = false;
        });
    },
    showDialogUpdateApp() {
      this.updateDialog = true;
    },
    hideDialogUpdateApp() {
      this.updateDialog = false;
    },
    async getAppScopesByClientId(client_id) {
      const res = await Application.getApplicationScopes(client_id);
      if (res && res.status === 200) return res.data.scope.split(" ");

      return [];
    },
    getComponent(name) {
      return this.$refs[name];
    },
    handleUpdateScopes(scopes) {
      this.appUpdate.scope = scopes;
    },
  },
  computed: {
    strAppUpdateScopes() {
      return this.appUpdate.scope.join(" ");
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
.el-dialog__wrapper {
  overflow: hidden;
  margin-top: 10vh;
}
</style>
