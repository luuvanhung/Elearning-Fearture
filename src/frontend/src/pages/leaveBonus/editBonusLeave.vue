<template>
  <div v-show="visible">
    <el-card>
      <el-form
        :label-position="'left'"
        label-width="130px"
        :model="oldBonusLeave"
        status-icon
        :rules="rules"
        hide-required-asterisk
        size="small"
      >
        <el-row>
          <el-col :span="15">
            <el-form-item label="Name" prop="profileTemp.name">
              <el-input
                disabled
                v-model="oldBonusLeave.profileTemp.name"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="15">
            <el-form-item label="Personal" prop="profileTemp.personal_email">
              <el-input
                disabled
                v-model="oldBonusLeave.profileTemp.personal_email"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="15">
            <el-form-item label="Bonus Leave" prop="bonus_days">
              <el-input-number
                controls-position="right"
                size="medium"
                v-model="oldBonusLeave.bonus_days"
                :step="0.5"
                :min="0.5"
                :max="365"
                :step-strictly="true"
                placeholder="Amount of leaves"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="15">
            <el-form-item label="Reason" prop="reason">
              <el-input v-model="oldBonusLeave.reason"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="15">
            <el-form-item label="Type" prop="bonus_type">
              <el-select
                v-model="oldBonusLeave.bonus_type"
                :options="optionsBonusType"
                placeholder="Type"
              >
                <el-option
                  v-for="(item, index) in optionsBonusType"
                  :key="index"
                  :label="item.name"
                  :value="item.id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <el-row type="flex" class="row-bg" justify="center">
        <div>
          <el-button
            id="btn-submit"
            type="primary"
            size="medium"
            plain
            @click="submitForm"
            >Save
          </el-button>
          <el-button
            id="btn-discard"
            type="default"
            size="medium"
            plain
            @click="closeEditForm"
            >Cancel
          </el-button>
        </div>
      </el-row>
    </el-card>
  </div>
</template>
<script>
import BonusLeaveService from "@/services/leave_management/bonus_leave/bonus_leave.services";

export default {
  name: "EditBonusLeave",
  props: ["optionsBonusType", "oldBonusLeave", "visible"],

  data() {
    return {
      bonusLeaveTemp: null,
      rules: {
        reason: [
          {
            required: true,
            message: "Please input Reason",
            trigger: "change",
          },
        ],
        bonus_type: [
          {
            required: true,
            message: "Please select Bonus Type!",
            trigger: "change",
          },
        ],
      },
    };
  },
  methods: {
    submitForm() {
      if (this.oldBonusLeave.bonus_days % 0.5 === 0) {
        BonusLeaveService.edit(this.oldBonusLeave)
          .then((res) => {
            if (res.status === 200) {
              this.$toast.success("Edited Successfully");
              this.closeEditForm();
            }
          })
          .catch(() => {
            this.$toast.error("Edit Failed");
          });
      } else {
        this.$toast.error("Given Leave Incorrect Type");
      }
    },
    closeEditForm() {
      this.visible = false;
      this.$emit("handleEditData", false);
    },
  },
};
</script>

<style lang="scss" scoped>
.el-card {
  margin: 12px;
  padding: 20px;
  color: #333;

  h4.title {
    font-weight: 600;
    padding-bottom: 10px;
    border-bottom: #ccc solid 1.5px;
    margin-bottom: 10px;
  }

  .el-select.max-width {
    width: 100%;
  }
}
</style>
