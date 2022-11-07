<template>
  <div class="container-fluid">
    <div class="general-infor">
      <el-card class="box-card mb-4 card-detail">
        <div slot="header" class="clearfix">
          <span class="card-title">Target Skill Information</span>

          <el-button
            class="edit-button"
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
            @click="AddTargetSkill(currentInput)"
          >
            <span class="ml-1">Add Skill</span>
          </div>
        </el-form>
        <el-table
          :data="targetSkill"
          :cell-style="{ textAlign: 'center' }"
          stripe
          header-cell-class-name="bg-header-table"
          border
          style="width: 100%"
          :class="{ hiddenTable: isHiddenTable }"
        >
          <el-table-column prop="skill_name" label="Skill"> </el-table-column>
          <el-table-column prop="level_name" label="Level"> </el-table-column>
          <el-table-column label="Rate">
            <template slot-scope="scope">
              <div
                class="mobile-screen d-flex align-items-center justify-content-center"
              >
                <el-rate
                  :disabled="!isEditing"
                  :max="maxStar(scope.row)"
                  :value="countStar(scope.row)"
                  @change="updateTargetSkill(scope.row, $event)"
                >
                </el-rate>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="set_by_user.name" label="Set by">
          </el-table-column>
          <el-table-column label="Action" v-if="isEditing">
            <template slot-scope="scope">
              <div
                :class="[{ active: scope.row.set_by_user.id !== voter_user }]"
                @click="showDialogDelete(scope.row)"
              >
                <img :src="require('@/static/images/IconDelete.svg')" />
              </div>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog :visible.sync="dialogDelete" title="Confirm Delete">
          <slot>
            <h3 class="text-center">Do you want to remove?</h3>
            <div class="text-center">
              <el-button
                type="danger"
                class="mt-3"
                @click="deleteTargetSkill()"
              >
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
import TargetSkill from "@/services/profile/targetSkill";
import SkillDefinition from "@/services/skill/definition";
import RestrictedView from "@/components/RestrictedView";

export default {
  name: "targetSkill",
  components: { RestrictedView },
  data() {
    return {
      isEditing: false,
      isConfirming: false,
      dialogDelete: false,
      isHiddenTable: false,
      targetSkill: [],
      skillDefinitions: [],
      levels: [],
      currentInput: {
        skill_id: "",
        level_id: "",
        maxStar: 0,
        star: 0,
      },
      voter_user: "",
      targetSkillToDelete: "",
    };
  },
  methods: {
    showDialogDelete(targetSkill) {
      this.targetSkillToDelete = targetSkill;
      this.dialogDelete = true;
    },
    saveConfirm() {
      this.isConfirming = false;
      this.isEditing = false;
    },
    async updateTargetSkill(row, star) {
      try {
        const skill = this.skillDefinitions.find((e) => e.id == row.skill_id);
        const skillDefId = skill.level[star - 1].definition;
        const data = {
          target_user: row.target_user,
          skill_definition: skillDefId,
        };
        const res = await TargetSkill.update(row.id, data);
        if (res.status === 201 || res.status === 200) {
          this.$toast.success("Update success");
          await this.getTargetSkill();
        }
      } catch (err) {
        this.$toast.error("Update error");
      }
    },
    async deleteTargetSkill() {
      try {
        const targetSkill = this.targetSkillToDelete;
        const res = await TargetSkill.delete(targetSkill.id);
        if (res.status === 204) {
          this.$toast.success("Delete success");
          this.dialogDelete = false;
          this.targetSkillToDelete = "";
          await this.getTargetSkill();
        }
      } catch (err) {
        this.$toast.error("Delete Failed");
      }
    },
    async AddTargetSkill(currentInput) {
      try {
        const skill = this.skillDefinitions.find(
          (e) => e.id == currentInput.skill_id
        );
        const level = skill.level.find((e) => e.id == currentInput.level_id);
        const data = {
          target_user: this.$route.params.id,
          skill_definition: level.definition,
        };
        const res = await TargetSkill.create(data);
        if (res.status === 200 || res.status === 201) {
          this.$toast.success("Add success");
          await this.getTargetSkill();
        }
      } catch (err) {
        this.$toast.error("Add Failed");
      }
    },
    async getTargetSkill() {
      try {
        const id = this.$route.params.id;
        const res = await TargetSkill.get(id);
        if (res.status === 201 || res.status === 200) {
          this.targetSkill = res.data;
          if (this.targetSkill.length !== 0) {
            this.isHiddenTable = false;
            this.targetSkill.map((e) => {
              this.skillDefinitions.forEach((skill) =>
                skill.level.forEach((item) => {
                  if (item.definition == e.skill_definition) {
                    e.level_id = item.id;
                    e.level_name = item.name;
                    e.skill_id = skill.id;
                    e.skill_name = skill.name;
                  }
                })
              );
            });
          } else this.isHiddenTable = true;
        }
      } catch (err) {
        console.log(err);
      }
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
    countStar(row) {
      const check = this.skillDefinitions.find((e) => e.id == row.skill_id);
      const star = check.level.findIndex((e) => e.id == row.level_id) + 1;
      return star;
    },
    maxStar(row) {
      const check = this.skillDefinitions.find((e) => e.id == row.skill_id);
      return check.level.length;
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
  },
  async created() {
    await this.getSkillDefinitions();
    await this.getTargetSkill();
    this.voter_user = localStorage.getItem("user_id");
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

@media screen and (max-width: 1024px) {
  .mobile-screen {
    margin-bottom: 65% !important;
    margin-top: 65% !important;
  }
}
</style>
