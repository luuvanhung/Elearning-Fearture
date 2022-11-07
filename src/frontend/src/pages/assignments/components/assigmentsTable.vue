<template>
  <div>
    <el-dialog
      title="Detail progress"
      :visible.sync="dialogTableVisible"
      width="25%"
    >
      <el-tree
        :data="ProgressTrainee"
        :props="defaultProps"
        :render-content="renderContent"
      ></el-tree>
    </el-dialog>
    <el-table
      v-loading="loading"
      highlight-current-row
      :data="assignments"
      header-cell-class-name="bg-header-table"
      style="width: 100%"
      border
    >
      <el-table-column
        sortable
        prop="full_name"
        label="Employee"
        align="center"
      ></el-table-column>
      <el-table-column
        sortable
        prop="course_name"
        label="Course"
        align="center"
      ></el-table-column>
      <el-table-column label="Start Date" width="300" sortable align="center">
        <template slot-scope="scope">
          {{ formatDate(scope.row.start_date) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="due"
        label="Due Date"
        sortable
        width="300"
        align="center"
      >
        <template slot-scope="scope">
          {{ formatDate(scope.row.due_date) }}
        </template>
      </el-table-column>
      <el-table-column sortable label="Status" width="200" align="center">
        <template slot-scope="scope">
          <el-tag :type="identifyTag(scope.row.status)" disable-transitions>
            {{ scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" label="Operations" width="180">
        <template slot-scope="scope">
          <el-tooltip
            effect="light"
            :content="TOOLTIPS.edit_assignment"
            placement="top"
          >
            <el-button
              style="font-size: 20px"
              @click="handleClickEdit(scope.row)"
              type="text"
              icon="el-icon-edit"
            ></el-button>
          </el-tooltip>
          <el-tooltip
            effect="light"
            :content="TOOLTIPS.delete_assignment"
            placement="top"
          >
            <el-popconfirm
              confirm-button-text="Delete"
              cancel-button-text="No"
              title="Delete this assignment?"
              @confirm="handleClickDel(scope.row.id)"
            >
              <template slot="reference">
                <el-button
                  style="font-size: 20px"
                  type="text"
                  icon="el-icon-delete"
                />
              </template>
            </el-popconfirm>
          </el-tooltip>
          <el-tooltip
            effect="light"
            :content="TOOLTIPS.assignment_detail"
            placement="top"
          >
            <el-button
              style="font-size: 20px"
              @click="handleClickInfo(scope.row)"
              type="text"
              icon="el-icon-info"
            ></el-button>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { formatDate } from "@/utils/time";
import AssignService from "@/services/e-learning/assignment.js";
import { ASSIGNMENT_STATUSES } from "@/const/AssignmentDetail.js";
const TOOLTIPS = {
  edit_assignment: "Edit this assignment",
  delete_assignment: "Delete this assignment",
  assignment_detail: "assignment detail",
};
export default {
  data() {
    return {
      TOOLTIPS: TOOLTIPS,
      dialogTableVisible: false,
      statuses: Object.keys(ASSIGNMENT_STATUSES),
      type: ["", "success", "danger", "info", ""],
      dataTrainee: null,
      defaultProps: {
        children: "children",
        label: "label",
      },
    };
  },
  props: ["assignments", "loading"],
  methods: {
    renderContent(h, { node, data, store }) {
      return (
        <span class="custom-tree-node">
          <span>{node.label}</span>
          <span> - </span>
          <span class="el-tag el-tag el-tag--light">{data.status}</span>
        </span>
      );
    },
    handleClickInfo(row) {
      this.dataTrainee = row;
      this.dialogTableVisible = true;
    },
    identifyTag(tag) {
      let index = this.statuses.indexOf(tag);
      index = index === -1 ? 0 : index;
      return this.type[index];
    },
    async handleClickDel(id) {
      const res = await AssignService.delAssignments(id);
      if (res) {
        this.$emit("del");
      }
    },
    handleClickEdit(value) {
      const h = this.$createElement;
      this.$msgbox({
        title: "Edit assignments",
        customClass: "new",
        message: h(
          "EditAssignment",
          {
            props: {
              assignFormEdit: value,
            },
          },
          []
        ),
        roundButton: true,
        beforeClose: (action, instances, done) => {
          if (action === "confirm") {
            if (instances.$children[2].editAssignment()) {
              done();
            }
          } else {
            done();
          }
        },
      }).then(() => {});
    },
    formatDate,
    disabledDate(time) {
      return time.getTime() <= Date.now();
    },
  },
  computed: {
    ProgressTrainee() {
      if (this.dataTrainee) {
        return this.dataTrainee.assignment_chapters.reduce(
          (current, val, index) => (
            (current = [
              ...current,
              {
                label: this.dataTrainee.assignment_chapters[index].chapter_name,
                status: this.dataTrainee.assignment_chapters[index].status,
                children: this.dataTrainee.assignment_chapters[
                  index
                ].assignment_chapter_lessons.reduce(
                  (current2, val2, index2) => (
                    (current2 = [
                      ...current2,
                      {
                        label:
                          this.dataTrainee.assignment_chapters[index]
                            .assignment_chapter_lessons[index2].lesson_name,
                        status:
                          this.dataTrainee.assignment_chapters[index]
                            .assignment_chapter_lessons[index2].status,
                      },
                    ]),
                    current2
                  ),
                  []
                ),
              },
            ]),
            current
          ),
          []
        );
      }
      return null;
    },
  },
};
</script>

<style lang="scss">
.el-dialog {
  font-size: 200%;
  font-weight: bold;
}
.custom-tree-node {
  font-size: 0.9rem;
}
.el-icon-success {
  color: rgb(9, 199, 9);
}
</style>
