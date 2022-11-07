<template>
  <div>
    <div class="mb-3">
      <strong type="success">
        Users that will be added to the System:
        <span style="color: #67c23a; font-size: 15px">{{
          tableData.length
        }}</span> </strong
      ><br />
      <strong type="warning">
        Users that is already existed and active:
        <span style="color: #e6a23c; font-size: 15px">
          {{ numActive }}
        </span> </strong
      ><br />
      <strong type="error">
        Users that is already existed and deactivate:
        <span style="color: #f56c6c; font-size: 15px"
          >{{ numDeactivate }}
        </span> </strong
      ><br />
    </div>
    <el-table
      class="table-responsive"
      ref="excelTable"
      highlight-current-row
      :data="tableData"
      @row-click="handleRowClick"
      @selection-change="onUserSelectedChange"
      border
    >
      <el-table-column type="selection" align="center" />
      <el-table-column align="center" :min-width="200" label="Name" fixed>
        <template #default="scope">
          {{ scope.row.values[contactCols.name] }}
        </template>
      </el-table-column>
      <el-table-column align="center" :min-width="200" label="Team / Squad">
        <template #default="scope">
          {{ scope.row.values[contactCols.team] }}
        </template>
      </el-table-column>
      <el-table-column align="center" :min-width="220" label="Role">
        <template #default="scope">
          {{ scope.row.values[contactCols.role] }}
        </template>
      </el-table-column>
      <el-table-column align="center" :min-width="250" label="Email">
        <template #default="scope">
          {{ scope.row.values[contactCols.email] }}
        </template>
      </el-table-column>
      <el-table-column
        :min-width="180"
        align="center"
        label="Status"
        fixed="right"
      >
        <template #default="scope">
          <el-tag :type="makeColorStatus(scope)" disable-transitions>
            {{ scope.row.values[contactCols.status] }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "ConfirmAddToSystemBox",
  props: ["defaultValue", "contactCols"],
  data() {
    return {
      selectedUser: [],
    };
  },
  mounted() {
    if (this.$refs.excelTable) {
      this.$refs.excelTable.toggleAllSelection();
    }
  },
  computed: {
    tableData() {
      return (
        this.defaultValue &&
        this.defaultValue.filter(({ values, _index }) => {
          return values[this.contactCols.status] === "Does not exist";
        })
      );
    },
    numActive() {
      return (
        this.defaultValue &&
        this.defaultValue.filter(({ values, _index }) => {
          return values[this.contactCols.status] === "Active";
        }).length
      );
    },
    numDeactivate() {
      return (
        this.defaultValue &&
        this.defaultValue.filter(({ values, _index }) => {
          return values[this.contactCols.status] === "Deactivate";
        }).length
      );
    },
  },
  methods: {
    handleRowClick(row) {
      this.$refs["excelTable"].toggleRowSelection(row);
    },

    onUserSelectedChange(val) {
      this.selectedUser = val;
    },

    makeColorStatus(scope) {
      switch (scope.row.values[this.contactCols.status]) {
        case "Active":
          return "success";
        case "Deactivate":
          return "danger";
        case "Does not exist":
          return "warning";
      }
    },
  },
  watch: {
    selectedUser: {
      deep: true,
      handler: function () {
        this.$emit("input", this.selectedUser);
      },
    },
  },
};
</script>

<style scoped></style>
