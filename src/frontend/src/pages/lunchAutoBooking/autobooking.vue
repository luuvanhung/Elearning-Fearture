<template>
  <restricted-view :scopes="['user_lunch:update_list_auto_booking']">
    <template v-slot:default>
      <div>
        <el-col :span="10">
          <el-row style="height: 30px"></el-row>
          <el-input
            placeholder="Search by name"
            v-model="searchEmployeeList"
            style="width: 60%"
          ></el-input>
          <el-table
            :data="dataTableLeft"
            @selection-change="updateListCheckboxNotAuto"
            stripe
            header-cell-class-name="bg-header-table"
            class="mt-2"
          >
            <el-table-column type="selection" width="42"></el-table-column>
            <el-table-column prop="name" label="Employee List">
              <template slot-scope="scope">
                {{ scope.row.name }} ({{ scope.row.personal_email }})
              </template>
            </el-table-column>
            <el-table-column width="100">
              <template slot-scope="scope">
                <el-checkbox v-model="scope.row.veggie"> Veggie </el-checkbox>
              </template>
            </el-table-column>
            <el-table-column width="42">
              <template slot-scope="scope">
                <img
                  @click="addAutoBookingLunchProfile(scope.row)"
                  class="img-action"
                  :src="require('@/static/images/send-to-right.svg')"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
        <el-col :span="4" style="min-width: 150px">
          <el-row style="height: 150px"></el-row>
          <el-row>
            <div class="text-center">
              <el-button
                type="primary"
                class="mb-3"
                icon="el-icon-caret-right"
                :disabled="listCheckBoxNotAuto.length === 0"
                @click="changeListNotAutoBooking()"
              >
              </el-button>
              <br />
              <el-button
                type="primary"
                class="mb-3"
                icon="el-icon-caret-left"
                :disabled="listCheckBoxAuto.length === 0"
                @click="changeListAutoBooking()"
              >
              </el-button>
            </div>
          </el-row>
        </el-col>
        <el-col :span="10">
          <el-row style="height: 30px"></el-row>
          <el-row>
            <el-input
              placeholder="Search by name"
              v-model="searchAutoBookingList"
              style="width: 60%"
            ></el-input>
            <el-button type="primary" class="ml-4">
              <download-excel
                :fetch="fetchDataForExportExcel"
                :fields="json_fields"
                worksheet="My Worksheet"
                title="Auto Booking Lunch"
                name="auto-booking.xls"
              >
                <font-awesome-icon :icon="['fas', 'file-export']" />
                Export file
              </download-excel>
            </el-button>
          </el-row>
          <el-table
            :data="dataTableRight"
            @selection-change="updateListCheckboxAuto"
            stripe
            header-cell-class-name="bg-header-table"
            class="mt-2"
          >
            <el-table-column width="42" type="selection"></el-table-column>
            <el-table-column prop="name" label="Auto Booking">
              <template slot-scope="scope">
                {{ scope.row.name }} ({{ scope.row.personal_email }})
              </template>
            </el-table-column>
            <el-table-column width="100">
              <template slot-scope="scope">
                <el-checkbox v-model="scope.row.veggie" disabled>
                  Veggie
                </el-checkbox>
              </template>
            </el-table-column>
            <el-table-column width="42">
              <template slot-scope="scope">
                <img
                  @click="removeAutoBookingLunchProfile(scope.row)"
                  class="img-action"
                  :src="require('@/static/images/send-to-left.svg')"
                />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </div>
    </template>
  </restricted-view>
</template>
<script>
import ProfileService from "@/services/profile/profile";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "AutoBooking",
  components: {
    RestrictedView,
  },
  data() {
    return {
      listAutoBookingLunch: [],
      listNotAutoBookingLunch: [],
      json_fields: {
        Name: "name",
        "Personal Email": "personal_email",
        "Birth day": "birth_day",
        Phone: "phone",
        "Join date": "join_date",
        Veggie: "veggie",
      },
      searchEmployeeList: "",
      searchAutoBookingList: "",
      listCheckBoxAuto: [],
      listCheckBoxNotAuto: [],
    };
  },

  created() {
    this.getListAutoBookingLunch();
  },

  computed: {
    dataTableLeft() {
      return this.listNotAutoBookingLunch.filter((data) =>
        data.name.toLowerCase().includes(this.searchEmployeeList.toLowerCase())
      );
    },

    dataTableRight() {
      return this.listAutoBookingLunch.filter((data) =>
        data.name
          .toLowerCase()
          .includes(this.searchAutoBookingList.toLowerCase())
      );
    },
  },

  methods: {
    updateListCheckboxNotAuto(val) {
      this.listCheckBoxNotAuto = val;
    },

    updateListCheckboxAuto(val) {
      this.listCheckBoxAuto = val;
    },

    async getListAutoBookingLunch() {
      const res = await ProfileService.getAutoBookingLunchProfile();
      if (res.status === 200) {
        this.listAutoBookingLunch = res.data.pfs_lunch_booking;
        this.listNotAutoBookingLunch = res.data.pfs_lunch_not_booking;
      } else {
        this.$toast.error(res.data);
      }
    },

    async addAutoBookingLunchProfile(profile) {
      try {
        const data = {
          auto_booking_lunch: true,
          profiles: [
            { ["profile_id"]: profile.id, ["veggie"]: profile.veggie },
          ],
        };
        profile.auto_booking_lunch = true;
        await ProfileService.updateListAutoBookingLunch(data);
        this.listNotAutoBookingLunch.splice(
          this.listNotAutoBookingLunch.indexOf(profile),
          1
        );
        this.listAutoBookingLunch.push(profile);
        this.$toast.success("Updated Successfully");
      } catch (e) {
        console.log(e);
        this.$toast.error("Update Failed");
      }
    },

    async removeAutoBookingLunchProfile(profile) {
      try {
        const data = {
          auto_booking_lunch: false,
          profiles: [
            { ["profile_id"]: profile.id, ["veggie"]: profile.veggie },
          ],
        };
        profile.auto_booking_lunch = false;
        await ProfileService.updateListAutoBookingLunch(data);
        this.listAutoBookingLunch.splice(
          this.listAutoBookingLunch.indexOf(profile),
          1
        );
        this.listNotAutoBookingLunch.unshift(profile);
        this.$toast.success("Updated Successfully");
      } catch (e) {
        console.log(e);
        this.$toast.error("Update Failed");
      }
    },

    fetchDataForExportExcel() {
      return this.listAutoBookingLunch;
    },

    async changeListNotAutoBooking() {
      try {
        const data = {
          auto_booking_lunch: true,
          profiles: this.listCheckBoxNotAuto.map((data) => ({
            ["profile_id"]: data.id,
            ["veggie"]: data.veggie,
          })),
        };
        await ProfileService.updateListAutoBookingLunch(data);
        await this.getListAutoBookingLunch();
        this.$toast.success("Updated Successfully");
      } catch (e) {
        console.log(e);
        this.$toast.error("Update Failed");
      }
      this.listCheckBoxNotAuto = [];
    },

    async changeListAutoBooking() {
      try {
        const data = {
          auto_booking_lunch: false,
          profiles: this.listCheckBoxAuto.map((data) => ({
            ["profile_id"]: data.id,
            ["veggie"]: data.veggie,
          })),
        };
        await ProfileService.updateListAutoBookingLunch(data);
        await this.getListAutoBookingLunch();
        this.$toast.success("Updated Successfully");
      } catch (e) {
        console.log(e);
        this.$toast.error("Update Failed");
      }
      this.listCheckBoxAuto = [];
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
