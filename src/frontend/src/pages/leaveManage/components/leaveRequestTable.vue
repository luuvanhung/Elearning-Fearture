<template>
  <div>
    <el-table
      highlight-current-row
      @selection-change="handleUpdateStatusLeaveRequest"
      :data="requestOffsData"
      header-cell-class-name="bg-header-table"
      border
    >
      <el-table-column type="selection" align="center"></el-table-column>
      <el-table-column
        sortable
        prop="profile.name"
        label="Employee"
        align="center"
      >
      </el-table-column>
      <el-table-column
        sortable
        prop="profile.email"
        label="Email"
        align="center"
      >
      </el-table-column>
      <el-table-column label="Date Off" width="200" align="center">
        <template v-slot="scope">
          <div v-for="dateOff in scope.row.date_off" :key="dateOff.id">
            {{ dateOff.date }} ({{ dateOff.type }})
          </div>
        </template>
      </el-table-column>
      <el-table-column
        sortable
        prop="leave_type.name"
        label="Leave Type"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="reason"
        label="Reason"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="request_detail[0]"
        label="Assigned"
        align="center"
        v-if="isOfficer"
      ></el-table-column>
      <el-table-column
        prop="created_at"
        label="Created at"
        align="center"
      ></el-table-column>
      <el-table-column sortable prop="status" label="Status" align="center">
        <template v-slot="scope">
          <el-tag type="danger" v-if="scope.row.status === 'Rejected'">
            Rejected
          </el-tag>
          <el-tag type="success" v-else-if="scope.row.status === 'Approved'">
            Approved
          </el-tag>
          <el-tag type="warning" v-else-if="scope.row.status === 'Canceling'">
            Canceling
          </el-tag>
          <el-tag type="info" v-else-if="scope.row.status === 'Canceled'">
            Canceled
          </el-tag>
          <el-tag type="warning" v-else> Pending </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "LeaveRequestTable",
  props: {
    requestOffsData: Array,
    isOfficer: Boolean,
  },
  methods: {
    handleUpdateStatusLeaveRequest(val) {
      this.$emit("handleUpdateStatusLeaveRequest", val);
    },
  },
};
</script>
