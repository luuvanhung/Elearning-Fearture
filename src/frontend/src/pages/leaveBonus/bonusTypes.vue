<template>
  <div>
    <restricted-view :scopes="[SCOPES['BonusLeaveEdit']]">
      <template v-slot:default>
        <el-card style="width: 100%">
          <el-form :model="newBonusType">
            <el-row :gutter="16">
              <el-col :span="14">
                <el-form-item class="required" label="Name" prop="name">
                  <el-input
                    required
                    id="descriptions"
                    rows="2"
                    v-model="newBonusType.name"
                    class="input_data"
                    maxlength="70"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  class="required"
                  label="Descriptions"
                  prop="descriptions"
                >
                  <el-input
                    type="textarea"
                    required
                    id="descriptions"
                    rows="2"
                    v-model="newBonusType.descriptions"
                    class="input_data"
                    maxlength="256"
                  ></el-input>
                </el-form-item>
              </el-col>
              <div class="d-flex justify-content-center mt-5">
                <div>
                  <el-button
                    v-if="newBonusType.id != null"
                    id="btn-submit"
                    type="primary"
                    size="medium"
                    plain
                    :disabled="disableSaveButton()"
                    @click="submitForm"
                    >Save
                  </el-button>
                  <el-button
                    v-else
                    id="btn-submit"
                    type="primary"
                    size="medium"
                    plain
                    :disabled="disableSaveButton()"
                    @click="submitForm"
                    >Add more
                  </el-button>
                  <el-button
                    id="btn-discard"
                    type="danger"
                    size="medium"
                    plain
                    @click="cancelEditForm"
                    >Cancel
                  </el-button>
                </div>
              </div>
            </el-row>
          </el-form>
        </el-card>
      </template>
    </restricted-view>
    <el-table
      highlight-current-row
      :data="bonusLeaveData"
      header-cell-class-name="bg-header-table"
      stripe
      border
      class="input_data"
    >
      <el-table-column
        type="index"
        label="NO"
        sortable
        align="center"
        width="80"
      >
      </el-table-column>
      <el-table-column
        prop="name"
        label="Name"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="descriptions"
        label="Descriptions"
        align="center"
      ></el-table-column>
      <el-table-column label="Actions" width="180" align="center">
        <template v-slot="scope">
          <restricted-view :scopes="[SCOPES['BonusLeaveEdit']]">
            <template v-slot:default>
              <el-button
                circle
                style="cursor: pointer"
                @click="editBonusType(scope.row)"
                type="primary"
                icon="el-icon-edit"
              ></el-button>
              <el-button
                circle
                style="cursor: pointer"
                type="danger"
                icon="el-icon-delete"
                @click="deleteRequest(scope.row.id)"
              />
            </template>
          </restricted-view>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="Delete"
      :visible.sync="dialogVisible"
      width="30%"
      class="dialog"
    >
      <span>Do you want to delete this template ?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="deleteItem()">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import RestrictedView from "@/components/RestrictedView";
import BonusTypeService from "@/services/leave_management/bonus_leave/bonus_type.services";
import { SCOPES } from "@/const/scopes";

export default {
  name: "BonusTypes",
  middleware: "authentication",
  components: {
    RestrictedView,
  },

  async created() {
    await this.fetchBonusTypes();
  },

  data() {
    return {
      dialogVisible: false,
      bonusLeaveData: [],
      delete_id: "",
      tmpBonusLeave: null,
      newBonusType: {
        id: null,
        name: "",
        descriptions: "",
      },
    };
  },

  computed: {
    SCOPES: function () {
      return SCOPES;
    },
  },

  methods: {
    async fetchBonusTypes() {
      let res = await BonusTypeService.get();
      if (res && res.data) {
        this.bonusLeaveData = res.data;
      }
    },

    cancelEditForm() {
      this.clearBonusTypeData();
    },

    clearBonusTypeData() {
      this.newBonusType.id = null;
      this.newBonusType.name = "";
      this.newBonusType.descriptions = "";
    },

    checkBonusTypeName(name) {
      let index = this.bonusLeaveData.findIndex(
        (item) => item.name.toLowerCase() === name.toLowerCase()
      );
      return index > -1;
    },

    editBonusType(obj) {
      this.newBonusType.id = obj.id;
      this.newBonusType.name = obj.name;
      this.newBonusType.descriptions = obj.descriptions;
      this.tmpBonusLeave = obj;
    },

    deleteRequest(id) {
      this.dialogVisible = true;
      this.delete_id = id;
    },

    disableSaveButton() {
      let name = this.newBonusType.name.trim();
      let descriptions = this.newBonusType.descriptions.trim();
      return name === "" || descriptions === "";
    },

    async deleteItem() {
      if (this.delete_id !== "") {
        this.dialogVisible = false;
        let res = await BonusTypeService.delete(this.delete_id);
        if (res.status === 204) {
          this.$nextTick(() => {
            this.$toast.success("Deleted Successfully");
          });
          let index = this.bonusLeaveData.findIndex(
            (item) => item.id === this.delete_id
          );
          this.bonusLeaveData.splice(index, 1);
          this.clearBonusTypeData();
        } else {
          this.$toast.error("Delete Failed");
        }
      }
    },

    async submitForm() {
      let id = this.newBonusType.id;
      let name = this.newBonusType.name.trim();
      let descriptions = this.newBonusType.descriptions.trim();
      let data = {
        id: id,
        name: name,
        descriptions: descriptions,
      };
      if (id === null && this.checkBonusTypeName(name)) {
        this.$toast.error("Bonus type name was exists!");
        this.clearBonusTypeData();
        return;
      }
      if (name !== "" && descriptions !== "") {
        const res = await BonusTypeService.create_or_update(data);
        this.clearBonusTypeData();
        if (res.status === 200) {
          this.updateBonusTypeData(res.data);
        } else {
          this.$toast.error("Save Failed");
        }
      } else {
        this.$toast.error("Input is not valid!");
      }
    },

    updateBonusTypeData(responseData) {
      let index = this.bonusLeaveData.findIndex(
        (item) => item.id === responseData.id
      );
      if (index < 0) {
        this.bonusLeaveData.unshift(responseData);
        this.$toast.success("Created Successfully");
      } else {
        this.bonusLeaveData[index].name = responseData.name;
        this.bonusLeaveData[index].descriptions = responseData.descriptions;
        this.$toast.success("Updated Successfully");
      }
    },
  },
};
</script>

<style lang="scss">
@import "./bonusTypes.scss";
</style>
