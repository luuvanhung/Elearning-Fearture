<template>
  <div style="max-height: 86vh; overflow-y: auto; overflow-x: hidden">
    <div class="d-flex justify-content-center" style="margin-top: 2%">
      <div class="col-12 col-sm-5">
        <el-input
          v-model="currentRole.name"
          placeholder="Enter role name"
          required
          maxlength="100"
          clearable
          :disabled="viewMode"
        ></el-input>
      </div>
      <div class="col-12 col-sm-5">
        <el-input
          v-model="currentRole.description"
          placeholder="Enter role description"
          required
          maxlength="256"
          clearable
          :disabled="viewMode"
        ></el-input>
      </div>
    </div>

    <div style="margin-top: 2%">
      <span style="color: red" v-show="validate">
        Please input valid field
      </span>
    </div>

    <div>
      <strong v-if="mode === 'view'">All permissions</strong>
      <strong v-else>Please choose permissions</strong>
    </div>

    <el-input
      style="margin-top: 1%"
      placeholder="Filter keyword"
      v-model="filterText"
    >
    </el-input>

    <div style="margin-top: 1%">
      <el-checkbox
        v-model="selectAll"
        @change="checkAll"
        border
        v-show="mode !== 'view'"
      >
        Select all
      </el-checkbox>
    </div>

    <div class="row">
      <div class="col-12 mt-3">
        <el-tree
          class="filter-tree"
          :data="scopeTree"
          :props="defaultProps"
          :show-checkbox="true"
          node-key="scope"
          :highlight-current="true"
          ref="tree"
          :filter-node-method="filterNode"
          @check-change="handleCheckChange"
          @check="handleClick"
        >
        </el-tree>
      </div>
    </div>
    <div class="footer-dialog d-flex justify-content-end mt-2">
      <el-button
        type="danger"
        @click="reset"
        style="margin-left: 2%"
        v-show="mode !== 'view'"
      >
        Reset
      </el-button>
      <el-button
        type="primary"
        @click="handleClickCreateRole"
        style="margin-left: 2%"
        v-show="mode === 'create'"
      >
        Create
      </el-button>
      <restricted-view :scope="['role:edit']">
        <el-button
          type="primary"
          @click="handleClickUpdateRole"
          style="margin-left: 24px"
          v-show="mode === 'update'"
        >
          Update
        </el-button>
      </restricted-view>
    </div>
  </div>
</template>
<script>
import ScopeService from "@/services/role/scope_service";
import RoleService from "@/services/role/role_service";
import { mapActions } from "vuex";
import RestrictedView from "@/components/RestrictedView";
import { DEFAULT_SCOPES } from "@/const/default-scopes";

export default {
  name: "Dialog",
  middleware: "authentication",
  components: { RestrictedView },
  props: ["roleListData"],

  async created() {
    await this.getAddedData();
    this.currentRole.scope = DEFAULT_SCOPES.join(" ");
  },

  data() {
    return {
      filterText: "",
      validate: false,
      mode: "",
      defaultProps: {
        children: "children",
        label: "label",
        disabled: "disabled",
      },
      currentRole: {
        id: "",
        name: "",
        description: "",
        scope: "",
      },
      errors: "",
      scopeTree: [],
      page_size: 8,
      fullScope: [],
      selectAll: false,
      viewMode: false,
    };
  },

  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },

  methods: {
    ...mapActions({
      getRoleList: "role/getRoleList",
    }),

    filterNode(value, data) {
      if (!value) return true;
      return data.label.toLowerCase().includes(value.toLowerCase());
    },

    checkAll() {
      if (this.selectAll) {
        this.setChecked(this.fullScope);
      } else {
        this.$refs.tree.setCheckedKeys(DEFAULT_SCOPES);
      }
    },

    reset() {
      this.$refs.tree.setCheckedKeys(DEFAULT_SCOPES);
      this.selectAll = false;
    },

    handleClick() {
      if (this.mode === "view")
        this.$toast.error("You chose view,so you only view!!!");
    },

    setChecked(checkedList = []) {
      if (!checkedList.length) {
        this.clearForm();
      }
      this.$refs.tree.setCheckedKeys(checkedList);
    },

    setDefaultCheckedKeys() {
      this.clearForm();
      this.$refs.tree.setCheckedKeys(DEFAULT_SCOPES);
    },

    clearForm() {
      this.currentRole.name = "";
      this.currentRole.description = "";
    },

    handleCheckChange() {
      this.currentRole.scope = this.$refs.tree.getCheckedKeys(true).join(" ");
    },

    handleCheckNameContain(nameRole) {
      let index = this.roleListData.rows.findIndex(
        (item) => item.name.toLowerCase() === nameRole.toLowerCase()
      );
      return index > -1;
    },

    async handleClickCreateRole() {
      if (!this.currentRole.name) {
        this.validate = true;
        return;
      }
      if (this.handleCheckNameContain(this.currentRole.name)) {
        this.$toast.error("Role name was exists!");
        return;
      }
      await RoleService.createRole(this.currentRole);
      this.$emit("handleData", false);
      this.mode = "create";
    },

    async handleClickUpdateRole() {
      if (!this.currentRole.name) {
        this.validate = true;
        return;
      }
      await RoleService.updateRole(this.currentRole);
      this.$emit("handleData", false);
    },

    async getAddedData() {
      let responseData = await ScopeService.getScopes();
      if (responseData && responseData.data) {
        this.scopeTree = responseData.data.scope;
        this.fullScope = this.transformDicToArr(this.scopeTree);
      }
    },

    transformDicToArr(scopeTreeArray) {
      const result = [];
      for (let node of scopeTreeArray) {
        for (let el of node.children) {
          result.push(el.scope);
        }
      }
      return result;
    },
  },
};
</script>

<style scoped></style>
