<template>
  <div>
    <restricted-view :scopes="['type_off:edit']">
      <template v-slot:default>
        <el-card style="width: 100%">
          <el-form ref="addLeaveType" :rules="rules" :model="newLeaveType">
            <el-row :gutter="20">
              <el-col :span="8" class="mb-0">
                <el-form-item prop="name" label="Name">
                  <el-input
                    v-model="newLeaveType.titleOffTypes"
                    class="input_data"
                    ref="name"
                    clearable
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="6" class="mb-0">
                <el-form-item label="Group" prop="groupTypeOffChoose">
                  <el-select
                    v-model="newLeaveType.groupTypeOffChoose"
                    class="input_data"
                  >
                    <el-option
                      v-for="typePay in listTypeOffGroup"
                      :label="typePay.name"
                      :value="typePay.id"
                      :key="typePay.id"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="4" class="mb-0 pr-0 p0">
                <el-form-item label="Limit Leave Days">
                  <el-input-number
                    class="input_data"
                    size="big"
                    v-model="newLeaveType.totalDayLeaves"
                    :min="1"
                    :max="365"
                  ></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="4" class="mb-0 ml-1">
                <el-form-item label="Is Count?">
                  <br />
                  <el-checkbox v-model="newLeaveType.isCount" border
                    >Count Leave Days</el-checkbox
                  >
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="10">
                <el-form-item
                  label="Descriptions"
                  class="mb-0"
                  prop="descriptions"
                >
                  <el-input
                    type="textarea"
                    id="descriptions"
                    rows="2"
                    v-model="newLeaveType.descriptions"
                    clearable
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="8" class="mb-0">
                <el-form-item
                  label="Approval Title Suggestion"
                  prop="approvalTitle"
                >
                  <br />
                  <el-select v-model="newLeaveType.approvalTitle">
                    <el-option
                      v-for="title in listTitle"
                      :key="title.id"
                      :label="title.title"
                      :value="title.id"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <div class="d-flex justify-content-end mt-5">
                <el-button type="danger" class="mr-2" @click="cancelLeave()">
                  Cancel
                </el-button>
                <el-button
                  type="primary"
                  class="btn_submit"
                  @click="submitLeave(type !== '' ? type : 0, 'addLeaveType')"
                >
                  {{ button_submit }}
                </el-button>
              </div>
            </el-row>
          </el-form>
        </el-card>
      </template>
    </restricted-view>
    <el-table
      highlight-current-row
      :data="listTypeOff"
      :span-method="objectSpanMethod"
      stripe
      header-cell-class-name="bg-header-table"
      border
      class="input_data"
    >
      <el-table-column prop="name_type" label="Group" width="300">
        <template v-slot="scope">
          <div v-if="scope.row.is_active === true">
            {{ scope.row.name_type }}
          </div>
          <div v-else>
            <s>{{ scope.row.name_type }}</s>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="Name">
        <template v-slot="scope">
          <div v-if="scope.row.is_active === true">
            {{ scope.row.name }}
          </div>
          <div v-else>
            <s>{{ scope.row.name }}</s>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="descriptions"
        label="Description"
      ></el-table-column>
      <el-table-column
        prop="approval_title_name"
        label="Approval Title Suggestion"
        width="300"
        align="center"
      >
        <template v-slot="scope">
          <div v-if="scope.row.is_active === true">
            {{ scope.row.approval_title_name }}
          </div>
          <div v-else>
            <s>{{ scope.row.approval_title_name }}</s>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="is_count"
        label="Counted"
        width="80"
        align="center"
      >
        <template v-slot="scope">
          {{ scope.row.is_count === true ? "Yes" : "No" }}
        </template>
      </el-table-column>
      <el-table-column
        prop="days"
        label="Limit Days"
        width="100"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="is_active"
        label="Active"
        width="65"
        align="center"
      >
        <template v-slot="scope">
          <el-switch
            active-color="#25c9d0"
            inactive-color="#ff4949"
            v-model="scope.row.is_active"
            @change="switchActive(scope.row)"
          >
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="150" align="center">
        <template v-slot="scope">
          <restricted-view :scopes="['type_off:edit']">
            <template v-slot:default>
              <el-button
                circle
                style="cursor: pointer"
                @click="editLeaveType(scope.row)"
                type="primary"
                icon="el-icon-edit"
              ></el-button>
              <el-button
                circle
                style="cursor: pointer"
                type="danger"
                icon="el-icon-delete"
                @click="deleteOffType(scope.row)"
              />
            </template>
          </restricted-view>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import TypeOffAdminServices from "@/services/leave_management/type_off/type_off_admin.services";
import TypeOffGroupAdminServices from "@/services/leave_management/type_off/type_off_group.services";
import RestrictedView from "@/components/RestrictedView";
import GetUserService from "@/services/user/getUser";

export default {
  name: "LeaveType",
  components: {
    RestrictedView,
  },
  middleware: "authentication",
  created: async function () {
    await GetUserService.getAllTitles().then((res) => {
      this.getListTitle(res.data);
    });
    await TypeOffAdminServices.getTypeOff().then((res) => {
      this.getListTypeOff(res.data);
    });
    await TypeOffGroupAdminServices.getTypeOffGroup().then((res) => {
      this.getListTypeOffGroup(res.data);
    });
    this.groupTable();
  },
  computed: {
    ...mapGetters({
      listTypeOff: "offType/listTypeOff",
      listTypeOffGroup: "offTypeGroup/listTypeOffGroup",
      listTitle: "title/listTitle",
      showNotification: "showNotification",
    }),
  },
  data() {
    return {
      newLeaveType: {
        titleOffTypes: "",
        groupTypeOffChoose: "",
        descriptions: "",
        approvalTitle: "",
        isCount: false,
        totalDayLeaves: 1,
      },
      BUTTON_SUBMIT: (title) => `${title}`,
      button_submit: "Add more",
      idOffEditDelete: "",
      type: 0,
      tempTitle: "",
      id_array: [],
      id_pos: 0,
      row: "",
      column: "",
      rules: {
        name: [
          {
            required: true,
            validator: (_rule, _value, callback, _source, _options) => {
              if (this.newLeaveType.titleOffTypes.trim().length === 0) {
                callback(new Error("Name is required"));
              } else if (
                this.newLeaveType.titleOffTypes.trim().length > 50 ||
                this.newLeaveType.titleOffTypes.trim().length < 3
              ) {
                callback(new Error("Name must be between 3 and 50 characters"));
              }
              callback();
            },
            trigger: ["blur"],
          },
        ],
        descriptions: [
          {
            required: true,
            validator: (_rule, _value, callback, _source, _options) => {
              if (this.newLeaveType.descriptions.trim().length === 0) {
                callback(new Error("Description is required"));
              } else if (
                this.newLeaveType.descriptions.trim().length > 50 ||
                this.newLeaveType.descriptions.trim().length < 3
              ) {
                callback(
                  new Error("Description must be between 3 and 50 characters")
                );
              }
              callback();
            },
            trigger: ["blur"],
          },
        ],
        approvalTitle: [
          {
            required: true,
            message: "Approver is required",
            trigger: "change",
          },
        ],
        groupTypeOffChoose: [
          { required: true, message: "Group is required", trigger: "change" },
        ],
      },
    };
  },
  methods: {
    ...mapActions({
      getListTypeOffGroup: "offTypeGroup/getListTypeOffGroup",
      getListTypeOff: "offType/getListTypeOff",
      updateListTypeOff: "offType/updateListTypeOff",
      deleteListTypeOff: "offType/deleteListTypeOff",
      getListTitle: "title/updateListTitle",
    }),
    editLeaveType(obj) {
      this.idOffEditDelete = obj.id;
      this.newLeaveType.titleOffTypes = obj.name;
      const indexTypeOffGroup = this.listTypeOffGroup.findIndex(
        (item) => item.id === obj.leave_type_group
      );
      const indexTitle = this.listTitle.findIndex(
        (item) => item.title === obj.approval_title_name
      );
      this.newLeaveType.groupTypeOffChoose =
        this.listTypeOffGroup[indexTypeOffGroup].id;
      this.newLeaveType.isCount = obj.is_count;
      this.newLeaveType.totalDayLeaves = obj.days;
      this.newLeaveType.descriptions = obj.descriptions;
      this.type = 1; // return update status
      this.newLeaveType.approvalTitle = this.listTitle[indexTitle].id;
      this.button_submit = this.BUTTON_SUBMIT("Save");
    },
    cancelLeave() {
      this.newLeaveType.titleOffTypes = "";
      this.newLeaveType.isCount = false;
      this.newLeaveType.groupTypeOffChoose = "";
      this.type = 0; // return add status
      this.newLeaveType.approvalTitle = "";
      this.button_submit = this.BUTTON_SUBMIT("Add more");
      this.newLeaveType.descriptions = "";
      this.newLeaveType.totalDayLeaves = 1;
    },
    submitLeave(pk, formName) {
      this.$refs[formName].validate((valid) => {
        let data;
        data = {
          name: this.newLeaveType.titleOffTypes,
          leave_type_group: this.newLeaveType.groupTypeOffChoose,
          days: this.newLeaveType.totalDayLeaves,
          is_count: this.newLeaveType.isCount,
          descriptions: this.newLeaveType.descriptions,
          approval_title: this.newLeaveType.approvalTitle,
        };
        if (data && valid) {
          TypeOffAdminServices.updateOrCreateTypeOff(
            pk,
            this.idOffEditDelete,
            data
          )
            .then((res) => {
              this.updateListTypeOff(res.data);
              this.groupTable();
              let message;
              res.status === 200
                ? (message = "Updated Successfully")
                : (message = "Added Successfully");
              this.$toast.success(message);
            })
            .catch(() => {
              this.$toast.error("An error occurred");
            });
          this.cancelLeave();
        }
      });
    },
    switchActive(obj) {
      TypeOffAdminServices.handleActiveTypeOff(obj.id)
        .then((res) => {
          if (res.status === 200) {
            this.$toast.success(
              `${res.data.is_active ? "Active" : "Hidden"} Successfully`
            );
          }
        })
        .catch(() => {
          this.$toast.error("You don't have permission!");
          obj.is_active = !obj.is_active;
        });
    },
    deleteOffType(obj) {
      if (confirm("Are you sure you want to delete this item?")) {
        TypeOffAdminServices.deleteTypeOff(obj.id)
          .then((res) => {
            if (res.status === 204) {
              this.deleteListTypeOff(obj);
              this.groupTable();
              this.$toast.success("Deleted Successfully");
            }
          })
          .catch(() => {
            this.$toast.error("An error occurred");
          });
      }
    },
    groupTable() {
      this.id_array = [];
      this.id_pos = 0;
      for (let i = 0; i < this.listTypeOff.length; i++) {
        if (i === 0) {
          this.id_array.push(1);
          this.id_pos = 0;
        } else {
          if (
            this.listTypeOff[i].name_type === this.listTypeOff[i - 1].name_type
          ) {
            this.id_array[this.id_pos] += 1;
            this.id_array.push(0);
          } else {
            this.id_array.push(1);
            this.id_pos = i;
          }
        }
      }
    },
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      this.row = row;
      this.column = column;
      if (columnIndex === 0) {
        const _row = this.id_array[rowIndex];
        const _col = _row > 0 ? 1 : 0;
        return {
          rowspan: _row,
          colspan: _col,
        };
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
