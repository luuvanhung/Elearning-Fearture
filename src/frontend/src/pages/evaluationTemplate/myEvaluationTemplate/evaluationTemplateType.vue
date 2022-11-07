<template>
  <div>
    <restricted-view :scopes="['evaluation_template:create']">
      <template v-slot:default>
        <el-card style="width: 100%">
          <el-form ref="formAddEvaluationType" :model="formData">
            <el-row :gutter="16">
              <el-col :span="14">
                <el-form-item
                  label="New evaluation type"
                  class="mb-0"
                  prop="typeName"
                  :rules="rules.name"
                >
                  <el-input
                    id="type_name"
                    rows="2"
                    v-model="formData.typeName"
                    placeholder="Enter name"
                    class="input_data"
                    clearable
                  ></el-input>
                </el-form-item>
              </el-col>
              <div class="d-flex justify-content-end mt-5">
                <el-button type="danger" class="mr-2" @click="cancelDialog()">
                  Cancel
                </el-button>
                <el-button
                  type="primary"
                  class="btn_submit"
                  @click="
                    submit(type !== '' ? type : 0, 'formAddEvaluationType')
                  "
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
      :data="templateTypes"
      header-cell-class-name="bg-header-table"
      stripe
      border
      class="input_data"
    >
      <el-table-column type="index" sortable align="center" width="80">
      </el-table-column>
      <el-table-column
        prop="type_name"
        label="Type"
        align="center"
      ></el-table-column>
      <el-table-column label="Actions" width="180" align="center">
        <template v-slot="scope">
          <restricted-view :scopes="['evaluation_template:edit']">
            <template v-slot:default>
              <el-button
                circle
                style="cursor: pointer"
                @click="editTemplateType(scope.row)"
                type="primary"
                icon="el-icon-edit"
              ></el-button>
              <el-button
                circle
                style="cursor: pointer"
                type="danger"
                icon="el-icon-delete"
                @click="showRemoveDialog(scope.row.type_name, scope.row.id)"
              />
            </template>
          </restricted-view>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="isDialogRemove" hide-footer hide-header="">
      <div class="d-block text-center text-danger">
        <h3>Remove Evaluation Type</h3>
      </div>
      <div class="d-block text-center mb-4 mt-4">
        Are you sure you want to delete this type of evaluation:
        <p class="text-danger d-inline">{{ currentType }}</p>
      </div>
      <div class="d-flex justify-content-center">
        <el-button type="primary" @click="deleteTemplateType()">
          Remove</el-button
        >
        <el-button type="danger" @click="showRemoveDialog()"> Cancel</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { mapActions, mapState } from "vuex";
import templateTypeServices from "@/services/probation/evaluation_template_type.services";
import RestrictedView from "@/components/RestrictedView";
export default {
  name: "EvaluationTemplateFormType",
  components: {
    RestrictedView,
  },
  middleware: "authentication",
  async created() {
    await this.fetchTypes();
  },
  computed: {
    ...mapState("probation", ["templateTypes"]),
  },
  data() {
    return {
      BUTTON_SUBMIT: (title) => `${title}`,
      button_submit: "Add more",
      formData: {
        typeName: "",
      },
      idTemplateType: "",
      type: 0,
      isDialogRemove: false,
      currentType: "",
      currentId: "",
      rules: {
        name: [
          {
            validator: (_rule, value, callback, _source, _options) => {
              if (value.trim().length === 0) {
                callback(new Error("Name is required"));
              } else if (value.trim().length > 50 || value.trim().length < 3) {
                callback(new Error("Name must be between 3 and 50 characters"));
              }
              callback();
            },
            trigger: ["change"],
          },
        ],
      },
    };
  },
  methods: {
    ...mapActions("probation", ["fetchTypes"]),
    editTemplateType(obj) {
      this.idTemplateType = obj.id;
      this.formData.typeName = obj.type_name;
      this.type = 1; // return update status
      this.button_submit = this.BUTTON_SUBMIT("Save");
    },

    cancelDialog() {
      this.button_submit = this.BUTTON_SUBMIT("Add more");
      this.formData.typeName = "";
    },

    async submit(type, formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          if (type === 0) {
            await this.createEvaluationType();
          } else {
            await this.updateEvaluationType();
          }
          this.cancelDialog();
        }
      });
    },

    async createEvaluationType() {
      await templateTypeServices.add({
        type_name: this.formData.typeName,
      });
      await this.fetchTypes();
    },

    async updateEvaluationType() {
      await templateTypeServices.edit(this.idTemplateType, {
        type_name: this.formData.typeName,
      });
      await this.fetchTypes();
    },

    showRemoveDialog(name, id) {
      this.currentType = name;
      this.currentId = id;
      this.isDialogRemove = !this.isDialogRemove;
    },

    async deleteTemplateType() {
      await templateTypeServices.delete(this.currentId);
      await this.fetchTypes();
      this.isDialogRemove = false;
    },
  },
};
</script>

<style lang="scss" scoped></style>
