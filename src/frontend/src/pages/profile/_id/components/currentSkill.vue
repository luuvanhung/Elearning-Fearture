<template>
  <div class="container-fluid">
    <div class="general-infor">
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">Current Skill Information</span>
          <el-button
            class="edit-button mb-3"
            type="text"
            v-if="!isEditing"
            @click="isEditing = true"
          >
            <restricted-view :scopes="['personal_skill:edit']">
              <template v-slot:default>
                <img
                  :src="require('@/static/images/IconCardEdit.svg')"
                  class="edit-icon"
                />
              </template>
            </restricted-view>
          </el-button>
          <el-button
            class="edit-button"
            type="text"
            v-if="isEditing"
            @click="isConfirming = true"
          >
            <img
              :src="require('@/static/images/IconCardSave.svg')"
              class="edit-icon"
            />
          </el-button>
        </div>
        <el-form class="d-flex justify-content-center" v-if="isEditing">
          <el-form-item class="mr-2 ml-2">
            <el-select
              style="width: 100%"
              placeholder="Skill"
              @change="onChangeSkill($event)"
              v-model="currentInput.skill_id"
            >
              <el-option
                v-for="skill in skillDefinitions"
                :key="skill.id"
                :value="skill.id"
                :label="skill.name"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="mr-2 ml-2">
            <el-select
              style="width: 100%"
              :disabled="!currentInput.skill_id"
              placeholder="Level"
              v-model="currentInput.level_id"
              @change="onChangeLevel($event)"
            >
              <el-option
                v-for="level in levels"
                :key="level.id"
                :value="level.id"
                :label="level.name"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="mr-2 ml-2 d-flex align-items-center">
            <el-rate
              @change="onChangeStar($event)"
              :max="currentInput.maxStar"
              v-model="currentInput.star"
              :disabled="!currentInput.skill_id"
            >
            </el-rate>
          </el-form-item>
          <div
            class="d-flex justify-content-center align-items-center btnAddSkill"
            @click="AddCurrentSkill(currentInput)"
          >
            <span class="ml-1">Add Skill</span>
          </div>
        </el-form>
        <el-table
          :data="currentSkill"
          :cell-style="{ textAlign: 'center' }"
          stripe
          header-cell-class-name="bg-header-table"
          border
          style="width: 100%"
          :class="{ hiddenTable: isHiddenTable }"
        >
          <el-table-column prop="skill_name" width="120" label="Skill">
          </el-table-column>
          <el-table-column label="Level">
            <template slot-scope="scope">
              <div
                class="mobile-screen d-flex align-items-center mb-2 mt-2 justify-content-center"
                v-for="item in currentSkill[scope.$index].data"
                :key="item.id"
              >
                <span>{{ item.level_name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Rate">
            <template slot-scope="scope">
              <div
                class="mobile-screen d-flex align-items-center justify-content-center mb-2 mt-2"
                v-for="item in currentSkill[scope.$index].data"
                :key="item.id"
              >
                <el-rate
                  :disabled="!isEditing"
                  :max="maxStar(item.skill_id)"
                  :value="countStar(item.skill_id, item.level_id)"
                  @change="voteSkill(item, item.level_id, $event)"
                >
                </el-rate>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Endorsed by">
            <template slot-scope="scope">
              <div
                class="mobile-screen d-flex align-items-center justify-content-center mb-2 mt-2"
                v-for="item in currentSkill[scope.$index].data"
                :key="item.id"
              >
                <span>{{ item.voters.map((el) => el.name).join(", ") }} </span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Action" v-if="isEditing">
            <template slot-scope="scope">
              <div
                class="mobile-screen d-flex align-items-center justify-content-center mb-2 mt-2"
                v-for="(item, index) in currentSkill[scope.$index].data"
                :key="item.id"
              >
                <restricted-view :scopes="['personal_skill:edit']">
                  <template v-slot:default>
                    <div
                      :class="[{ active: !item.isMineVote }, 'btnUnvote']"
                      @click="showDialogDelete(scope.$index, index)"
                    >
                      <span>Unvote</span>
                    </div>
                  </template>
                </restricted-view>
              </div>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog :visible.sync="dialogDelete" title="Confirm Delete">
          <slot>
            <h3 class="text-center">Do you want to remove?</h3>
            <div class="text-center">
              <el-button type="danger" class="mt-3" @click="removeMyVote()">
                Delete
              </el-button>
            </div>
          </slot>
        </el-dialog>
      </el-card>
      <el-dialog title="Confirm" :visible.sync="isConfirming" width="30%">
        <span>Do you want to save this change?</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="isConfirming = false">Cancel</el-button>
          <el-button type="primary" @click="saveConfirm">Save</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import SkillDefinition from "@/services/skill/definition";
import CurrentSkill from "@/services/profile/currentSkill";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "currentSkill",
  components: { RestrictedView },
  data() {
    return {
      skillDefinitions: [],
      currentSkill: [],
      levels: [],
      currentInput: {
        skill_id: "",
        level_id: "",
        maxStar: 0,
        star: 0,
      },
      currentSkillToDelete: {
        skillIndex: null,
        levelIndex: null,
      },
      voter_user: "",
      isEditing: false,
      isConfirming: false,
      dialogDelete: false,
      isHiddenTable: false,
    };
  },
  methods: {
    showDialogDelete(skillIndex, levelIndex) {
      this.dialogDelete = true;
      this.currentSkillToDelete.skillIndex = skillIndex;
      this.currentSkillToDelete.levelIndex = levelIndex;
    },
    saveConfirm() {
      this.isEditing = false;
      this.isConfirming = false;
    },
    async voteSkill(currentSkill, levelId, star) {
      const skill = this.skillDefinitions.find(
        (e) => e.id == currentSkill.skill_id
      );
      const skillDefId = skill.level[star - 1].definition;
      const data = {
        voted_user: this.$route.params.id,
        skill_definition: skillDefId,
      };
      const myVote = this.getMyVote(currentSkill.skill_id);
      if (myVote !== undefined) {
        try {
          const res = await CurrentSkill.update(myVote.skill_vote, data);
          if (res.status === 200) {
            this.$toast.success("Updated Successfully");
          }
        } catch (err) {
          this.$toast.error("Update Failed");
        }
      } else {
        const res = await CurrentSkill.create(data);
        if (res.status === 201) {
          this.$toast.success("Voted Successfully");
        } else {
          this.$toast.error("Vote Failed");
        }
      }
      await this.getCurrentSkill();
      this.syncVotedField();
    },
    async AddCurrentSkill(currentInput) {
      try {
        const skill = this.skillDefinitions.find(
          (e) => e.id == currentInput.skill_id
        );
        const level = skill.level.find((e) => e.id == currentInput.level_id);
        const data = {
          voted_user: this.$route.params.id,
          skill_definition: level.definition,
        };
        const res = await CurrentSkill.create(data);
        if (res.status === 200 || res.status === 201) {
          this.$toast.success("Added Successfully");
          await this.getCurrentSkill();
          this.syncVotedField();
        }
      } catch (err) {
        this.$toast.error("Add Failed");
      }
    },
    onChangeSkill(skillId) {
      const skill = this.skillDefinitions.find((e) => e.id == skillId);
      this.levels = skill.level;
      this.currentInput.maxStar = this.levels.length;
      this.currentInput.level_id = "";
      this.currentInput.star = 0;
    },
    onChangeLevel(levelId) {
      const index = this.levels.findIndex((e) => e.id == levelId);
      this.currentInput.star = index + 1;
    },
    onChangeStar(star) {
      this.currentInput.level_id = this.levels[star - 1].id;
    },
    async getSkillDefinitions() {
      try {
        const res = await SkillDefinition.get();
        let uniqueSkill = _.uniqBy(res.data, "skill.id").map((e) => e.skill);
        uniqueSkill.map((skillArray) => {
          let newArray = [];
          res.data.forEach((item) => {
            if (skillArray.id == item.skill.id) {
              newArray.push(Object.assign(item.level, { definition: item.id }));
              newArray = _.orderBy(newArray, ["weight"], ["asc"]);
            }
          });
          skillArray.level = newArray;
        });
        this.skillDefinitions = uniqueSkill;
      } catch (err) {
        console.log(err);
      }
    },
    async getCurrentSkill() {
      try {
        const user_voted_id = this.$route.params.id;
        const res = await CurrentSkill.get(user_voted_id);
        if (res.status === 200 || res.status === 201) {
          if (res.data.length !== 0) {
            this.isHiddenTable = false;
            this.currentSkill = _.chain(res.data)
              .groupBy("skill_id")
              .map((value, keySkill) => {
                let groupByLevel = _.chain(value)
                  .groupBy("level_id")
                  .map((val, key) => ({
                    id: val[0].id,
                    level_id: key,
                    skill_id: keySkill,
                    level_name: val[0].level_name,
                    definition_id: val[0].skill_definition,
                    isMineVote:
                      val.find((el) => el.id == this.voter_user) !== undefined,
                    max_title_weight: Math.max(
                      ...val.map((el) => el.voter_title_weight)
                    ),
                    voters: _.orderBy(
                      val.map((el) => ({
                        id: el.voter,
                        name: el.voter_name,
                        skill_vote: el.id,
                      })),
                      "voter_title_weight",
                      "desc"
                    ),
                  }))
                  .value();

                const data = {
                  skill_id: keySkill,
                  skill_name: value[0].skill_name,
                  data: groupByLevel,
                };
                return data;
              })
              .value();
          } else this.isHiddenTable = true;
        }
      } catch (e) {
        console.log(e);
      }
    },
    countStar(skillId, levelId) {
      const check = this.skillDefinitions.find((e) => e.id == skillId);
      const star = check.level.findIndex((e) => e.id == levelId) + 1;
      return star;
    },
    maxStar(skillId) {
      const check = this.skillDefinitions.find((e) => e.id == skillId);
      return check.level.length;
    },

    getMyVote(skillId) {
      const skill = this.currentSkill.find((el) => el.skill_id == skillId);
      const level = skill.data.find(
        (level) =>
          level.voters.find((el) => el.id === this.voter_user) !== undefined
      );
      return level == undefined
        ? undefined
        : level.voters.find((el) => el.id == this.voter_user);
    },

    syncVotedField() {
      this.currentSkill.forEach((skill) => {
        skill.data.forEach((level) => {
          level.isMineVote =
            level.voters.find((el) => el.id == this.voter_user) !== undefined;
        });
      });
    },
    async removeMyVote() {
      const skillIndex = this.currentSkillToDelete.skillIndex;
      const levelIndex = this.currentSkillToDelete.levelIndex;
      const level = this.currentSkill[skillIndex].data[levelIndex];
      const myVote = level.voters.find((el) => el.id == this.voter_user);
      const res = await CurrentSkill.delete(myVote.skill_vote);
      if (res.status === 204) {
        level.voters.splice(level.voters.indexOf(myVote), 1);
        level.isMineVote = false;
        this.dialogDelete = false;
        this.currentSkillToDelete.skillIndex =
          this.currentSkillToDelete.levelIndex = null;
        this.$toast.success("Deleted Successfully");
        if (this.isEmptySkill(skillIndex)) {
          this.currentSkill.splice(skillIndex, 1);
        }
        if (this.isEmptyLevel(skillIndex, levelIndex)) {
          this.currentSkill[skillIndex].data.splice(levelIndex, 1);
        }
      }
    },
    isEmptySkill(skillIndex) {
      return (
        this.currentSkill[skillIndex].data.find(
          (level) => level.voters.length !== 0
        ) === undefined
      );
    },
    isEmptyLevel(skillIndex, levelIndex) {
      return this.currentSkill[skillIndex].data[levelIndex].voters.length == 0;
    },
  },

  async created() {
    await this.getSkillDefinitions();
    await this.getCurrentSkill();
    this.voter_user = localStorage.getItem("user_id");
    this.syncVotedField();
  },
};
</script>

<style scoped>
.active {
  visibility: hidden;
}

.hiddenTable {
  display: none;
}

.btnAddSkill {
  font-family: "Times New Roman", Times, serif;
  font-weight: bold;
  font-size: 16px;
  width: 10%;
  height: 40px;
  color: #ffffff;
  background: #25c9d0;
  border: 1px solid #c6c6c6;
  border-radius: 5px;
  cursor: pointer;
}

.btnUnvote {
  font-family: "Times New Roman", Times, serif;
  font-weight: bold;
  font-size: 14px;
  width: 120%;
  height: 5%;
  color: #ffffff;
  background: #f56c6c;
  border-radius: 5px;
  cursor: pointer;
}

@media screen and (max-width: 1024px) {
  .btnUnvote {
    width: 100%;
  }

  .mobile-screen {
    margin-bottom: 65% !important;
    margin-top: 65% !important;
  }
}
</style>
