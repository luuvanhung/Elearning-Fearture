<template>
  <div>
    <restricted-view :scopes="['type_pay:edit']">
      <template v-slot:default>
        <el-card style="width: 100%">
          <el-form ref="addLeaveTypeGroup" :model="newLeaveTypeGroup">
            <el-row :gutter="20">
              <el-col :span="10">
                <el-form-item label="Name:" prop="name" :rules="rules.name">
                  <el-input
                    v-model="newLeaveTypeGroup.titlePaymentType"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item label="Pay choices:">
                  <br />
                  <el-checkbox
                    v-model="newLeaveTypeGroup.isCompanyPay"
                    label="Company Pay"
                    border
                    size="big"
                  ></el-checkbox>
                  <el-checkbox
                    v-model="newLeaveTypeGroup.isInsurancePay"
                    label="Insurance Pay"
                    border
                    size="big"
                  ></el-checkbox>
                </el-form-item>
              </el-col>
            </el-row>
            <div class="d-flex justify-content-end">
              <el-button type="danger" @click="cancelPayment()">
                Cancel
              </el-button>
              <el-button
                type="primary"
                class="btn_submit"
                @click="submitPay(type !== '' ? type : 0, 'addLeaveTypeGroup')"
              >
                {{ button_submit }}
              </el-button>
            </div>
          </el-form>
        </el-card>
      </template>
    </restricted-view>
    <el-table
      highlight-current-row
      :data="listTypeOffGroup"
      stripe
      header-cell-class-name="bg-header-table"
      border
      style="width: 100%"
    >
      <el-table-column prop="name" label="Name"></el-table-column>
      <el-table-column label="Pay Choices" width="360">
        <template v-slot="scope">
          <el-checkbox
            v-model="scope.row.is_company_pay"
            label="Company Pay"
            border
            size="big"
            @change="changeCheckboxCompany(scope.row)"
          ></el-checkbox>
          <el-checkbox
            v-model="scope.row.is_insurance_pay"
            label="Insurance Pay"
            border
            size="big"
            @change="changeCheckboxInsurance(scope.row)"
          ></el-checkbox>
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="150" align="center">
        <template v-slot="scope">
          <restricted-view :scopes="['type_pay:edit']">
            <template v-slot:default>
              <el-button
                circle
                style="cursor: pointer"
                @click="editPaymentType(scope.row)"
                type="primary"
                icon="el-icon-edit"
              ></el-button>
              <el-button
                circle
                style="cursor: pointer"
                type="danger"
                icon="el-icon-delete"
                @click="deletePaymentType(scope.row)"
              />
            </template>
          </restricted-view>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import TypeOffGroupAdminServices from "@/services/leave_management/type_off/type_off_group.services";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "LeaveTypeGroup",
  components: {
    RestrictedView,
  },
  created: function () {
    TypeOffGroupAdminServices.getTypeOffGroup().then((res) => {
      this.getListTypeOffGroup(res.data);
    });
  },
  computed: {
    ...mapGetters({
      listTypeOffGroup: "offTypeGroup/listTypeOffGroup",
    }),
  },
  data() {
    return {
      BUTTON_SUBMIT: (title) => `${title}`,
      newLeaveTypeGroup: {
        titlePaymentType: "",
        isCompanyPay: false,
        isInsurancePay: false,
      },
      button_submit: "Add more",
      idPayEditDelete: "",
      idPayTemp: "",
      isCompanyPayTemp: false,
      isInsurancePayTemp: false,
      type: 0,
      rules: {
        name: [
          {
            required: true,
            validator: (_rule, _value, callback, _source, _options) => {
              if (this.newLeaveTypeGroup.titlePaymentType.trim().length === 0) {
                callback(new Error("Name is required"));
              } else if (
                this.newLeaveTypeGroup.titlePaymentType.trim().length > 50 ||
                this.newLeaveTypeGroup.titlePaymentType.trim().length < 3
              ) {
                callback(new Error("Name must be between 3 and 50 characters"));
              }
              callback();
            },
            trigger: ["blur"],
          },
        ],
      },
    };
  },
  methods: {
    ...mapActions({
      getListTypeOffGroup: "offTypeGroup/getListTypeOffGroup",
      updateListTypeOffGroup: "offTypeGroup/updateListTypeOffGroup",
      deleteListTypeOffGroup: "offTypeGroup/deleteListTypeOffGroup",
    }),
    changeCheckboxCompany(typeOffGroup) {
      if (this.idPayTemp === "" || this.idPayTemp !== typeOffGroup.id) {
        this.idPayTemp = typeOffGroup.id;
        typeOffGroup.is_company_pay = !typeOffGroup.is_company_pay;
        this.isCompanyPayTemp = typeOffGroup.is_company_pay;
        this.isInsurancePayTemp = typeOffGroup.is_insurance_pay;
      } else {
        typeOffGroup.is_company_pay = this.isCompanyPayTemp;
        typeOffGroup.is_insurance_pay = this.isInsurancePayTemp;
      }
    },
    changeCheckboxInsurance(typeOffGroup) {
      if (this.idPayTemp === "" || this.idPayTemp !== typeOffGroup.id) {
        this.idPayTemp = typeOffGroup.id;
        typeOffGroup.is_insurance_pay = !typeOffGroup.is_insurance_pay;
        this.isCompanyPayTemp = typeOffGroup.is_company_pay;
        this.isInsurancePayTemp = typeOffGroup.is_insurance_pay;
      } else {
        typeOffGroup.is_company_pay = this.isCompanyPayTemp;
        typeOffGroup.is_insurance_pay = this.isInsurancePayTemp;
      }
    },

    editPaymentType(obj) {
      this.idPayEditDelete = obj.id;
      this.newLeaveTypeGroup.titlePaymentType = obj.name;
      this.newLeaveTypeGroup.isCompanyPay = obj.is_company_pay;
      this.newLeaveTypeGroup.isInsurancePay = obj.is_insurance_pay;
      this.type = 1; // return update status
      this.button_submit = this.BUTTON_SUBMIT("Save");
    },
    cancelPayment() {
      this.newLeaveTypeGroup.titlePaymentType = "";
      this.newLeaveTypeGroup.isCompanyPay = false;
      this.newLeaveTypeGroup.isInsurancePay = false;
      this.type = 0; // return add status
      this.button_submit = this.BUTTON_SUBMIT("Add more");
    },
    submitPay(pk, formName) {
      this.$refs[formName].validate((valid) => {
        let data;
        data = {
          name: this.newLeaveTypeGroup.titlePaymentType,
          is_company_pay: this.newLeaveTypeGroup.isCompanyPay,
          is_insurance_pay: this.newLeaveTypeGroup.isInsurancePay,
        };
        if (data && valid) {
          TypeOffGroupAdminServices.updateOrCreateTypeOffGroup(
            pk,
            this.idPayEditDelete,
            data
          )
            .then((res) => {
              this.updateListTypeOffGroup(res.data);
              let message;
              res.status === 200
                ? (message = "Updated Successfully")
                : (message = "Added Successfully");
              this.$toast.success(message);
            })
            .catch(() => {
              this.$toast.error("An error occurred");
            });
          this.cancelPayment();
        }
      });
    },
    deletePaymentType(obj) {
      if (confirm("Are you sure you want to delete this item?")) {
        TypeOffGroupAdminServices.deleteTypeOffGroup(obj.id)
          .then((res) => {
            if (res.status === 204) {
              this.deleteListTypeOffGroup(obj);
              this.$toast.success("Deleted Successfully");
            }
          })
          .catch(() => {
            this.$toast.error("An error occurred");
          });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
