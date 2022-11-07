<template>
  <div class="mt-3 mb-5">
    <div class="actions">
      <restricted-view :scopes="['evaluation_template:create']">
        <el-button
          id="btn-add-template"
          type="primary"
          icon="el-icon-circle-plus"
          @click="addNewEvaluationTemplate"
        >
          New Evaluation Form Template
        </el-button>
      </restricted-view>
    </div>
    <el-table
      highlight-current-row
      :data="template.results"
      style="width: 100%"
      header-cell-class-name="bg-header-table"
      border
    >
      <el-table-column type="index" sortable align="center" width="50">
      </el-table-column>

      <el-table-column sortable prop="name" label="Name" align="center">
      </el-table-column>
      <el-table-column sortable label="Type" width="200" align="center">
        <template v-slot="scope">
          {{
            templateTypes.find((type) => type.id === scope.row.type).type_name
          }}
        </template>
      </el-table-column>
      <el-table-column
        sortable
        prop="created_at"
        :formatter="formatter"
        label="Create at"
        width="130"
        align="center"
      >
      </el-table-column>
      <el-table-column
        sortable
        prop="updated_at"
        :formatter="formatter"
        label="Update at"
        width="130"
        align="center"
      >
      </el-table-column>
      <el-table-column sortable label="Office" align="center" width="180">
        <template v-slot="scope">
          {{ offices.find((office) => office.id === scope.row.office).name }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="Active" width="80" align="center">
        <template v-slot="scope">
          <restricted-view :scopes="['evaluation_template:edit']">
            <el-switch
              active-color="#25c9d0"
              inactive-color="#ff4949"
              v-model="scope.row.status"
              @change="switchActive(scope.row)"
            >
            </el-switch>
          </restricted-view>
        </template>
      </el-table-column>
      <el-table-column label="Action" width="120" align="center">
        <template v-slot="scope">
          <restricted-view :scopes="['evaluation_template:edit']">
            <el-button
              circle
              style="cursor: pointer"
              @click="redirectToEditPage(scope.row.id)"
              type="primary"
              icon="el-icon-edit"
              title="Edit Probation Template"
            ></el-button>
            <el-button
              circle
              style="cursor: pointer"
              type="danger"
              icon="el-icon-delete"
              @click="deleteRequest(scope.row.id)"
              title="Delete Probation Template"
            />
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
      <span>Do you want to delete this template</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="deleteItem()">Confirm</el-button>
      </span>
    </el-dialog>
    <div class="d-flex justify-content-center mt-5">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-size="template.page_size"
        :current-page="template.current"
        :total="template.count"
        @current-change="changePages"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import probationService from "@/services/probation/probation";
import RestrictedView from "@/components/RestrictedView";
import { BOOLEANS } from "@/const/boolean";
import { mapState, mapActions } from "vuex";

export default {
  name: "MyEvaluationTemplate",
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  async created() {
    await this.fetchOffices();
    await this.fetchTypes();
    await this.asyncDataActive();
    await this.fetchTitles();
  },
  computed: {
    ...mapState("probation", ["template", "offices", "templateTypes"]),
  },
  data() {
    return {
      page: 1,
      pageSize: 12,
      dialogVisible: false,
      checkActive: true,
      table_data: [],
      delete_id: "",
    };
  },
  methods: {
    ...mapActions("probation", [
      "fetchOffices",
      "fetchTitles",
      "setEvaluationTemplates",
      "fetchTypes",
    ]),
    addNewEvaluationTemplate() {
      window.location.href =
        "/evaluation-form-templates/new-evaluation-form-template";
    },
    formatter(row, column) {
      let date = new Date(row[column.property]);
      return date.toLocaleDateString();
    },

    async asyncDataActive() {
      let response = await probationService.getManagementTemplate(
        this.page,
        this.pageSize
      );
      if (response && response.status === 200 && response.data) {
        await this.setEvaluationTemplates(response);
      }
    },

    async changePages(page) {
      let response = await probationService.getManagementTemplate(
        page,
        this.pageSize
      );
      if (response && response.status === 200 && response.data) {
        await this.setEvaluationTemplates(response);
      }
    },

    switchActive(obj) {
      probationService.handleTemplateActive(obj.id).then((res) => {
        if (res.status === 200) {
          this.$toast.success(BOOLEANS[res.data.status]);
        } else {
          this.$toast.error("An error occurred");
        }
      });
    },

    redirectToEditPage(id) {
      window.location.href = "/evaluation-form-templates/" + id;
    },

    deleteRequest(id) {
      this.dialogVisible = true;
      this.delete_id = id;
    },

    async deleteItem() {
      if (this.delete_id !== "") {
        this.dialogVisible = false;
        let res = await probationService.deleteEvaluationTemplate(
          this.delete_id
        );
        if (res.status === 204) {
          this.$nextTick(() => {
            this.$toast.success(
              "Your evaluation template was deleted successfully"
            );
          });
          await this.asyncDataActive();
        } else {
          this.$toast.error("Your evaluation template was deleted error");
        }
      }
    },
  },
};
</script>

<style lang="scss">
@import "./myEvaluationTemplate.scss";
</style>
