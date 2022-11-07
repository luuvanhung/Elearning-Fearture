<template>
  <div>
    <div class="mt-3">
      <el-table
        :data="positionData.rows"
        :header-row-style="{ textAlign: 'center' }"
        :cell-style="{ textAlign: 'center' }"
        stripe
        header-cell-class-name="bg-header-table"
        style="width: 100%"
      >
        <el-table-column prop="title" label="Position" width="300">
        </el-table-column>
        <el-table-column prop="title_skills" label="Skills">
          <template slot-scope="scope">
            <div class="d-flex justify-content-center align-items-center">
              <div class="skill-content">
                <div
                  class="item row mb-2"
                  v-for="(item, index) in positionData.rows[scope.$index]
                    .title_skills"
                  :key="item.id"
                >
                  <div class="skill-name col-md-3">
                    <span v-if="item.editMode">
                      <el-select
                        @change="onChangeSkill($event, scope.$index)"
                        v-model="skillForm.skillName[scope.$index]"
                        placeholder="Skill"
                        size="mini"
                      >
                        <el-option
                          v-for="item in skillData"
                          :key="item.id"
                          :label="item.name"
                          :value="item.id"
                        >
                        </el-option>
                      </el-select>
                    </span>
                    <span v-else>{{ item.skill_name }}</span>
                  </div>
                  <div class="skill-name col-md-3 text-secondary">
                    <span v-if="item.editMode">
                      <el-select
                        @change="onChangeLevel($event, scope.$index)"
                        v-model="skillForm.skillLevel[scope.$index]"
                        placeholder="Level"
                        size="mini"
                        :disabled="!skillForm.skillName[scope.$index]"
                      >
                        <el-option
                          v-for="item in levelData[scope.$index]"
                          :key="item.id"
                          :label="item.name"
                          :value="item.id"
                        >
                        </el-option>
                      </el-select>
                    </span>
                    <span v-else>{{ item.level_name }}</span>
                  </div>
                  <div class="skill-rate col-md-6 pl-3 d-flex">
                    <div class="d-flex justify-content-between rate-start">
                      <div class="d-flex align-items-center">
                        <el-rate
                          @change="onChangeStar($event, scope.$index)"
                          v-model="skillForm.skillStar[scope.$index]"
                          :max="skillForm.maxStar[scope.$index]"
                          :disabled="!skillForm.skillName[scope.$index]"
                          v-if="item.editMode"
                        >
                        </el-rate>
                        <el-rate
                          :value="definitionStar(item.skill_id, item.level_id)"
                          disabled
                          :max="maxStar(item.skill_id)"
                          v-else
                        >
                        </el-rate>
                        <div v-if="!item.editMode">
                          <cite class="author"
                            >(Set by {{ item.set_by_user_name }})</cite
                          >
                        </div>
                      </div>
                      <restricted-view :scopes="['title_skill:edit']">
                        <template v-slot:default>
                          <div v-if="!item.editMode">
                            <img
                              :src="require('@/static/images/IconEdit.svg')"
                              @click="editDataTable(item, scope.$index)"
                            />
                            <img
                              :src="require('@/static/images/IconDelete.svg')"
                              @click="removeSkill(scope.$index, index, item.id)"
                            />
                          </div>
                          <div v-else>
                            <img
                              :src="require('@/static/images/IconCheck.svg')"
                              class="mr-3"
                              @click="
                                saveDataTable(
                                  item,
                                  scope.$index,
                                  positionData.rows[scope.$index]
                                )
                              "
                            />
                            <img
                              :src="require('@/static/images/IconCancel.svg')"
                              class="ml-3"
                              @click="cancelEditDataTable(item, scope.$index)"
                            />
                          </div>
                        </template>
                      </restricted-view>
                    </div>
                  </div>
                </div>
                <el-form
                  ref="skillForm"
                  label-width="120px"
                  :class="formIsHidden[scope.$index] ? 'activeHidden' : ''"
                  class="item row demo-skillForm d-flex justify-content-center align-items-center"
                >
                  <div class="col-md-3">
                    <el-form-item label-width="0px">
                      <el-select
                        @change="onChangeSkill($event, scope.$index)"
                        v-model="skillForm.skillName[scope.$index]"
                        placeholder="Skill"
                        size="mini"
                      >
                        <el-option
                          v-for="item in skillData"
                          :key="item.id"
                          :label="item.name"
                          :value="item.id"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div class="col-md-3">
                    <el-form-item label-width="0px">
                      <el-select
                        @change="onChangeLevel($event, scope.$index)"
                        v-model="skillForm.skillLevel[scope.$index]"
                        placeholder="Level"
                        size="mini"
                        :disabled="!skillForm.skillName[scope.$index]"
                      >
                        <el-option
                          v-for="item in levelData[scope.$index]"
                          :key="item.id"
                          :label="item.name"
                          :value="item.id"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div class="col-md-6 d-flex pl-3">
                    <div
                      class="d-flex align-items-center justify-content-between rate-start"
                    >
                      <el-rate
                        @change="onChangeStar($event, scope.$index)"
                        v-model="skillForm.skillStar[scope.$index]"
                        :max="skillForm.maxStar[scope.$index]"
                        :disabled="!skillForm.skillName[scope.$index]"
                      >
                      </el-rate>
                      <restricted-view :scopes="['title_skill:edit']">
                        <template v-slot:default>
                          <el-button
                            type="primary"
                            @click="
                              addSkill(
                                scope.$index,
                                positionData.rows[scope.$index]
                              )
                            "
                          >
                            <font-awesome-icon :icon="['fas', 'plus']" />
                          </el-button>
                        </template>
                      </restricted-view>
                    </div>
                  </div>
                </el-form>
              </div>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import positionSkillService from "@/services/skill/positionSkill.services";
import responeMessage from "@/services/skill/responseMessage.js";
import definitionService from "@/services/skill/definition";
import _ from "lodash";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "position_skill",
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  data() {
    return {
      positionData: {
        searching: false,
        rows: [],
        currentPage: 0,
        totalPage: 1,
      },
      skillForm: {
        skillName: [],
        skillLevel: [],
        skillStar: [],
        maxStar: [],
      },
      formIsHidden: [],
      skillData: [],
      levelData: [],
      page: 1,
      page_size: 12,
    };
  },
  methods: {
    editDataTable(positionRow, row) {
      this.$set(positionRow, "editMode", true);
      this.formIsHidden = [];
      this.formIsHidden[row] = true;
      positionRow.oldSkill = positionRow.skill_name;
      positionRow.oldLevel = positionRow.level_name;
    },
    async saveDataTable(currentData, row, position) {
      if (
        !this.skillForm.skillName[row] ||
        !this.skillForm.skillLevel[row] ||
        !this.skillForm.skillStar[row]
      ) {
        return this.$toast.error("Error: Form is empty");
      }
      currentData.skill_id = this.skillForm.skillName[row];
      currentData.level_id = this.skillForm.skillLevel[row];
      const skillData = this.skillData.find(
        (e) => e.id === currentData.skill_id
      );
      const levelData = skillData.level.find(
        (e) => e.id === currentData.level_id
      );
      const data = {
        title: position.id,
        skill_definition: levelData.definition,
      };
      try {
        const res = await positionSkillService.updatePositionSkill(
          currentData.id,
          data
        );
        if (res.status === 200) {
          this.formIsHidden = [];
          this.formIsHidden[row] = false;
          currentData.skill_name = skillData.name;
          currentData.level_name = levelData.name;
          currentData.set_by_user_name = localStorage.getItem("name");
          this.skillForm.skillName[row] = "";
          this.skillForm.skillLevel[row] = "";
          this.skillForm.skillStar[row] = 0;
          this.$set(currentData, "editMode", false);
          this.$toast.success("Update success");
        }
      } catch (err) {
        this.$toast.error("Edit Failed");
      }
    },
    cancelEditDataTable(positionRow, row) {
      this.$set(positionRow, "editMode", false);
      this.formIsHidden[row] = false;
      this.skillForm.skillName[row] = "";
      this.skillForm.skillLevel[row] = "";
      this.skillForm.skillStar[row] = 0;
      positionRow.skill_name = positionRow.oldSkill;
      positionRow.level_name = positionRow.oldLevel;
    },
    async removeSkill(row, index, positionSkillId) {
      try {
        await positionSkillService.deletePositionSkill(positionSkillId);
        this.positionData.rows[row].title_skills.splice(index, 1);
        this.$toast.success("Deleted Successfully");
      } catch (error) {
        return this.$toast.error("Delete Failed ");
      }
    },
    async addSkill(row, position) {
      if (
        !this.skillForm.skillName[row] ||
        !this.skillForm.skillLevel[row] ||
        !this.skillForm.skillStar[row]
      ) {
        return this.$toast.error("Error: Form is empty");
      }
      const newSkillId = this.skillForm.skillName[row];
      const newLevelId = this.skillForm.skillLevel[row];
      const checkData = position.title_skills.find(
        (element) => element.skill_id == newSkillId
      );

      if (checkData) {
        return this.$toast.error(responeMessage.VALIDATION.POSITION_SKILL);
      }

      const skillData = this.skillData.find(
        (element) => element.id == newSkillId
      );
      const levelData = skillData.level.find(
        (element) => element.id == newLevelId
      );

      const data = new FormData();
      data.append("title", position.id);
      data.append("skill_definition", levelData.definition);
      try {
        let responseData = await positionSkillService.createPositionSkill(data);
        if (responseData && responseData.status == 201) {
          this.positionData.rows[row].title_skills.push({
            id: responseData.data.id,
            skill_definition: data.skill_definition,
            skill_name: skillData.name,
            level_name: levelData.name,
            level_id: this.skillForm.skillLevel[row],
            skill_id: this.skillForm.skillName[row],
            set_by_user_name: localStorage.getItem("name"),
            start: this.skillForm.skillStar[row],
          });

          this.skillForm.skillName[row] = "";
          this.skillForm.skillLevel[row] = "";
          this.skillForm.skillStar[row] = 0;
          return this.$toast.success("Created Successfully");
        } else {
          return this.$toast.error("Create Failed");
        }
      } catch (error) {
        return this.$toast.error("Create Failed");
      }
    },
    async getData() {
      let skillDefinitionsData = await definitionService.get();
      skillDefinitionsData = skillDefinitionsData.data;

      let ArrayUnique = _.uniqBy(skillDefinitionsData, "skill.name").map(
        (element) => element.skill
      );
      ArrayUnique.map((skillItem) => {
        let newArray = [];
        skillDefinitionsData.forEach((item) => {
          if (skillItem.id == item.skill.id) {
            newArray.push(Object.assign(item.level, { definition: item.id }));
            newArray = _.orderBy(newArray, ["weight"], ["asc"]);
          }
        });
        skillItem.level = newArray;
      });
      this.skillData = ArrayUnique;

      let responseData = await positionSkillService.getPositionSkill();
      this.positionData.rows = responseData.data;
    },
    maxStar(skillId) {
      const found = this.skillData.find((element) => element.id == skillId);
      return found.level.length;
    },
    definitionStar(skillId, levelId) {
      const found = this.skillData.find((element) => element.id == skillId);
      const star =
        found.level.findIndex((element) => element.id == levelId) + 1;
      return star;
    },
    onChangeSkill(event, index) {
      this.skillForm.skillName[index] = event;
      this.skillForm.skillLevel[index] = "";
      this.skillForm.skillStar[index] = 0;
      const found = this.skillData.find((element) => element.id == event);
      this.levelData[index] = found.level;
      this.skillForm.maxStar[index] = found.level.length;
    },
    onChangeLevel(event, index) {
      const found = this.skillData.find(
        (element) => element.id == this.skillForm.skillName[index]
      );
      this.skillForm.skillStar[index] =
        found.level.findIndex((element) => element.id == event) + 1;
    },
    onChangeStar(event, index) {
      const found = this.skillData.find(
        (element) => element.id == this.skillForm.skillName[index]
      );
      this.skillForm.skillLevel[index] = found.level[event - 1].id;
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
