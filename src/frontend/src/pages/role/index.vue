<template>
  <div>
    <div class="row my-2">
      <div class="col-10 col-md-4">
        <el-input
          label="Search"
          v-model="roleName"
          placeholder="Search role"
          @change="search()"
          maxlength="100"
          clearable
        ></el-input>
      </div>
      <restricted-view
        :scopes="['role:edit']"
        style="order: 1"
        class="col-10 col-md-8"
      >
        <template v-slot:default>
          <div style="float: right">
            <el-button
              type="primary"
              icon="el-icon-circle-plus"
              @click="handelClickAdd"
              style="width: 200px"
            >
              Add Role
            </el-button>
          </div>
        </template>
      </restricted-view>
    </div>

    <el-table
      :data="roleList.rows"
      stripe
      header-cell-class-name="bg-header-table"
      style="width: 100%"
    >
      <el-table-column prop="name" label="Role" width="260" align="center">
        <template v-slot:default="table">
          <span>{{ table.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="description" align="center" label="Description">
        <template v-slot:default="table">
          <span style="word-break: break-word">{{
            table.row.description
          }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="last_modified_by"
        label="Last modified by"
        align="center"
        width="260"
      >
        <template v-slot:default="table">
          <span>{{ table.row.last_modified_by }}</span>
        </template>
      </el-table-column>
      <el-table-column
        fixed="right"
        label="Operations"
        align="center"
        width="260"
      >
        <template v-slot:default="table">
          <el-button
            circle
            style="cursor: pointer"
            @click="
              handleViewRole(
                table.row.id,
                table.row.description,
                table.row.name
              )
            "
            type="info"
            icon="el-icon-info"
            title="View"
          ></el-button>
          <restricted-view :scopes="['role:edit']">
            <template v-slot:default>
              <el-button
                circle
                style="cursor: pointer"
                @click="
                  handleUpdateRole(
                    table.row.id,
                    table.row.description,
                    table.row.name
                  )
                "
                type="primary"
                icon="el-icon-edit"
                title="Edit"
              ></el-button>
            </template>
          </restricted-view>
          <restricted-view :scope="['role:edit']">
            <template v-slot:default>
              <el-button
                circle
                style="cursor: pointer"
                type="danger"
                icon="el-icon-delete"
                @click="handleClickDeleteRole(table.row.id)"
                title="Delete"
              />
            </template>
          </restricted-view>
        </template>
      </el-table-column>
    </el-table>

    <div class="d-flex justify-content-center mt-5">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="roleList.page_size"
        :page-count="roleList.totalPage"
        :total="roleList.count"
        :current-page="roleList.currentPage"
        @current-change="setPage"
      >
      </el-pagination>
    </div>

    <div style="overflow: hidden">
      <el-dialog :visible.sync="dialogAdd" top="-5vh">
        <Dialog
          ref="Dialog"
          :roleListData="roleList"
          @handleData="handleData"
        ></Dialog>
      </el-dialog>
    </div>

    <el-dialog
      title="Delete"
      :visible.sync="dialogDelete"
      width="30%"
      class="dialog"
    >
      <span>Do you want to delete this template</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogDelete = false">Cancel</el-button>
        <el-button type="primary" @click="deleteRole()">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import "vue2-datepicker/index.css";
import Dialog from "./Dialog";
import { mapActions, mapGetters } from "vuex";
import RoleService from "@/services/role/role_service";
import RestrictedView from "@/components/RestrictedView";

export default {
  components: {
    Dialog,
    RestrictedView,
  },
  name: "ManageRole",
  middleware: "authentication",
  computed: {
    ...mapGetters({
      roleList: "role/roleList",
    }),
  },
  watch: {
    roleName: function () {
      this.search(1);
    },
  },
  data() {
    return {
      roleName: "",
      dialogAdd: false,
      page_size: 8,
      page: 1,
      dialogDelete: false,
      deleteId: "",
    };
  },

  async created() {
    await this.search(1);
  },

  methods: {
    ...mapActions({
      getRoleList: "role/getRoleList",
    }),

    async setPage(page) {
      this.page = page;
      await this.search(this.page);
    },

    async search(page = this.page) {
      await this.getRoleList({
        page_size: this.roleList.page_size,
        page: page,
        name: this.roleName,
      });
    },

    async handleViewRole(id, description, name) {
      this.dialogAdd = true;
      await RoleService.getRole(id).then((res) => {
        this.$nextTick(function () {
          this.$refs.Dialog.setChecked(res.data.scope.split(" "));
          this.$refs.Dialog.currentRole = { id, description, name };
          this.$refs.Dialog.mode = "view";
          this.$refs.Dialog.validate = false;
          this.$refs.Dialog.viewMode = true;
        });
      });
    },

    async handleUpdateRole(id, description, name) {
      this.dialogAdd = true;
      await RoleService.getRole(id).then((res) => {
        this.$nextTick(function () {
          this.$refs.Dialog.setChecked(res.data.scope.split(" "));
          this.$refs.Dialog.currentRole = { id, description, name };
          this.$refs.Dialog.mode = "update";
          this.$refs.Dialog.validate = false;
          this.$refs.Dialog.selectAll = false;
          this.$refs.Dialog.viewMode = false;
        });
      });
    },

    handelClickAdd() {
      this.title = "Create Role";
      this.dialogAdd = true;
      this.$nextTick(function () {
        this.$refs.Dialog.setDefaultCheckedKeys();
        this.$refs.Dialog.mode = "create";
        this.$refs.Dialog.validate = false;
        this.$refs.Dialog.selectAll = false;
        this.$refs.Dialog.viewMode = false;
      });
    },

    handleClickDeleteRole(role_id) {
      this.dialogDelete = true;
      this.deleteId = role_id;
    },

    deleteRole() {
      RoleService.deleteRole(this.deleteId)
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
          this.search();
          this.dialogDelete = false;
        });
    },

    handleData(visible) {
      this.dialogAdd = visible;
      this.search();
    },
  },
};
</script>
<style lang="scss" scoped>
@import "index";

.el-dialog__wrapper {
  overflow: hidden;
  margin-top: 10vh;
}

.modal-active {
  display: block;
}

.img-fluid {
  width: 60px;
}
</style>
