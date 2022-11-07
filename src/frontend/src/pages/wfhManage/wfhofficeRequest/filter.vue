<template>
  <div class="search-fields">
    <div style="width: 25%">
      <el-input
        placeholder="Search name or email"
        v-model="contentSearch.name_or_email"
        clearable
        @keyup.enter.native="search(1)"
      />
    </div>
    <div>
      <el-form>
        <el-form-item>
          <el-date-picker
            v-model="contentSearch.date"
            type="daterange"
            range-separator="-"
            start-placeholder="Start date"
            end-placeholder="End date"
          >
          </el-date-picker>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import RequestWfhService from "@/services/wfh_management/request_wfh/request_wfh.services";
import moment from "moment";
export default {
  props: ["page_size"],
  data() {
    return {
      contentSearch: {
        name_or_email: "",
        date: [],
      },
    };
  },
  watch: {
    "contentSearch.date": function () {
      this.search(1);
    },
  },
  methods: {
    async search(page = 1) {
      let name_or_email = this.contentSearch.name_or_email.trim();
      let fromDate = null;
      let toDate = null;
      if (this.contentSearch.date) {
        fromDate = this.format_date(this.contentSearch.date[0]);
        toDate = this.format_date(this.contentSearch.date[1]);
      }
      const responseData = await RequestWfhService.search(
        name_or_email,
        fromDate,
        toDate,
        page,
        this.page_size
      );
      if (responseData && responseData.data) {
        this.$emit("loadData", responseData.data, true);
      }
    },
    format_date(value) {
      if (value) {
        return moment(String(value)).format("YYYY-MM-DD");
      }
    },
  },
  updated() {
    if (!this.contentSearch.name_or_email) {
      this.search(1);
    }
  },
};
</script>

<style scoped>
.search-fields {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 20px;
}
</style>
