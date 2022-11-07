<template>
  <div>
    <el-input placeholder="Filter Name" v-model="filterText"></el-input>
    <el-tree
      :data="data"
      node-key="id"
      default-expand-all
      :props="defaultProps"
      :filter-node-method="filterNode"
      :expand-on-click-node="false"
      ref="tree"
    >
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <template v-if="node.isEdit">
          <div class="row">
            <div class="col-12 col-md-10">
              <div class="row">
                <div class="col-12 col-md-4 mt-1 mt-md-0">
                  <el-input
                    v-model="data.name"
                    autofocus
                    size="mini"
                    :ref="'slotTreeInput' + data[NODE_KEY]"
                    class="field-input"
                  ></el-input>
                </div>
                <div class="col-12 col-md-4 mt-1 mt-md-0">
                  <el-select
                    v-model="data.manager_id"
                    filterable
                    placeholder="Select Manager"
                    size="mini"
                  >
                    <el-option
                      v-for="item in usersList"
                      :key="item.id"
                      :label="item.user_name + ' - ' + item.user_title"
                      :value="item.id"
                    ></el-option>
                  </el-select>
                </div>
                <div class="col-12 col-md-4 mt-1 mt-md-0">
                  <el-input
                    v-model="data.address"
                    autofocus
                    size="mini"
                    :ref="'slotTreeInput' + data[NODE_KEY]"
                    placeholder="Address"
                    class="field-input"
                    v-if="data.isOfficeChild"
                  ></el-input>
                </div>
              </div>
            </div>
            <div class="col-12 col-md-2 mt-2 mt-md-0">
              <el-button
                size="mini"
                type="primary"
                @click="handleInput(node, data)"
                >Save</el-button
              >
              <el-button size="mini" type="info" @click="cancel(node, data)"
                >Cancel</el-button
              >
            </div>
          </div>
        </template>
        <template v-else>
          <div>
            <span class="d-block title-tree" v-if="!data.isOfficeChild">
              <font-awesome-icon
                :icon="['fas', 'folder']"
                class="option-icon"
                v-if="!data.isOfficeChild && !node.expanded"
              />
              <font-awesome-icon
                :icon="['fas', 'folder-open']"
                class="option-icon"
                v-else-if="
                  !data.isOfficeChild &&
                  node.expanded &&
                  !data.isChildrenDepartments
                "
              />
              <font-awesome-icon
                :icon="['fas', 'users']"
                class="option-icon"
                v-else-if="data.isChildrenDepartments"
              />
              {{ node.label }} : {{ node.data.manager_name }} -
              {{ node.data.manager_title }}
            </span>
            <span class="d-block title-tree" v-else>
              <router-link
                :to="{ name: 'OfficeInformation', params: { id: data.id } }"
              >
                <img
                  :src="require('@/static/images/OfficesIcon.svg')"
                  class="option-icon"
                />
                {{ node.label }} : {{ node.data.manager_name }} -
                {{ node.data.manager_title }}
              </router-link>
            </span>
            <template v-if="node.isAdd">
              <div class="row">
                <div class="col-12 col-md-10">
                  <div class="row">
                    <div class="col-12 col-md-4 mt-1 mt-md-0">
                      <el-input
                        v-model="initParam.name"
                        autofocus
                        size="mini"
                        class="field-input"
                        :placeholder="
                          !data.createDepartment
                            ? data.createOffice
                              ? 'Office Name'
                              : 'Group Name'
                            : 'Team Name'
                        "
                      ></el-input>
                    </div>
                    <div class="col-12 col-md-4 mt-1 mt-md-0">
                      <el-select
                        v-model="initParam.manager"
                        filterable
                        placeholder="Select Manager"
                        size="mini"
                      >
                        <el-option
                          v-for="item in usersList"
                          :key="item.id"
                          :label="item.user_name + ' - ' + item.user_title"
                          :value="item.id"
                        ></el-option>
                      </el-select>
                    </div>
                    <div class="col-12 col-md-4 mt-1 mt-md-0">
                      <el-input
                        v-model="initParam.address"
                        autofocus
                        size="mini"
                        :ref="'slotTreeInput' + data[NODE_KEY]"
                        placeholder="Address"
                        class="field-input"
                        v-if="data.createOffice"
                      ></el-input>
                    </div>
                  </div>
                </div>
                <div class="col-12 col-md-2 mt-2 mt-md-0">
                  <el-button
                    size="mini"
                    type="primary"
                    @click="append(node, data)"
                    >Save</el-button
                  >
                  <el-button size="mini" type="info" @click="cancel(node, data)"
                    >Cancel</el-button
                  >
                </div>
              </div>
            </template>
          </div>
          <restricted-view :scopes="['office:edit']">
            <template v-slot:default>
              <span>
                <el-button
                  v-if="!data.isOfficeChild && !data.isChildrenDepartments"
                  size="mini"
                  circle
                  @click="handleAddOffice(node, data)"
                >
                  <img
                    :src="require('@/static/images/AddOffice.svg')"
                    class="option-icon"
                  />
                </el-button>

                <el-button
                  v-if="!data.isOfficeChild && !data.isChildrenDepartments"
                  size="mini"
                  circle
                  @click="handleAdd(node)"
                >
                  <font-awesome-icon
                    :icon="['fas', 'folder-plus']"
                    class="option-icon"
                  ></font-awesome-icon>
                </el-button>

                <el-button
                  v-if="data.isOfficeChild"
                  size="mini"
                  circle
                  @click="handleAddDepartment(node, data)"
                >
                  <font-awesome-icon
                    :icon="['fas', 'user-plus']"
                    class="option-icon"
                  ></font-awesome-icon>
                </el-button>

                <el-button
                  icon="el-icon-edit"
                  size="mini"
                  circle
                  type="info"
                  class="mr-2"
                  @click="handleEdit(node, data)"
                ></el-button>

                <el-popover
                  placement="top"
                  width="250"
                  v-model="data.confirmDelete"
                >
                  <p>Are you sure to delete this?</p>

                  <div style="text-align: right; margin: 10px 0px">
                    <el-button
                      size="mini"
                      type="text"
                      @click="data.confirmDelete = false"
                      >Cancel</el-button
                    >
                    <el-button
                      type="primary"
                      size="mini"
                      @click="remove(node, data)"
                      >Confirm</el-button
                    >
                  </div>

                  <el-button
                    icon="el-icon-delete"
                    size="mini"
                    circle
                    type="danger"
                    slot="reference"
                  ></el-button>
                </el-popover>
              </span>
            </template>
          </restricted-view>
        </template>
      </span>
    </el-tree>
  </div>
</template>

<script>
import officeService from "@/services/office/office.service.js";
import groupService from "@/services/office/group.service.js";
import message from "@/services/office/responseMessage.js";
import userService from "@/services/user/user.js";
import RestrictedView from "@/components/RestrictedView";
import departmentService from "@/services/office/department.service.js";
import { mapGetters } from "vuex";

export default {
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val);
    },
  },
  data() {
    return {
      data: [],
      filterText: "",
      defaultProps: {
        children: "children_groups",
        label: "name",
      },
      curText: "",
      HTMLcontent: null,
      IsLoading: false,
      SetTree: [],
      NODE_KEY: "id",
      NODE_ID_START: 0,
      startId: null,
      initParam: {
        name: "",
        manager: "",
        children: [],
        address: "",
      },
      usersList: [],
    };
  },
  computed: {
    ...mapGetters("user", ["allUsers"]),
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true;
      return data.name.indexOf(value) !== -1;
    },

    async append(node, data) {
      const dataForm = new FormData();
      dataForm.append("name", this.initParam.name);
      dataForm.append("manager", this.initParam.manager);
      if (!this.initParam.name || !this.initParam.manager) {
        return this.$toast.error(message.VALIDATION);
      }

      if (data.createOffice) {
        dataForm.append("group", data.id);
        dataForm.append("address", this.initParam.address);
      } else if (data.createDepartment) {
        dataForm.append("office", data.id);
      } else {
        dataForm.append("parent_group", data.id);
      }

      try {
        let response = !data.createDepartment
          ? data.createOffice
            ? await officeService.createOffice(dataForm)
            : await groupService.createGroup(dataForm)
          : await departmentService.createDepartment(dataForm);
        this.$set(node, "isAdd", false);
        let managerData = this.usersList.find(
          (d) => d.id === response.data.manager
        );
        const newChild = {
          id: response.data.id,
          name: this.initParam.name,
          manager_name: managerData.user_name,
          manager_title: managerData.user_title,
          address: this.initParam.address,
          children_groups: [],
          isOfficeChild: data.createOffice ? true : false,
          isChildrenDepartments: data.createDepartment ? true : false,
        };
        if (!data.children_groups) {
          this.$set(data, "children_groups", []);
        }
        data.children_groups.push(newChild);
        this.initParam.name = "";
        this.initParam.manager = "";
        this.$toast.success("Created Successfully");
      } catch (error) {
        let errorContent =
          error?.response.status == 400 && error.response.data
            ? error.response.data.name[0]
            : "Create Failed";
        this.$toast.error(errorContent);
      }
    },
    cancel(node, data) {
      this.$set(node, "isEdit", false);
      this.$set(node, "isAdd", false);
      data.createOffice = false;
      this.initParam.name = "";
      this.initParam.manager = "";
    },

    async remove(node, data) {
      const parent = node.parent;
      const children = parent.data.children_groups || parent.data;
      const index = children.findIndex((d) => d.id === data.id);
      try {
        !data.isChildrenDepartments
          ? data.isOfficeChild
            ? await officeService.deleteOffice(data.id)
            : await groupService.deleteGroup(data.id)
          : await departmentService.deleteDepartment(data.id);

        this.$toast.success("Deleted Successfully");
      } catch (error) {
        let errorContent =
          error.response.status == 400 && error.response.data
            ? error.response.data.name[0]
            : "Delete Failed";
        this.$toast.error(errorContent);
      }
      children.splice(index, 1);
    },

    async handleInput(node, data) {
      const dataForm = new FormData();
      dataForm.append("name", data.name);
      dataForm.append("manager", data.manager_id);
      if (data.isOfficeChild) {
        dataForm.append("group", node.parent.data.id);
        dataForm.append("address", data.address);
      } else if (data.isChildrenDepartments) {
        dataForm.append("office", node.parent.data.id);
      } else {
        dataForm.append("parent_group", node.parent.data.id);
      }
      let response = null;
      try {
        if (dataForm.get("parent_group") === "undefined") {
          dataForm.delete("parent_group");
        }

        response = !data.isChildrenDepartments
          ? data.isOfficeChild
            ? await officeService.editOffice(dataForm, data.id)
            : await groupService.editGroup(dataForm, data.id)
          : await departmentService.editDepartment(dataForm, data.id);

        let managerData = this.usersList.find(
          (d) => d.id === response.data.manager
        );
        data.manager_name = managerData.user_name;
        data.manager_title = managerData.user_title;
        this.$toast.success("Updated Successfully");
      } catch (error) {
        let errorContent =
          error.response.status == 400 && error.response.data
            ? error.response.data.name
            : "Update Failed";
        this.$toast.error(errorContent);
      }
      if (node.isEdit) {
        this.$set(node, "isEdit", false);
      }
    },

    handleEdit(node, data) {
      if (!node.isEdit) {
        this.$set(node, "isEdit", true);
      }
      this.$nextTick(() => {
        if (this.$refs["slotTreeInput" + data[this.NODE_KEY]]) {
          this.$refs["slotTreeInput" + data[this.NODE_KEY]].$refs.input.focus();
        }
      });
    },

    handleAddDepartment(node, data) {
      if (!node.isAdd) {
        this.$set(node, "isAdd", true);
        data.createDepartment = true;
      }
    },

    handleAdd(node) {
      if (!node.isAdd) {
        this.$set(node, "isAdd", true);
      }
    },

    handleAddOffice(node, data) {
      if (!node.isAdd) {
        this.$set(node, "isAdd", true);
        data.createOffice = true;
      }
    },

    convertData(data) {
      data.confirmDelete = false;
      if (data.children_offices && data.children_offices.length > 0) {
        data.children_offices.forEach((element) => {
          element.isOfficeChild = true;
          if (element.children_departments) {
            element.children_groups = element.children_departments;
            element.children_groups.forEach((value) => {
              value.isChildrenDepartments = true;
            });
          }
        });

        if (!data.children_groups) {
          data.children_groups = data.children_offices;
        } else {
          data.children_groups = data.children_groups.concat(
            data.children_offices
          );
        }
      }
      if (data.children_groups && data.children_groups.length > 0) {
        data.children_groups.forEach((element) => {
          return this.convertData(element);
        });
      }
      return data;
    },
    async getData() {
      let usersListData = await userService.getUsersIncludeNameAndTitle();
      this.usersList = usersListData.data;

      let responseData = await officeService.getAllOffice();
      let data = responseData.data
        ? this.convertData(responseData.data)
        : this.initParam;
      return this.data.push(data);
    },
  },
  async created() {
    return this.getData();
  },
};
</script>
<style lang="scss" scope>
@import "index.scss";
</style>
