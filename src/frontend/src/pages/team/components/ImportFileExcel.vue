<template>
  <div>
    <el-row class="mt-3 mb-3 d-flex justify-content-between align-items-center">
      <div
        class="col-12 col-lg-6 mt-3 col-xl-6 ml-auto justify-xl-start d-flex justify-content-start"
      >
        <el-button
          @click="clearFilter"
          type="primary"
          v-if="tableData.length > 0"
        >
          Reset All Filters
        </el-button>
      </div>
      <div
        class="col-12 col-lg-6 mt-3 col-xl-6 ml-auto justify-xl-end d-flex justify-content-end"
      >
        <el-button
          icon="el-icon-back"
          type="primary"
          v-if="selectedUsers.length <= 0"
          class="d-flex align-items-end"
          @click="back"
        >
          Back
        </el-button>
        <el-button icon="el-icon-plus" type="primary" v-else @click="addUsers">
          Add to System
        </el-button>
      </div>
    </el-row>
    <div class="d-sm-flex gap-3 justify-content-center">
      <el-card v-if="tableData.length > 0">
        <el-table
          class="table-responsive"
          ref="excelTable"
          highlight-current-row
          height="1000"
          :data="tableData"
          @row-click="handleRowClick"
          @selection-change="onUserSelectedChange"
          :row-class-name="tableRowClassName"
          border
        >
          <el-table-column type="selection" align="center" />
          <el-table-column
            align="center"
            v-for="(col, index) in headers"
            :min-width="index === 0 ? 100 : 300"
            :label="col"
            :key="index"
            :prop="`values[${index.toString()}]`"
            :fixed="index <= contactCols.name"
          ></el-table-column>
          <el-table-column
            :min-width="200"
            align="center"
            label="Status"
            fixed="right"
            :filters="statusAccount"
            :filter-method="filterStatus"
          >
            <template v-slot="scope">
              <el-tag :type="makeColorStatus(scope)" disable-transitions>
                {{ scope.row.values[contactCols.status] }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      <el-upload
        v-if="tableData.length <= 0"
        action=""
        drag
        :on-change="handleImportExcel"
        class="el-row mt-3"
        accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      >
        <el-icon class="el-icon-upload"></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
        <div slot="tip" class="el-upload__tip text-center">
          Please input excel file (.xlsx).
        </div>
      </el-upload>
    </div>
  </div>
</template>

<script>
import XLSX from "xlsx";
import { mapActions, mapGetters } from "vuex";
import TitlesServices from "../../../services/titles/titles.services";
import UserService from "../../../services/user/user";
import TeamServices from "../../../services/team/team.services";
import SquadService from "../../../services/office/squad.service";
import DepartmentService from "../../../services/office/department.service";
import Validation from "../../../utils/validation";

export default {
  name: "ImportFileExcel",
  async created() {
    await TitlesServices.getAll().then((res) => {
      this.getListTitle(res.data);
    });
  },
  data() {
    return {
      header_index: 0,
      sending_columns: [],
      contactCols: {},
      excelData: [],
      statusAccount: [
        { text: "Active", value: "Active" },
        { text: "Deactivate", value: "Deactivate" },
        { text: "Does not exist", value: "Does not exist" },
        { text: "Email not valid", value: "Email not valid" },
      ],
      selectedUsers: [],
      listUser: [],
      listTeamsImport: [],
      colors: [],
      squads: [],
      departments: [],
      newTitles: [],
      teamData: [],
      squadData: [],
      departmentData: [],
    };
  },
  computed: {
    ...mapGetters({
      allUsers: "user/allExistedAccounts",
      allTeams: "team/listTeams",
      allSquads: "squad/listSquads",
      allDepartments: "squad/listDepartments",
      listTitle: "title/listTitle",
    }),
    headers() {
      return this.excelData && this.excelData[this.header_index];
    },
    tableData() {
      const teams = [
        ...this.teamOrSquads.filter((item) => {
          return !item.toLowerCase().includes("squad");
        }),
      ];
      return (
        this.excelData &&
        this.excelData
          .map((values, index) => {
            if (index === this.header_index) {
              values = [...this.addColumns(values)];
            } else {
              let email = values[this.contactCols.email];
              let team = values[this.contactCols.team];
              let onBoarding = values[this.contactCols.onBoarding];
              if (onBoarding) {
                values[this.contactCols.onBoarding] =
                  this.convertJoinDate(onBoarding);
              }
              let status = this.checkStatusAccount(email);
              values[this.contactCols.team] = this.fillTeam(team, teams);
              values[this.contactCols.squad] = this.fillSquad(index, team);
              values[this.contactCols.department] = this.fillDepartment(
                index,
                team
              );
              values[this.contactCols.status] = status;
            }
            return { index, values };
          })
          .slice(this.header_index + 1)
      );
    },
    allEmails() {
      return this.allUsers.map((user) => user.email);
    },
    teamOrSquads() {
      let allTitle =
        this.excelData &&
        this.excelData.map((values, index) => {
          if (index > this.header_index) {
            return values[this.contactCols.team];
          }
        });
      return allTitle.filter((item) => item !== undefined);
    },
    titlesExist() {
      return this.listTitle.map((item) => {
        return item.title;
      });
    },
  },
  methods: {
    ...mapActions({
      getListTitle: "title/updateListTitle",
    }),

    filterStatus(value, row) {
      return row.values[this.contactCols.status] === value;
    },

    fillSquad(index, team) {
      if (team && team.toLowerCase().includes("squad")) {
        this.squads.splice(0, 1, team);
        return team.split(": ")[1];
      } else {
        if (this.squads.length > 0) {
          if (this.colors[index].color === this.colors[index - 1].color) {
            return this.squads[0].split(": ")[1];
          } else {
            this.squads.pop();
          }
        }
      }
      return "N/A";
    },

    fillDepartment(index, team) {
      if (team && team.toLowerCase().includes("department")) {
        this.departments.splice(0, 1, team);
        return team.split(": ")[1];
      } else {
        if (this.departments.length > 0) {
          if (this.colors[index].color === this.colors[index - 1].color) {
            return this.departments[0].split(": ")[1];
          } else {
            this.departments.pop();
          }
        }
      }
      return "N/A";
    },

    fillTeam(team, allTeams) {
      if (!team) {
        team = allTeams[0];
        if (!this.listTeamsImport.includes(team)) {
          this.listTeamsImport.push(team);
        }
      } else {
        allTeams.unshift(team);
      }

      return team;
    },

    checkStatusAccount(email) {
      if (!Validation.validateEmail(email)) {
        return "Email not valid";
      } else if (!this.allEmails.includes(email)) {
        return "Does not exist";
      } else {
        let user = this.allUsers.find((item) => item.email === email);
        return user.active ? "Active" : "Deactivate";
      }
    },

    addColumns(columns) {
      this.contactCols = {
        ...this.contactCols,
        status: columns.length,
        department: columns.length + 1,
        squad: columns.length + 2,
      };
      return [...columns, "Status", "Department", "Squad"];
    },

    makeColorStatus(scope) {
      switch (scope.row.values[this.contactCols.status]) {
        case "Active":
          return "success";
        case "Deactivate":
          return "danger";
        case "Does not exist":
          return "warning";
        case "Email not valid":
          return "info";
      }
    },

    clearFilter() {
      this.$refs.excelTable.clearFilter();
    },

    handleError(message) {
      this.loading = false;
      this.$toast.error(message || "Failed! Please, try again!");
    },

    onUserSelectedChange(val) {
      this.selectedUsers = val;
    },

    handleRowClick(row) {
      this.$refs["excelTable"].toggleRowSelection(row);
    },

    convertJoinDate(date) {
      let dateArr = date.split(" ");
      let year = dateArr[2];
      let month = this.convertMonth(dateArr[0]);
      let day = dateArr[1].slice(0, -1);
      if (!year) {
        year = dateArr[1];
        day = "01";
      } else if (!day) {
        day = "01";
      }
      day = day.length === 1 ? `0${day}` : day;
      return `${year}-${month}-${day}`;
    },

    convertMonth(month) {
      switch (month) {
        case "Jan":
        case "January":
          return "01";
        case "Feb":
        case "February":
          return "02";
        case "Mar":
        case "March":
          return "03";
        case "Apr":
        case "April":
          return "04";
        case "May":
          return "05";
        case "Jun":
        case "June":
          return "06";
        case "Jul":
        case "July":
          return "07";
        case "Aug":
        case "August":
          return "08";
        case "Sep":
        case "September":
          return "09";
        case "Oct":
        case "October":
          return "10";
        case "Nov":
        case "November":
          return "11";
        case "Dec":
        case "December":
          return "12";
      }
    },

    addUsers() {
      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm Add Users",
        message: h(
          "ConfirmAddToSystemBox",
          {
            props: {
              defaultValue: this.selectedUsers,
              contactCols: this.contactCols,
            },
            on: {
              input: (value) => {
                this.listUser = value;
              },
            },
          },
          []
        ),
        roundButton: true,
        customClass: "confirmForm",
      }).then(() => {
        if (this.listUser.length > 0) {
          this.confirmAddTitles(this.listUser);
        } else {
          this.$alert("You are choosing NO ONE!", "Warning", {
            confirmButtonText: "OK",
            callback: (action) => {
              this.$message({
                type: "warning",
                message: `action: ${action}`,
              });
            },
          });
        }
      });
    },

    confirmAddTitles(selectedUsers) {
      let titles = [];
      selectedUsers.forEach(({ _index, values }) => {
        let title = values[this.contactCols.role];
        if (title) {
          title.split("/").forEach((item) => {
            let temp = item.split("Developer")[0].trim();
            if (!titles.includes(temp) && !this.titlesExist.includes(temp)) {
              titles.push(temp);
            }
          });
        }
      });
      this.newTitles = titles;
      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm Add Titles",
        message: h(
          "ConfirmAddNewTitle",
          {
            props: {
              defaultValue: [...titles],
            },
            on: {
              input: (value) => {
                this.newTitles = [...value];
              },
            },
          },
          []
        ),
        roundButton: true,
        customClass: "confirmForm",
      }).then(async () => {
        if (this.newTitles.length > 0) {
          await TitlesServices.importTitles({ titles: this.newTitles });
        }
        const loading = this.$loading({
          lock: true,
          text: "Processing",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
        });
        await this.importUsers(selectedUsers)
          .then(() => {
            loading.close();
            this.$toast.success("Import users successfully!");
            this.confirmImportTeams();
          })
          .catch(() => {
            loading.close();
            this.$alert("Something went wrong!", "Warning", {
              confirmButtonText: "OK",
              callback: (action) => {
                this.$message({
                  type: "error",
                  message: `action: ${action}`,
                });
              },
            });
          });
      });
    },

    confirmImportTeams() {
      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm Add Teams",
        message: h(
          "ConfirmAddNewTeam",
          {
            props: {
              newUsers: [...this.selectedUsers],
              contactCols: this.contactCols,
            },
            on: {
              input: (value) => {
                this.teamData = [...value];
              },
            },
          },
          []
        ),
        roundButton: true,
        customClass: "confirmForm",
      }).then(async () => {
        const loading = this.$loading({
          lock: true,
          text: "Processing",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
        });
        if (this.teamData.length > 0) {
          const data = this.covertTeamData(this.teamData);
          await TeamServices.importTeams(data);
        }
        loading.close();
        this.confirmImportSquads();
      });
    },

    covertTeamData(teamData) {
      let data = [];
      teamData.forEach(({ team, members }) => {
        let temp = {
          team: team,
          members: members.map((member) => {
            return member.reduce((allAttribute, attribute, index) => {
              return {
                ...allAttribute,
                [this.getKeyByValue(this.contactCols, index)]: attribute,
              };
            }, {});
          }),
        };
        data.push(temp);
      });
      return data;
    },

    getKeyByValue(object, value) {
      return Object.keys(object).find((key) => object[key] === value);
    },

    confirmImportSquads() {
      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm Add Squads",
        message: h(
          "ConfirmAddNewSquad",
          {
            props: {
              newUsers: [...this.selectedUsers],
              newTeams: [...this.teamData],
              contactCols: this.contactCols,
            },
            on: {
              input: (value) => {
                this.squadData = [...value];
              },
            },
          },
          []
        ),
        roundButton: true,
        customClass: "confirmForm",
      }).then(async () => {
        const loading = this.$loading({
          lock: true,
          text: "Processing",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
        });
        if (this.squadData.length > 0) {
          await SquadService.importSquads(this.squadData);
        }
        loading.close();
        this.confirmImportDepartment();
      });
    },

    confirmImportDepartment() {
      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm Add Department",
        message: h(
          "ConfirmAddNewDepartment",
          {
            props: {
              newUsers: [...this.selectedUsers],
              newTeams: [...this.teamData],
              contactCols: this.contactCols,
            },
            on: {
              input: (value) => {
                this.departmentData = [...value];
              },
            },
          },
          []
        ),
        roundButton: true,
        customClass: "confirmForm",
      }).then(async () => {
        const loading = this.$loading({
          lock: true,
          text: "Processing",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
        });
        if (this.departmentData.length > 0) {
          await DepartmentService.importDepartments(this.departmentData);
        }
        loading.close();
        await this.$alert("Import Successfully", "Notification", {
          confirmButtonText: "OK",
          callback: (action) => {
            this.$message({
              type: "info",
              message: `action: ${action}`,
            });
          },
        });
      });
      this.$router.push("/teams");
    },

    async importUsers(selectedUsers) {
      const allUsers = selectedUsers.map(({ _index, values }) => {
        return {
          email: values[this.contactCols.email],
          name: values[this.contactCols.name],
          title: values[this.contactCols.role],
          phone: values[this.contactCols.phone],
          join_date: values[this.contactCols.onBoarding],
        };
      });
      return UserService.importUsers(allUsers);
    },

    handleImportExcel(file) {
      const loading = this.$loading({
        lock: true,
        text: "Processing",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });

      if (
        file.raw.type !==
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      ) {
        this.handleError("Please, select sheet file!");
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const data = e.target.result;

        const workBook = XLSX.read(data, { type: "binary" });
        const workBookIncludeColor = XLSX.read(data, {
          type: "binary",
          cellStyles: true,
        });

        const workSheetName = workBook.SheetNames[0];

        const workSheet = workBook.Sheets[workSheetName];
        const workSheetIncludeColor =
          workBookIncludeColor.Sheets[workSheetName];

        this.colors = [];
        this.colors = Object.entries(workSheetIncludeColor)
          .map(([key, value]) => {
            if (value.s && value.s.bgColor && key.includes("E")) {
              return { key: key, color: value.s.bgColor.rgb };
            }
          })
          .filter((item) => item !== undefined);

        const excelData = XLSX.utils.sheet_to_json(workSheet, {
          raw: false,
          header: 1,
          blankrows: false,
        });

        if (excelData.length === 0) {
          this.$message.error("Oops, file invalid.");
          return;
        }
        loading.close();
        this.confirmHeader(excelData);
      };

      reader.readAsBinaryString(file.raw);
    },

    confirmHeader(excelData) {
      const headerTemp = excelData.findIndex((item) => item.length > 2);
      if (headerTemp >= 0) {
        this.header_index = headerTemp;
      }

      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm Header",
        message: h(
          "ConfirmHeaderBox",
          {
            props: {
              headers: excelData,
            },
            on: {
              input: (value) => {
                this.header_index = value;
              },
            },
          },
          []
        ),
        roundButton: true,
        customClass: "confirmForm",
      }).then(() => {
        this.sending_columns = Array.from(
          { length: excelData[this.header_index].length },
          () => true
        );
        this.colors.splice(0, this.header_index + 1);
        this.confirmContact(excelData);
      });
    },

    confirmContact(excelData) {
      const header = excelData[this.header_index];

      let contactCols = {
        team: header.findIndex((item) => item === "Team"),
        name: header.findIndex((item) => item === "Name / Team"),
        role: header.findIndex((item) => item === "Role"),
        email: header.findIndex((item) => item === "Email"),
        phone: header.findIndex((item) => item === "Phone"),
        onBoarding: header.findIndex(
          (item) => item === "On board at Paradox/Olivia"
        ),
      };

      this.contactCols = {};
      this.contactCols = { ...contactCols };

      const h = this.$createElement;
      this.$msgbox({
        title: "Confirm Contact Data",
        message: h(
          "ConfirmContactBox",
          {
            props: {
              cols: excelData[this.header_index].map(
                (col, index) => `${XLSX.utils.encode_col(index)} - ${col}`
              ),
              defaultValue: this.contactCols,
            },
            on: {
              input: (value) => {
                this.contactCols = value;
              },
            },
          },
          []
        ),
        customClass: "confirmForm",
        roundButton: true,
        beforeClose: (action, instance, done) => {
          if (action === "confirm") {
            instance.$children[2].$refs["refContactForm"].validate((valid) => {
              valid && done();
            });
          } else {
            done();
          }
        },
      }).then(() => {
        this.excelData = [];
        this.excelData = excelData;
      });
    },

    tableRowClassName({ row, _rowIndex }) {
      if (row.values[this.contactCols.status] === "Active") {
        return "active-row";
      } else if (row.values[this.contactCols.status] === "Deactivate") {
        return "warning-row";
      }
    },

    back() {
      this.$router.push("/teams");
    },
  },
};
</script>

<style lang="scss">
.el-table .warning-row {
  background: #ff9ba6 !important;
}

.el-table .active-row {
  background: #82e8af !important;
}

.upload-form-item {
  .el-form-item__content {
    .el-form-item__error {
      left: 50%;
      transform: translateX(-50%);
    }
  }
}

.confirmForm {
  width: auto !important;
  overflow: auto !important;
  max-height: 90vh;
  min-width: 500px;
  &::-webkit-scrollbar {
    height: 10px;
    width: 10px;
  }

  /* Track */
  &::-webkit-scrollbar-track {
    background: white;
    border-radius: 50rem;
    outline: 1px solid #cbcddc;
  }

  /* Handle */
  &::-webkit-scrollbar-thumb {
    border: 2px solid white;
    background: #cbcddc;
    border-radius: 50rem;
  }
}
</style>
