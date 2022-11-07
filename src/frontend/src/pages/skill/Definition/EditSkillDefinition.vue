<template>
  <form>
    <h5 class="header">Edit Skill</h5>
    <div class="col p-4 content">
      <div class="inputContent">
        <div class="d-flex">
          <div class="col-10">
            <span class="input-label">Skill:</span>
            <el-input
              placeholder="Please input"
              v-model="currentDefinition.skill.name"
              class="inputName"
            ></el-input>
          </div>
          <div
            class="col-2 d-flex justify-content-center align-items-center btnSaveSkill"
            @click="editSkill(currentDefinition)"
          >
            <span>Save</span>
          </div>
        </div>
        <div class="p-2 border-definition">
          <h3 class="text-center">Definition</h3>
          <div
            class="d-flex justify-content-center align-items-center btnHandleData"
            @click="createDefinition()"
          >
            Add Definition
          </div>
          <table>
            <colgroup>
              <col class="col-2" />
              <col class="col-7" />
              <col class="col-3" />
            </colgroup>
            <thead class="nameColumn">
              <th class="border-top-left-radius">Level</th>
              <th>Requirements</th>
              <th class="border-top-right-radius">Actions</th>
            </thead>
            <tbody class="text-center">
              <tr
                v-for="(definition, index) in arrSkillDefinitionEdit"
                :key="index"
              >
                <td>
                  <span v-if="definition.editMode">
                    <el-select
                      v-model="definition.level.name"
                      class="inputName"
                    >
                      <el-option
                        v-for="level in editLevels"
                        :key="level.id"
                        :label="level.name"
                        :value="level.name"
                      >
                      </el-option>
                    </el-select>
                  </span>
                  <span v-else>{{ definition.level.name }}</span>
                </td>
                <td class="text-left" style="white-space: pre-wrap">
                  <span v-if="definition.editMode">
                    <el-input
                      type="textarea"
                      :autosize="{ minRows: 2, maxRows: 4 }"
                      placeholder="Please fill input"
                      v-model="definition.requirements"
                      class="inputName"
                    >
                    </el-input>
                  </span>
                  <span v-else style="white-space: pre-wrap">{{
                    definition.requirements
                  }}</span>
                </td>
                <td>
                  <div v-if="!definition.editMode">
                    <img
                      :src="require('@/static/images/IconEdit.svg')"
                      @click="editDataTable(definition)"
                    />
                    <img
                      :src="require('@/static/images/IconDelete.svg')"
                      @click="deleteDefinition(definition)"
                    />
                  </div>
                  <div v-else>
                    <img
                      :src="require('@/static/images/IconCheck.svg')"
                      class="mr-3"
                      @click="saveDataTable(definition)"
                    />
                    <img
                      :src="require('@/static/images/IconCancel.svg')"
                      class="ml-3"
                      @click="cancelEditDataTable(definition)"
                    />
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </form>
</template>
<script>
import SkillDefinitions from "@/services/skill/definition";
import SkillLevels from "@/services/skill/level";

export default {
  name: "EditSkillDefinition",
  middleware: "authentication",
  props: {
    skillDefinitionEdit: Object,
  },
  data() {
    return {
      currentDefinition: {
        id: "",
        skill: {
          id: "",
          name: this.skillDefinitionEdit.name,
        },
        requirements: "",
        level: {
          id: "",
          name: "",
        },
      },
      isEdit: true,
      arrSkillDefinitionEdit: [],
      editLevels: [],
      allLevels: [],
    };
  },
  async created() {
    const res = await SkillLevels.getAll();
    this.allLevels = res.data.results;
    this.editLevels = this.allLevels.filter(
      (level) =>
        this.skillDefinitionEdit.data.filter(
          (skillDefinition) => skillDefinition.level.id === level.id
        ).length === 0
    );
    this.arrSkillDefinitionEdit = this.skillDefinitionEdit.data.map((e) => e);
  },
  beforeUpdate() {
    this.editLevels = this.allLevels.filter(
      (level) =>
        this.skillDefinitionEdit.data.filter(
          (skillDefinition) => skillDefinition.level.id === level.id
        ).length === 0
    );
  },
  watch: {
    skillDefinitionEdit: function (element) {
      this.currentDefinition.skill.name = element.name;
      this.arrSkillDefinitionEdit = element.data;
    },
  },
  methods: {
    async editSkill(currentDefinition) {
      try {
        const resSkill = await SkillDefinitions.updateSkill(
          this.skillDefinitionEdit.id,
          currentDefinition.skill
        );
        if (resSkill.status === 200) {
          this.$emit("update-skill", resSkill.data);
          this.$toast.success("Edited Successfully");
        }
      } catch (err) {
        const myJSX = <span>{err.response.data.name}</span>;
        this.$toast.error(myJSX);
      }
    },
    editDataTable(definition) {
      this.$set(definition, "editMode", true);
      definition.oldRequirements = definition.requirements;
      definition.oldLevel = definition.level;
      this.editLevels = this.allLevels.filter(
        (level) =>
          this.skillDefinitionEdit.data.filter(
            (skillDefinition) => skillDefinition.level.id === level.id
          ).length === 0
      );
    },
    async saveDataTable(definition) {
      if (definition.isEdit === false) {
        definition.level = this.allLevels.find(
          (level) => level.name === definition.level.name
        );
        definition.skill = {
          id: this.skillDefinitionEdit.id,
          name: definition.skill.name,
        };
        try {
          const res = await SkillDefinitions.create(definition);
          if (res.status === 201) {
            this.$set(definition, "editMode", false);
            this.skillDefinitionEdit.data.push(res.data);
            this.arrSkillDefinitionEdit.push(res.data);
            const index = this.arrSkillDefinitionEdit.findIndex(
              (e) => e.id === null
            );
            this.arrSkillDefinitionEdit.splice(index, 1);
            this.$toast.success("Added Successfully");
          }
        } catch (err) {
          this.$toast.error("Add Failed");
        }
      } else {
        try {
          definition.level = this.allLevels.find(
            (level) => level.name === definition.level.name
          );
          const res = await SkillDefinitions.update(definition.id, definition);
          if (res.status === 200) {
            this.$toast.success("Edited Successfully");
            this.$set(definition, "editMode", false);
          }
        } catch (err) {
          this.$toast.error("Edit Failed");
        }
      }
    },
    async deleteDefinition(definition) {
      try {
        const res = await SkillDefinitions.delete(definition.id);
        if (res.status === 204) {
          this.$toast.success("Deleted Successfully");
          const index = this.skillDefinitionEdit.data.findIndex(
            (e) => e.id === definition.id
          );
          const indexArr = this.arrSkillDefinitionEdit.findIndex(
            (e) => e.id === definition.id
          );
          this.skillDefinitionEdit.data.splice(index, 1);
          this.arrSkillDefinitionEdit.splice(indexArr, 1);
        }
      } catch (err) {
        this.$toast.error("Delete Failed");
      }
    },
    cancelEditDataTable(definition) {
      if (definition.isEdit === false) {
        const index = this.arrSkillDefinitionEdit.findIndex(
          (e) => e.isEdit === false
        );
        this.arrSkillDefinitionEdit.splice(index, 1);
      } else {
        this.$set(definition, "editMode", false);
        definition.requirements = definition.oldRequirements;
        definition.level = definition.oldLevel;
      }
    },
    async createDefinition() {
      if (
        this.arrSkillDefinitionEdit.find(
          (definition) => definition.id === null
        ) === undefined
      ) {
        let creatingDefinition = {
          isEdit: false,
          id: null,
          editMode: true,
          level: {
            id: null,
            name: "",
          },
          requirements: "",
          skill: {
            id: this.skillDefinitionEdit.id,
            name: this.skillDefinitionEdit.name,
          },
        };
        this.arrSkillDefinitionEdit.push(creatingDefinition);
      }
    },
  },
};
</script>
<style scoped>
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

.inputContent {
  border: 1px solid #707070;
  padding: 2%;
}

table {
  margin-top: 2%;
  width: 100%;
  border-collapse: collapse;
}

td {
  border: 1px solid #707070;
  border-spacing: 0;
  height: auto;
  padding: 2%;
}

.btnHandleData {
  font-family: "Times New Roman", Times, serif;
  font-weight: bold;
  font-size: 16px;
  width: 15%;
  height: 40px;
  color: #ffffff;
  background: #25c9d0;
  border: 1px solid #c6c6c6;
  margin-left: auto;
  border-radius: 5px;
  cursor: pointer;
}

.btnSaveSkill {
  font-family: "Times New Roman", Times, serif;
  font-weight: bold;
  font-size: 16px;
  width: 15%;
  height: 40px;
  color: #ffffff;
  background: #25c9d0;
  border: 1px solid #c6c6c6;
  border-radius: 5px;
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
