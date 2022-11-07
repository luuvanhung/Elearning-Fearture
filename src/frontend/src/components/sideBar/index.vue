<template>
  <nav ref="dropdown" class="nav-menu-expanded" id="side-menu">
    <ul class="list-unstyled components">
      <li id="siderbar_header" class="bg-color-primary">
        <router-link to="/">
          <img src="@/static/images/logoParadox.png" class="logoParadox" />
        </router-link>
      </li>
      <div id="button_container" class="font-weight-bold">
        <container
          v-for="(attributesOfSideItem, sideItem) in sideMenu"
          :key="sideItem"
          :sideItem="sideItem"
          :attributesOfSideItem="attributesOfSideItem"
          :dropdowned="dropdowned"
          :buttonIsHighlighted="buttonIsHighlighted"
          @setDropdownedState="setDropdownedState"
        >
        </container>
      </div>
    </ul>
  </nav>
</template>
<script>
import Container from "@/components/sideBar/container.vue";
import { ROUTERS } from "@/const/router";
import { SCOPES } from "@/const/scopes";

export default {
  components: {
    Container,
  },
  methods: {
    highlightButton: function (path) {
      this.buttonIsHighlighted = {};
      this.buttonIsHighlighted[path] = true;
    },
    unHighlightAllButtons: function () {
      this.buttonIsHighlighted = {};
    },
    unDropdownAll: function () {
      this.dropdowned = {};
    },
    setDropdownedState: function (path, state) {
      this.dropdowned = {};
      this.dropdowned[path] = state;
    },
    checkRoutePath: function (route) {
      if (route.name === "Page404") {
        this.unDropdownAll();
        this.unHighlightAllButtons();
        return;
      } else {
        const path = route.path;
        for (const [sideItemTitle, sideItem] of Object.entries(this.sideMenu)) {
          if (sideItem["path"]) {
            if (path === sideItem["path"]) {
              this.highlightButton(sideItem["path"]);
              this.unDropdownAll();
              return;
            }
          } else {
            for (const [childItemTitle, childItem] of Object.entries(
              sideItem["children"]
            )) {
              if (path.includes(childItem["path"])) {
                this.setDropdownedState(sideItemTitle, true);
                this.highlightButton(childItem["path"]);
                return;
              }
            }
          }
        }
      }
      this.unDropdownAll();
      this.unHighlightAllButtons();
    },
  },
  created() {
    this.checkRoutePath(this.$route);
  },
  watch: {
    $route(to, from) {
      this.checkRoutePath(to);
    },
  },
  data() {
    return {
      dropdowned: {},
      buttonIsHighlighted: {},
      showNotification: "unread messages",
      sideMenu: {
        "Company Calendar": {
          icon: "companyCalendar.svg",
          path: ROUTERS["Calendar"],
        },
        "Employee Management": {
          icon: "employee.svg",
          children: {
            Accounts: {
              scopes: ["user:view_public_user_information_list"],
              path: ROUTERS["EmployeeList"],
              icon: "Account.svg",
            },
            Skills: {
              scopes: ["skill:view"],
              path: ROUTERS["Skill"],
              icon: "Skill.svg",
            },
            Titles: {
              scopes: ["title:view"],
              path: ROUTERS["Titles"],
              icon: "position.svg",
            },
          },
        },
        Organization: {
          icon: "Organization.svg",
          children: {
            "Organization Chart": {
              path: ROUTERS["OrganizationChart"],
              icon: "OrganizationChart.svg",
            },
            Teams: {
              scopes: ["team:view"],
              path: ROUTERS["Teams"],
              icon: "Team.svg",
            },
            "Seat Map": {
              path: ROUTERS["SeatMap"],
              icon: "SeatMap.svg",
            },
            Events: {
              path: ROUTERS["Events"],
              icon: "Event.svg",
            },
          },
        },
        "Evaluation Management": {
          icon: "ProbationManagement.svg",
          children: {
            "Form Templates": {
              scopes: ["evaluation_template:view"],
              path: ROUTERS["EvaluationTemplateManage"],
              icon: "EvaluationTemplate.svg",
            },
            Evaluations: {
              path: ROUTERS["Evaluations"],
              icon: "MyProbation.svg",
              showNotification: true,
            },
          },
          showNotification: true,
        },
        "Leave Management": {
          icon: "LeaveManagement.svg",
          children: {
            Requests: {
              path: ROUTERS["LeaveManage"],
              icon: "RequestLeave.svg",
              showNotification: true,
            },
            Reports: {
              scopes: [
                "statistic_dateoff:user",
                "statistic_dateoff:team",
                "statistic_dateoff:office",
              ],
              path: ROUTERS["LeaveReports"],
              icon: "LeaveReports.svg",
            },
            "Leave Types": {
              scopes: ["type_off:view"],
              path: ROUTERS["LeaveTypes"],
              icon: "LeaveType.svg",
            },
            "Bonus Leaves": {
              scopes: [SCOPES["BonusLeaveView"], SCOPES["BonusLeaveEdit"]],
              path: ROUTERS["BonusLeaves"],
              icon: "Account.svg",
            },
          },
          showNotification: true,
        },
        "WFH Management": {
          icon: "wfh.svg",
          children: {
            "WFH Requests": {
              path: ROUTERS["WFHManage"],
              icon: "edit.svg",
              showNotification: true,
            },
          },
          showNotification: true,
        },
        "Lunch Management": {
          icon: "LuchManagement.svg",
          children: {
            Meals: {
              path: ROUTERS["LunchCalendar"],
              icon: "Meals.svg",
            },
            Schedule: {
              scopes: ["lunches:view"],
              path: ROUTERS["LunchSchedules"],
              icon: "Schedule.svg",
            },
            Provider: {
              scopes: ["provider:view"],
              path: ROUTERS["LunchProviders"],
              icon: "Provider.svg",
            },
            "Auto Booking": {
              scopes: ["user_lunch:update_list_auto_booking"],
              path: ROUTERS["LunchBookings"],
              icon: "AutoBooking.svg",
            },
          },
        },
        "E-Learning": {
          icon: "graduation-cap-solid.svg",
          children: {
            Courses: {
              path: ROUTERS["Courses"],
              icon: "book-medical-solid.svg",
            },
            Topics: {
              path: ROUTERS["Topics"],
              icon: "iconTopic.svg",
            },
            "My Assignments": {
              path: ROUTERS["MyAssignments"],
              icon: "address-card-solid.svg",
            },
            Assignments: {
              scopes: ["elearning_assignment:edit"],
              path: ROUTERS["assignments"],
              icon: "assign-course.svg",
            },
          },
        },
        Settings: {
          icon: "Setting.svg",
          children: {
            "Integrated Application": {
              scopes: ["application:list"],
              path: ROUTERS["IntegratedApplication"],
              icon: "Integrated.svg",
            },
            Offices: {
              scopes: ["office:view"],
              path: ROUTERS["Office"],
              icon: "Ofiices.svg",
            },
            "Manage Role": {
              scopes: ["role:view"],
              path: ROUTERS["ManageRole"],
              icon: "role.svg",
            },
          },
        },
      },
    };
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/scss/sidebar.scss";
</style>
