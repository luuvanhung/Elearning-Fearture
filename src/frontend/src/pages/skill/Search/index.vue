<template>
  <div class="row mt-3 p-sm-3">
    <div class="col-xl-3 col-12 p-xl-0 search-form" v-if="skillDefinitions">
      <div class="header-form">Search Options</div>
      <div class="p-2">
        <span class="label-field">Employee name:</span>
        <br />
        <el-input
          v-model="currentData.nameUser"
          placeholder="Please fill input"
        ></el-input>
      </div>
      <div class="p-2">
        <div>
          <span class="label-field">Skills</span>
          <br />
        </div>
        <div v-for="skill in skillDefinitions" :key="skill.id" class="mt-2">
          <div>
            <label class="d-flex align-items-center label-text mb-1">
              <input
                class="mr-2"
                type="checkbox"
                @change="changeShowingState(skill)"
              />
              {{ skill.name }}
            </label>
            <select
              :ref="`skill-definition-${skill.id}`"
              class="select"
              v-show="skill.isShowing"
            >
              <option value="-1">All</option>
              <option
                v-for="level in skill.level"
                :key="level.id"
                :value="level.definition"
              >
                {{ level.name }}
              </option>
            </select>
          </div>
        </div>

        <br />
        <div>
          <span class="label-field">Options</span>
          <label
            class="d-flex align-items-center label-text mt-2"
            style="font-style: italic"
          >
            <input
              class="mr-2 mycb"
              type="checkbox"
              v-model="currentData.checkAllSkill"
            />
            User must have all selected skills
          </label>
        </div>
      </div>
      <div
        class="d-flex justify-content-center align-items-center btnSearch"
        @click="searchData(currentData)"
      >
        Search
      </div>
    </div>
    <div class="col-xl-9 col-12">
      <el-table
        stripe
        :header-row-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        header-cell-class-name="bg-header-table"
        :data="skillSearch"
        style="width: 100%"
      >
        <el-table-column prop="name" label="Name" width="120">
        </el-table-column>
        <el-table-column prop="title" label="Skills">
          <template slot-scope="scope">
            <div
              v-for="item in skillSearch[scope.$index].data"
              :key="item.id"
              class="d-flex justify-content-center align-items-center"
            >
              <div class="col-md-3 text-left mb-1">
                <span>{{ item.skill_definition.skill.name }}</span>
              </div>
              <div class="col-md-3 text-left">
                <span>{{ item.skill_definition.level.name }}</span>
              </div>
              <div class="col-md-3" v-if="skillDefinitions">
                <el-rate
                  disabled
                  :max="maxStar(item.skill_definition.skill.id)"
                  :value="
                    countStar(
                      item.skill_definition.skill.id,
                      item.skill_definition.level.id
                    )
                  "
                  class="text-left"
                >
                </el-rate>
              </div>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <div class="d-flex justify-content-center mt-2">
        <el-pagination
          background
          layout="prev, pager, next"
          :page-size="page_size"
          :total="totalRecords"
          @current-change="setPage"
        >
        </el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import skillDefinition from "@/services/skill/definition";
import skillSearch from "@/services/skill/search";

export default {
  name: "SearchSkill",
  data() {
    return {
      skillDefinitions: [],
      skillSearch: [],
      currentData: {
        nameUser: "",
        checkAllSkill: false,
      },
      page_size: 12,
      totalRecords: 0,
      lastQueryData: Object,
    };
  },
  async created() {
    await this.getSkillDefinitions();
    await this.getData(this.page, this.page_size);
  },
  methods: {
    setPage(page) {
      this.getData(page, this.page_size, this.lastQueryData);
    },
    changeShowingState(skill) {
      this.$set(skill, "isShowing", !skill.isShowing);
      skill.isChecked = !skill.isChecked;
    },
    async getSkillDefinitions() {
      try {
        const res = await skillDefinition.get();
        let uniqueSkill = _.uniqBy(res.data, "skill.id").map((e) => e.skill);
        uniqueSkill.map((skillArray) => {
          let newArray = [];
          res.data.forEach((item) => {
            if (skillArray.id === item.skill.id) {
              newArray.push(Object.assign(item.level, { definition: item.id }));
              newArray = _.orderBy(newArray, ["weight"], ["asc"]);
            }
          });
          skillArray.level = newArray;
        });
        this.skillDefinitions = uniqueSkill;
        this.skillDefinitions.forEach((skill) => {
          skill.isChecked = false;
          skill.checkedDefinitionId = "";
        });
      } catch (err) {
        console.log(err);
      }
    },
    async getData(page, page_size, lastQueryData) {
      try {
        const res = await skillSearch.getAll(page, page_size, lastQueryData);
        this.skillSearch = this.handleDataSearchAPI(res.data.data);
        this.totalRecords = res.data.total_records;
      } catch (err) {
        console.log(err);
      }
    },
    handleDataSearchAPI(dataAPI) {
      const uniqueUser = _.uniqBy(dataAPI, "voted_user.id");
      return uniqueUser.map((userArray) => {
        const newData = {
          id: userArray.voted_user.id,
          name: userArray.voted_user.name,
          data: [],
        };
        dataAPI.forEach((item) => {
          if (item.voted_user.id === userArray.voted_user.id) {
            newData.data.push(item);
          }
        });
        return newData;
      });
    },
    maxStar(skillId) {
      const check = this.skillDefinitions.find((e) => e.id === skillId);
      return check.level.length;
    },
    countStar(skillId, levelId) {
      const check = this.skillDefinitions.find((e) => e.id === skillId);
      const star = check.level.findIndex((e) => e.id === levelId) + 1;
      return star;
    },
    async searchData() {
      let queryData = "";
      if (this.currentData.nameUser !== "") {
        queryData += `&q=${this.currentData.nameUser}`;
      }
      this.skillDefinitions.forEach((skill) => {
        if (skill.isChecked) {
          const definitionId =
            this.$refs[`skill-definition-${skill.id}`][0].value;
          if (definitionId === "-1") {
            skill.level.forEach((e) => {
              queryData += `&skill-definitions=${e.definition}`;
            });
          } else queryData += `&skill-definitions=${definitionId}`;
        }
      });
      queryData += `&i=${this.currentData.checkAllSkill ? "1" : "0"}`;

      const res = await skillSearch.getAll(
        this.page,
        this.page_size,
        queryData
      );
      this.lastQueryData = queryData;
      this.totalRecords = res.data.total_records;
      this.skillSearch = this.handleDataSearchAPI(res.data.data);
    },
  },
};
</script>

<style scoped>
.header-form {
  font-family: "Open Sans", sans-serif;
  font-size: 14px;
  font-weight: bold;
  height: 48px;
  line-height: 48px;
  text-align: center;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  padding-left: 0;
  color: #fff;
  background: #25c9d0;
}

.label-field {
  font-weight: bold;
  font-size: 14px;
  color: #707070;
}

.search-form {
  background: #fff;
}

.btnSearch {
  font-family: "Times New Roman", Times, serif;
  font-weight: bold;
  font-size: 16px;
  width: 25%;
  height: 40px;
  color: #ffffff;
  background: #25c9d0;
  border: 1px solid #c6c6c6;
  margin: 2% auto;
  border-radius: 5px;
  cursor: pointer;
}

.label-text {
  font-family: "Open Sans", sans-serif;
  font-size: 14px;
  cursor: pointer;
  color: #707070;
}

.select {
  width: 100%;
  border-radius: 5px;
  height: 40px;
  background: #ffffff;
  border: 1px solid #dcdfe6;
  padding-left: 10px;
  color: #707070;
}
</style>
