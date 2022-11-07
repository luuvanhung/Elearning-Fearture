<template>
  <div style="padding: 15px">
    <div class="d-flex justify-content-end mb-3" style="gap: 10px">
      <el-button type="success" @click="handleClick('Approved')">
        Approve
      </el-button>
      <el-button
        type="danger"
        @click="handleClick('Rejected')"
        style="margin: 0"
      >
        Reject
      </el-button>
      <restricted-view :scopes="['request_off:delete']">
        <el-button type="danger" @click="showDialogConfirmDelete()">
          Delete
        </el-button>
      </restricted-view>
    </div>
    <el-dialog title="Delete request" :visible.sync="dialogConfirmDelete">
      <div class="text-center text-danger">
        <h2>Do you want to delete these requests?</h2>
      </div>
      <div class="mt-3 text-center">
        <el-button type="primary" @click="handleClick('Delete')"
          >Confirm</el-button
        >
        <el-button type="danger" @click="dialogConfirmDelete = false"
          >Cancel</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import RestrictedView from "@/components/RestrictedView";
import ManagementLeaveService from "@/services/leave_management/managementLeave.service";
import { ACTION, STATUS } from "@/const/actions";

export default {
  name: "Button",
  components: {
    RestrictedView,
  },

  data() {
    return {
      dialogConfirmDelete: false,
      action: "",
    };
  },

  props: {
    leaveRequestsUpdate: Array,
    lastPageCount: Number,
    page: Number,
    searchData: Object,
  },

  computed: {
    requestOffIds() {
      return (
        this.action === ACTION.delete
          ? this.leaveRequestsUpdate
          : this.leaveRequestsUpdate.filter(
              (request) =>
                request.status === STATUS.pending ||
                request.status === STATUS.canceling
            )
      ).map((request) => request.id);
    },
  },

  methods: {
    async handleClick(action) {
      this.action = action;
      let page = this.page;
      if (
        this.lastPageCount === this.requestOffIds.length &&
        this.action === ACTION.delete
      ) {
        page -= 1;
      }
      page = page === 0 ? 1 : page;
      if (this.requestOffIds.length > 0) {
        await ManagementLeaveService.actionRequest({
          action: this.action,
          comment: "",
          request_off_ids: this.requestOffIds,
        });
        this.dialogConfirmDelete = false;
        await this.$emit("searchRequest", page, this.searchData);
      } else {
        let message =
          "You have to select at least one row have status is Pending or Canceling";
        this.$toast.warning(message);
      }
    },

    showDialogConfirmDelete() {
      this.action = ACTION.delete;
      if (this.requestOffIds.length > 0) {
        this.dialogConfirmDelete = true;
      } else {
        this.$toast.warning("You have to select at least one row");
      }
    },
  },
};
</script>
