<template>
  <form @submit.prevent="addData(currentDefinition)">
    <h5 class="header">Add Skill</h5>
    <div class="col p-4 content">
      <div class="p-2">
        <span class="input-label">Skill:</span>
        <el-input
          placeholder="Please fill input"
          v-model="currentDefinition.skill.name"
          class="inputName"
        ></el-input>
      </div>
      <div class="p-2 border-definition">
        <h3 class="text-center m-3 main--title">Definition</h3>
        <div class="mt-3 d-flex align-items-center">
          <span class="input-label">Levels:</span>
          <el-select v-model="currentDefinition.level.name" class="inputName">
            <el-option
              v-for="level in remainingLevels"
              :key="level.id"
              :label="level.name"
              :value="level.name"
            >
            </el-option>
          </el-select>
        </div>
        <div class="mt-3">
          <span class="input-label" style="line-height: 54px"
            >Requirements:</span
          >
          <el-input
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4 }"
            placeholder="Please fill input"
            v-model="currentDefinition.requirements"
            class="inputName"
          >
          </el-input>
        </div>
        <div
          class="d-flex justify-content-center align-items-center btnAddDataTable"
          @click="AddToTable(currentDefinition)"
        >
          <span>Add to table</span>
        </div>
        <table>
          <colgroup>
            <col class="col-3" />
            <col class="col-6" />
            <col class="col-3" />
          </colgroup>
          <thead class="nameColumn">
            <th class="border-top-left-radius">Level</th>
            <th>Requirements</th>
            <th class="border-top-right-radius">Actions</th>
          </thead>
          <tbody class="text-center">
            <tr
              class="item-row"
              v-for="(item, index) in arrDefinition"
              :key="index"
            >
              <td>
                <span v-if="item.editMode">
                  <el-select v-model="item.level.id" class="inputName">
                    <el-option
                      v-for="level in editLevels"
                      :key="level.id"
                      :label="level.name"
                      :value="level.id"
                    >
                      {{ level.name }}
                    </el-option>
                  </el-select>
                </span>
                <span v-else>{{ item.level.name }}</span>
              </td>
              <td class="text-left" style="white-space: pre-wrap">
                <span v-if="item.editMode">
                  <el-input
                    type="textarea"
                    :autosize="{ minRows: 2, maxRows: 4 }"
                    placeholder="Please fill input"
                    v-model="item.requirements"
                    class="inputName"
                  >
                  </el-input>
                </span>
                <span v-else>{{ item.requirements }}</span>
              </td>
              <td>
                <div v-if="!item.editMode">
                  <img
                    :src="require('@/static/images/IconEdit.svg')"
                    @click="editDataTable(item)"
                  />
                  <img
                    :src="require('@/static/images/IconDelete.svg')"
                    @click="deleteDataTable(item)"
                  />
                </div>
                <div v-else>
                  <img
                    :src="require('@/static/images/IconCheck.svg')"
                    class="mr-3"
                    @click="saveDataTable(item)"
                  />
                  <img
                    :src="require('@/static/images/IconCancel.svg')"
                    class="ml-3"
                    @click="cancelEditDataTable(item)"
                  />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button
        type="submit"
        class="d-flex justify-content-center align-items-center addData"
      >
        Save
      </button>
    </div>
  </form>
</template>
<script>
import SkillDefinitions from "@/services/skill/definition";
import SkillLevels from "@/services/skill/level";

export default {
  name: "AddSkillDefinition",
  middleware: "authentication",
  data() {
    return {
      currentDefinition: {
        skill: {
          name: "",
        },
        requirements: "",
        level: {
          id: "",
          name: "",
        },
      },
      levels: [],
      remainingLevels: [],
      editLevels: [],
      arrDefinition: [],
    };
  },
  async created() {
    const res = await SkillLevels.getAll();
    this.levels = res.data.results;
    this.remainingLevels = this.levels.slice();
  },
  methods: {
    updateRemainingLevels() {
      this.remainingLevels = this.levels.slice();
      this.arrDefinition.forEach((definition) => {
        let index = this.remainingLevels.findIndex(
          (level) => level.id === definition.level.id
        );
        this.remainingLevels.splice(index, 1);
      });
    },
    editDataTable(levelRow) {
      this.$set(levelRow, "editMode", true);
      levelRow.oldRequirements = levelRow.requirements;
      levelRow.oldLevel = levelRow.level;
      this.editLevels = this.levels.filter(
        (level) =>
          this.arrDefinition.filter((e) => e.level.name === level.name)
            .length === 0
      );
      this.editLevels.push(Object.assign({}, levelRow.level));
    },
    saveDataTable(levelRow) {
      this.$set(levelRow, "editMode", false);
      levelRow.level = Object.assign(
        {},
        this.levels.find((level) => level.id === levelRow.level.id)
      );
      this.updateRemainingLevels();
    },
    cancelEditDataTable(levelRow) {
      this.$set(levelRow, "editMode", false);
      levelRow.requirements = levelRow.oldRequirements;
      levelRow.level = levelRow.oldLevel;
    },
    deleteDataTable(levelRow) {
      const index = this.arrDefinition.findIndex(
        (e) => e.level.id === levelRow.level.id
      );
      if (index >= 0) {
        this.arrDefinition.splice(index, 1);
        this.updateRemainingLevels();
      }
    },
    AddToTable(currentDefinition) {
      if (
        !(
          currentDefinition.level.name === "" ||
          currentDefinition.requirements === ""
        )
      ) {
        currentDefinition.level = this.levels.find(
          (level) => level.name === currentDefinition.level.name
        );
        let tmp = Object.assign({}, currentDefinition.level);
        this.arrDefinition.push({
          level: tmp,
          requirements: currentDefinition.requirements,
        });
        this.updateRemainingLevels();
        this.currentDefinition.requirements = {
          ...this.currentDefinition.level
        } = "";
        this.$toast.success("Added Successfully");
      } else {
        this.$toast.error("These fields is required");
      }
    },
    async addData(currentDefinition) {
      let data = {
        skill_name: currentDefinition.skill.name,
        skill_definitions: this.arrDefinition,
      };
      try {
        const res = await SkillDefinitions.createMultiple(data);
        if (res.status === 201) {
          this.$emit("update-definition");
          this.currentDefinition.skill.name =
            this.currentDefinition.requirements =
            { ...this.currentDefinition.level } =
              "";
          this.arrDefinition.splice(0, this.arrDefinition.length);
          this.updateRemainingLevels();
          this.$toast.success("Saved Successfully");
        }
      } catch (err) {
        this.$toast.error("Save Failed");
      }
    },
  },
};
</script>
<style scoped>
.main--title {
  font-family: "Times New Roman", Times, serif;
  font-size: 18px;
}

img {
  cursor: pointer;
}

.border-top-left-radius {
  border-top-left-radius: 10px;
}

.border-top-right-radius {
  border-top-right-radius: 10px;
}

.header {
  width: 100%;
  color: #ffffff;
  background: #25c9d0;
  font-size: large;
  font-family: "Times New Roman", Times, serif;
  height: 40px;
  line-height: 40px;
  padding-left: 20px;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.content {
  border: 1px solid #c6c6c6;
}

.border-definition {
  border-radius: 10px;
  margin-top: 2%;
  box-shadow: 0 0 5px #c6c6c6;
}

.btnAddDataTable {
  font-family: "Times New Roman", Times, serif;
  font-weight: bold;
  font-size: 16px;
  width: 15%;
  height: 40px;
  color: #ffffff;
  background: #25c9d0;
  border: 1px solid #c6c6c6;
  border-radius: 5px;
  margin: 3% auto 0;
  cursor: pointer;
}

table {
  margin-top: 4%;
  width: 100%;
  border-collapse: collapse;
}

td {
  border: 1px solid #707070;
  border-spacing: 0;
  height: auto;
  padding: 2%;
}

.addData {
  font-family: "Times New Roman", Times, serif;
  font-weight: bold;
  font-size: 16px;
  width: 15%;
  height: 40px;
  color: #ffffff;
  background: #25c9d0;
  border: 1px solid #c6c6c6;
  border-radius: 5px;
  margin: 3% auto 0;
  cursor: pointer;
}

.inputName {
  width: 80%;
}

form {
  margin: auto;
}

.input-label {
  display: inline-block;
  width: 20%;
}

.nameColumn {
  width: 100%;
  height: 3%;
  color: #ffffff;
  background: #25c9d0;
  font-family: "Times New Roman", Times, serif;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  line-height: 58px;
}
</style>
