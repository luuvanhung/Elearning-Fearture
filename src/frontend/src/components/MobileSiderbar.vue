<template>
  <nav
    class="nav-menu-collapsed"
    :class="isCollapse ? 'show-sidebar' : ''"
    id="side-menu"
  >
    <el-menu
      ref="menu"
      default-active="1"
      class="mobile-sidebar"
      :collapse="true"
      background-color="#25c9d0"
      @select="handleSelect"
    >
      <el-menu-item index="1">
        <router-link to="/" class="child-item">
          <img
            :src="require('@/static/images/companyCalendar.svg')"
            class="filter icon"
            alt="calendar"
          />
        </router-link>
        <span slot="title">Company Calendar</span>
      </el-menu-item>

      <el-submenu index="2">
        <template slot="title">
          <img
            :src="require('@/static/images/employee.svg')"
            class="filter icon"
            alt="employee"
          />
          <span slot="title">Employee Management</span>
        </template>
        <restricted-view :scopes="['user:view_public_user_information_list']">
          <template v-slot:default>
            <el-menu-item-group>
              <el-menu-item index="2-1">
                <router-link to="/employeelist" class="child-item">
                  <img
                    :src="require('@/static/images/Account.svg')"
                    class="filter icon"
                    alt="account"
                  />
                  <span class="item-title">Accounts</span>
                </router-link>
              </el-menu-item>
            </el-menu-item-group>
          </template>
        </restricted-view>

        <restricted-view :scopes="['skill:view']">
          <template v-slot:default>
            <el-menu-item-group>
              <el-menu-item index="2-2">
                <router-link to="/skill" class="child-item">
                  <img
                    :src="require('@/static/images/Skill.svg')"
                    class="filter icon"
                    alt="skill"
                  />
                  <span class="item-title">Skills</span>
                </router-link>
              </el-menu-item>
            </el-menu-item-group>
          </template>
        </restricted-view>
      </el-submenu>

      <el-submenu index="3">
        <template slot="title">
          <img
            :src="require('@/static/images/Organization.svg')"
            class="filter icon"
            alt="organization"
          />
          <span slot="title">Organization</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="3-1">
            <router-link to="/organization-chart" class="child-item">
              <img
                :src="require('@/static/images/OrganizationChart.svg')"
                class="filter icon"
                alt="organization chart"
              />
              <span class="item-title">Organization Chart</span>
            </router-link>
          </el-menu-item>
        </el-menu-item-group>
        <restricted-view :scopes="['team:view']">
          <template v-slot:default>
            <el-menu-item-group>
              <el-menu-item index="3-2">
                <router-link to="/teams" class="child-item">
                  <img
                    :src="require('@/static/images/Team.svg')"
                    class="filter icon"
                    alt="team"
                  />
                  <span class="item-title">Teams</span>
                </router-link>
              </el-menu-item>
            </el-menu-item-group>
          </template>
        </restricted-view>

        <el-menu-item-group>
          <el-menu-item index="3-3">
            <router-link to="/seat-map" class="child-item">
              <img
                :src="require('@/static/images/SeatMap.svg')"
                class="filter icon"
                alt="seat map"
              />
              <span class="item-title">Seat Map</span>
            </router-link>
          </el-menu-item>
        </el-menu-item-group>

        <el-menu-item-group>
          <el-menu-item index="3-4">
            <router-link to="/events" class="child-item">
              <img
                :src="require('@/static/images/Event.svg')"
                class="filter icon"
                alt="event"
              />
              <span class="item-title">Events</span>
            </router-link>
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>

      <el-submenu index="4">
        <template slot="title">
          <img
            :src="require('@/static/images/LeaveManagement.svg')"
            class="filter icon"
            alt="leave management"
          />
          <span slot="title">Leave Management</span>
        </template>

        <el-menu-item-group>
          <el-menu-item index="4-1">
            <router-link to="/leaves" class="child-item">
              <img
                :src="require('@/static/images/RequestLeave.svg')"
                class="filter icon"
                alt="request leave"
              />
              <span class="item-title">Request</span>
            </router-link>
          </el-menu-item>
        </el-menu-item-group>
        <restricted-view
          :scopes="[
            'statistic_dateoff:user',
            'statistic_dateoff:team',
            'statistic_dateoff:office',
          ]"
        >
          <template v-slot:default>
            <el-menu-item-group>
              <el-menu-item index="4-2">
                <router-link to="/leave-reports" class="child-item">
                  <img
                    :src="require('@/static/images/LeaveReports.svg')"
                    class="filter icon"
                    alt="leave reports"
                  />
                  <span class="item-title">Reports</span>
                </router-link>
              </el-menu-item>
            </el-menu-item-group>
          </template>
        </restricted-view>
        <restricted-view :scopes="['type_off:view']">
          <template v-slot:default>
            <el-menu-item-group>
              <el-menu-item index="4-3">
                <router-link to="/leave-types" class="child-item">
                  <img
                    :src="require('@/static/images/LeaveType.svg')"
                    class="filter icon"
                    alt="leave types"
                  />
                  <span class="item-title">Leave Types</span>
                </router-link>
              </el-menu-item>
            </el-menu-item-group>
          </template>
        </restricted-view>
        <restricted-view :scopes="['bonus_leave:view', 'bonus_leave:edit']">
          <template v-slot:default>
            <el-menu-item-group>
              <el-menu-item index="4-3">
                <router-link to="/bonus-leaves" class="child-item">
                  <img
                    :src="require('@/static/images/Account.svg')"
                    class="filter icon"
                    alt="leave bonus"
                  />
                  <span class="item-title">Bonus Leave</span>
                </router-link>
              </el-menu-item>
            </el-menu-item-group>
          </template>
        </restricted-view>
      </el-submenu>

      <el-submenu index="5">
        <template slot="title">
          <img
            :src="require('@/static/images/LuchManagement.svg')"
            class="filter icon"
            alt="luch management"
          />
          <span slot="title">Lunch Management</span>
        </template>

        <el-menu-item-group>
          <el-menu-item index="5-1">
            <router-link to="/lunches" class="child-item">
              <img
                :src="require('@/static/images/Meals.svg')"
                class="filter icon"
                alt="lunches"
              />
              <span class="item-title">Meals</span>
            </router-link>
          </el-menu-item>
        </el-menu-item-group>
        <restricted-view :scopes="['lunches:view']">
          <template v-slot:default>
            <el-menu-item-group>
              <el-menu-item index="5-2">
                <router-link to="/lunch-schedules" class="child-item">
                  <img
                    :src="require('@/static/images/Schedule.svg')"
                    class="filter icon"
                    alt="lunch schedules"
                  />
                  <span class="item-title">Schedule</span>
                </router-link>
              </el-menu-item>
            </el-menu-item-group>
          </template>
        </restricted-view>
        <restricted-view :scopes="['provider:view']">
          <template v-slot:default>
            <el-menu-item-group>
              <el-menu-item index="5-3">
                <router-link to="/lunch-providers" class="child-item">
                  <img
                    :src="require('@/static/images/Provider.svg')"
                    class="filter icon"
                    alt="lunch providers"
                  />
                  <span class="item-title">Provider</span>
                </router-link>
              </el-menu-item>
            </el-menu-item-group>
          </template>
        </restricted-view>

        <restricted-view :scopes="['user_lunch:update_list_auto_booking']">
          <el-menu-item-group>
            <el-menu-item index="5-4">
              <router-link to="/lunch-bookings" class="child-item">
                <img
                  :src="require('@/static/images/AutoBooking.svg')"
                  class="filter icon"
                  alt="lunch bookings"
                />
                <span class="item-title">Auto Booking</span>
              </router-link>
            </el-menu-item>
          </el-menu-item-group>
        </restricted-view>
      </el-submenu>

      <el-submenu index="6">
        <template slot="title">
          <img
            :src="require('@/static/images/Setting.svg')"
            class="filter icon"
            alt="setting"
          />
          <span slot="title">Settings</span>
        </template>

        <restricted-view :scopes="['application:list']">
          <el-menu-item-group>
            <el-menu-item index="6-1">
              <router-link
                to="/setting/integrated-application"
                class="child-item"
              >
                <img
                  :src="require('@/static/images/Integrated.svg')"
                  class="filter icon"
                  alt="integrated application"
                />
                <span class="item-title">Integrated Application</span>
              </router-link>
            </el-menu-item>
          </el-menu-item-group>
        </restricted-view>
        <restricted-view :scope="['office:view']">
          <template v-slot:default>
            <el-menu-item-group>
              <el-menu-item index="6-2">
                <router-link to="/setting/offices" class="child-item">
                  <img
                    :src="require('@/static/images/Ofiices.svg')"
                    class="filter icon"
                    alt="offices"
                  />
                  <span class="item-title">Offices</span>
                </router-link>
              </el-menu-item>
            </el-menu-item-group>
          </template>
        </restricted-view>

        <restricted-view :scopes="['role:view']">
          <el-menu-item-group>
            <el-menu-item index="6-3">
              <router-link to="/roles" class="child-item">
                <img
                  :src="require('@/static/images/role.svg')"
                  class="filter icon"
                  alt="roles"
                />
                <span class="item-title">Manage Role</span>
              </router-link>
            </el-menu-item>
          </el-menu-item-group>
        </restricted-view>
      </el-submenu>
    </el-menu>
  </nav>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import RestrictedView from "./RestrictedView";

export default {
  name: "id_sidebar",
  components: {
    RestrictedView,
  },
  data() {
    return {
      checkSetting: false,
      checkLunch: false,
      checkLeave: false,
      checkOrganization: false,
      checkEmployee: false,
      buttonIsHighlighted: [],
    };
  },
  computed: {
    ...mapGetters({
      showNotification: "showNotification",
      isCollapse: "value",
    }),
  },
  watch: {
    $route: "fetchData",
    isCollapse: {
      handler() {
        this.checkEmployee = false;
        this.checkSetting = false;
        this.checkOrganization = false;
        this.checkLunch = false;
        this.checkLeave = false;
      },
      deep: true,
    },
  },
  methods: {
    fetchData() {},
    ...mapActions(["changeValue"]),
    handleSelect() {
      this.changeValue();
    },
  },
};
</script>
<style lang="scss">
@import "../assets/scss/mobile-sidebar.scss";
</style>
