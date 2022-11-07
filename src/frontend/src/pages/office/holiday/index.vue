<template>
  <div>
    <div class="row">
      <div class="col-12">
        <div class="border-taskbar p-2">
          <div class="col-xl-4">
            <el-col class="mb-2">
              <el-date-picker
                v-model="formData.dates"
                type="daterange"
                align="right"
                class="calendar"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                start-placeholder="Start date"
                end-placeholder="End date"
              >
              </el-date-picker>
            </el-col>
            <div class="row">
              <div class="col-4">
                <el-checkbox v-model="formData.repeat" class="mt-1">
                  Repeat
                </el-checkbox>
              </div>
              <div class="col-8">
                <el-input
                  size="small"
                  placeholder="Count"
                  v-model="formData.count"
                  v-if="formData.repeat"
                >
                </el-input>
              </div>
            </div>
          </div>
          <div class="col-xl-6">
            <el-input placeholder="Title" class="mb-2" v-model="formData.title">
            </el-input>
            <el-input
              type="textarea"
              :autosize="{ minRows: 3, maxRows: 5 }"
              placeholder="Descriptions"
              v-model="formData.descriptions"
            >
            </el-input>
          </div>
          <div
            class="col-xl-2 d-flex justify-content-center align-items-center position-relative mt-3 mt-xl-0"
          >
            <div
              v-if="this.isEditTable"
              class="d-flex justify-content-center align-items-cente"
            >
              <el-button type="info" size="medium" @click="cancel()"
                >Cancel
              </el-button>
              <el-button type="primary" size="medium" @click="saveData()"
                >Save
              </el-button>
            </div>
            <el-button
              v-show="
                $store.state.scope.tokenInfo.scope.includes('office:edit')
              "
              type="primary"
              v-else
              size="medium"
              icon="el-icon-plus"
              @click="addData()"
              >Add
            </el-button>
            <el-button
              type="warn"
              size="mini"
              class="btn-sync"
              @click="syncData()"
            >
              <font-awesome-icon :icon="['fas', 'sync']"></font-awesome-icon>
            </el-button>
          </div>
        </div>
      </div>
      <div class="col-12 mt-3">
        <el-table
          :data="dataTable"
          :header-row-style="{ textAlign: 'center' }"
          :cell-style="{ textAlign: 'center' }"
          stripe
          header-cell-class-name="bg-header-table"
          style="width: 100%"
        >
          <el-table-column prop="start_date" label="Start Date">
          </el-table-column>
          <el-table-column prop="end_date" label="End Date"> </el-table-column>
          <el-table-column prop="title" label="Title"> </el-table-column>
          <el-table-column prop="descriptions" label="Descriptions">
          </el-table-column>
          <el-table-column prop="id" label="Action" width="200">
            <template slot-scope="scope">
              <restricted-view :scopes="['office:edit']">
                <template v-slot:default>
                  <img
                    :src="require('@/static/images/IconEdit.svg')"
                    class="cursor-button mr-1"
                    @click="editData(scope.$index)" />
                  <img
                    :src="require('@/static/images/IconDelete.svg')"
                    class="cursor-button ml-1"
                    @click="deleteData(scope.$index)"
                /></template>
              </restricted-view>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>
<script>
import holidayService from "@/services/office/holiday.service.js";
import message from "@/services/office/responseMessage.js";
import RestrictedView from "@/components/RestrictedView";

export default {
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  data() {
    return {
      dataTable: [],
      formData: {
        dates: [],
        startDate: "",
        endDate: "",
        count: "",
        repeat: false,
        title: "",
        descriptions: "",
      },
      officeId: null,
      isEditTable: false,
      currentTableIndex: null,
    };
  },
  methods: {
    async getData() {
      this.officeId = this.$route.params.id;
      let holidays = await holidayService.get(this.officeId);
      this.dataTable = holidays.data.results;
    },
    async syncData() {
      try {
        let response = await holidayService.sync(this.officeId);
        if (response.status == 201) {
          await this.getData();
        }
      } catch (error) {
        this.$toast.error("Sync Failed");
      }
    },
    async addData() {
      try {
        if (!this.formData.dates || !this.formData.title) {
          return this.$toast.error(message.VALIDATION);
        }

        const dataForm = new FormData();
        dataForm.append("start_date", this.formData.dates[0]);
        dataForm.append("end_date", this.formData.dates[1]);
        dataForm.append("office", this.officeId);
        dataForm.append("title", this.formData.title);
        dataForm.append("descriptions", this.formData.descriptions);
        dataForm.append("repeat", this.formData.repeat);
        if (this.formData.repeat) {
          dataForm.append("count", this.formData.count);
        }

        const responseData = await holidayService.create(
          this.officeId,
          dataForm
        );

        if (responseData.status == 201) {
          !this.isEditTable ? this.$toast.success("Created Successfully") : "";
          this.dataTable.push(responseData.data);
        }
        this.cancel();
      } catch (error) {
        let errorContent =
          error.response.status == 400 && error.response.data
            ? error.response.data
            : "Create Failed";
        this.$toast.error(errorContent);
      }
    },
    editData(index) {
      this.isEditTable = true;
      this.currentTableIndex = index;
      Object.assign(this.formData, this.dataTable[index]);
      this.formData.dates = [];
      this.formData.dates.push(this.dataTable[index].start_date);
      this.formData.dates.push(this.dataTable[index].end_date);
    },
    cancel() {
      this.isEditTable = false;
      this.formData.dates = [];
      (this.formData.count = ""), (this.formData.descriptions = "");
      this.formData.title = "";
      this.formData.repeat = false;
    },

    async saveData() {
      try {
        if (!this.formData.dates || !this.formData.title) {
          return this.$toast.error(message.VALIDATION);
        }
        let oldData = this.dataTable[this.currentTableIndex];
        const dataForm = new FormData();
        let responseData = null;
        let currentYear = new Date().getFullYear();
        let endDate = new Date(oldData.end_date);
        let startDate = new Date(oldData.start_date);
        if (
          oldData.repeat &&
          (oldData.start_date != this.formData.dates[0] ||
            oldData.end_date != this.formData.dates[1]) &&
          currentYear >= startDate.getFullYear()
        ) {
          await this.addData();
          let count = currentYear - oldData.start_year;
          endDate.setFullYear(
            oldData.start_year +
              (endDate.getFullYear() - startDate.getFullYear())
          );
          startDate.setFullYear(oldData.start_year);
          dataForm.append("office", this.officeId);
          dataForm.append("start_date", this.formatDate(startDate));
          dataForm.append("title", oldData.title);
          dataForm.append("descriptions", oldData.descriptions);
          dataForm.append("end_date", this.formatDate(endDate));
          dataForm.append("repeat", count == 0 ? false : true);
          dataForm.append("count", count);
          responseData = await holidayService.update(
            this.officeId,
            this.formData.id,
            dataForm
          );
        } else {
          dataForm.append("start_date", this.formData.dates[0]);
          dataForm.append("end_date", this.formData.dates[1]);
          dataForm.append("office", this.officeId);
          dataForm.append("title", this.formData.title);
          dataForm.append("descriptions", this.formData.descriptions);
          dataForm.append("repeat", this.formData.repeat);
          if (this.formData.repeat) {
            dataForm.append("count", this.formData.count);
          }
          responseData = await holidayService.update(
            this.officeId,
            this.formData.id,
            dataForm
          );
        }

        if (responseData.status == 200) {
          this.$toast.success("Updated Successfully");
          if (
            oldData.repeat &&
            (oldData.start_date != this.formData.dates[0] ||
              oldData.end_date != this.formData.dates[1]) &&
            currentYear >= startDate.getFullYear()
          ) {
            this.dataTable.splice(this.currentTableIndex, 1);
          } else {
            Object.assign(oldData, responseData.data);
          }
        }
        this.cancel();
      } catch (error) {
        let errorContent =
          error.response?.status == 400
            ? error.response?.data
            : "Update Failed";
        this.$toast.error(errorContent);
      }
    },

    formatDate(date) {
      var d = new Date(date),
        month = "" + (d.getMonth() + 1),
        day = "" + d.getDate(),
        year = d.getFullYear();
      if (month.length < 2) month = "0" + month;
      if (day.length < 2) day = "0" + day;
      return [year, month, day].join("-");
    },
    async deleteData(index) {
      try {
        let holidayId = this.dataTable[index].id;
        const responseData = await holidayService.delete(
          this.officeId,
          holidayId
        );
        if (responseData.status == 204) {
          this.$toast.success("Deleted Successfully");
          this.dataTable.splice(index, 1);
        }
      } catch (error) {
        let errorContent =
          error.response.status == 400 && error.response.data
            ? error.response.data
            : "Delete Failed";
        this.$toast.error(errorContent);
      }
    },
  },
  async created() {
    return this.getData();
  },
};
</script>

<style lang="scss" scoped>
@import "index.scss";
</style>
