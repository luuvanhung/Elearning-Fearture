<template>
  <el-collapse v-model="activeChooseRoles" accordion>
    <el-collapse-item name="1">
      <template slot="title">
        <img
          :src="require('@/static/images/IconEdit.svg')"
          style="cursor: pointer"
        />
      </template>
      <!-- SELECT SCOPES -->
      <div>
        <el-input placeholder="Filter keyword" v-model="filterText"></el-input>
        <div class="d-flex justify-content-end">
          <el-checkbox
            style="margin-right: -1%"
            v-model="select_all"
            @change="checkAll"
            label="Option1"
            size="small"
            border
          >
            Select all
          </el-checkbox>
          <el-checkbox
            v-model="reset_all"
            @change="reset"
            label="Option1"
            size="small"
            border
          >
            reset
          </el-checkbox>
        </div>

        <div class="row">
          <div class="col-12 mt-3">
            <el-tree
              class="filter-tree"
              ref="treeNewAPIKeyRoles"
              node-key="scope"
              :data="scopes"
              :props="defaultProps"
              :show-checkbox="true"
              :check-strictly="false"
              :highlight-current="true"
              :expand-on-click-node="false"
              :filter-node-method="filterScopes"
              :default-checked-keys="selectedScopes"
              @check-change="handleUpdateScopes"
            >
            </el-tree>
          </div>
        </div>
      </div>
    </el-collapse-item>
  </el-collapse>
</template>
<script>
export default {
  name: "ChooseRoles",
  middleware: "authentication",
  data() {
    return {
      filterText: "",
      defaultProps: {
        children: "children",
        label: "label",
      },
      errors: "",
      select_all: false,
      reset_all: false,
      activeChooseRoles: ["1"],
    };
  },
  props: {
    scopes: { type: Array, default: () => [] },
    selectedScopes: { type: Array, default: () => [] },
  },
  watch: {
    filterText(val) {
      this.$refs.treeNewAPIKeyRoles.filter(val);
    },
    selectedScopes(newScopes) {
      this.selectedScopes = newScopes;
      this.setChecked(newScopes);
    },
  },
  methods: {
    filterScopes(value, data) {
      if (!value) return true;

      return data.label.toLowerCase().includes(value.toLowerCase());
    },
    checkAll() {
      if (!this.select_all) return;

      this.setChecked(this.allScopeArr);
      this.reset_all = false;
    },
    reset() {
      if (!this.reset_all) return;

      this.setChecked([]);
      this.select_all = false;
    },
    setChecked(checkedList = []) {
      this.$refs.treeNewAPIKeyRoles.setCheckedKeys(checkedList);
    },
    handleUpdateScopes() {
      this.$emit("handleUpdateScopes", this.getSelectedScopes());
    },
    getSelectedScopes() {
      return this.$refs.treeNewAPIKeyRoles.getCheckedKeys(true);
    },
    resetCollapse() {
      this.activeChooseRoles = ["1"];
    },
  },
  computed: {
    allScopeArr() {
      const result = [];
      for (let node of this.scopes) {
        for (let el of node.children) {
          result.push(el.scope);
        }
      }
      return result;
    },
  },
};
</script>

<style lang="scss">
.filter-tree {
  .el-tree-node__label {
    white-space: break-spaces !important;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    word-break: break-word;
  }
}
</style>
