<template>
  <div>
    <restricted-view :scopes="['skill_level:edit']">
      <template v-slot:default>
        <div class="d-flex justify-content-end mt-5">
          <button
            type="button"
            class="btn btn-primary btnHandleData"
            @click="addDataToTable"
          >
            <font-awesome-icon :icon="['fas', 'plus']" />
            <span class="ml-2">Add Level</span>
          </button>
        </div>
      </template>
    </restricted-view>
    <table class="tableData">
      <colgroup>
        <col class="col-2" />
        <col class="col-5" />
        <col class="col-3" />
        <col class="col-2" />
      </colgroup>
      <thead class="nameColumn">
        <tr>
          <th class="border-top-left-radius">ID</th>
          <th>Name</th>
          <th>Weight</th>
          <th class="border-top-right-radius">Actions</th>
        </tr>
      </thead>
      <transition-group
        tag="tbody"
        name="list"
        class="text-center"
        mode="out-in"
      >
        <tr v-for="level in levels" :key="level.id">
          <td>{{ level.id }}</td>
          <td>
            <span v-if="level.editMode">
              <input
                type="text"
                placeholder="Placeholder"
                v-model="level.name"
                class="m-auto"
              />
            </span>
            <span v-else>{{ level.name }} </span>
          </td>
          <td>
            <span v-if="level.editMode">
              <input
                type="number"
                placeholder="Placeholder"
                v-model="level.weight"
                class="m-auto"
              />
            </span>
            <span v-else>{{ level.weight }} </span>
          </td>
          <td>
            <restricted-view :scopes="['skill_level:edit']">
              <template v-slot:default>
                <div v-if="!level.editMode">
                  <img
                    :src="require('@/static/images/IconEdit.svg')"
                    class="mr-3"
                    @click="editData(level)"
                  />
                  <img
                    :src="require('@/static/images/IconDelete.svg')"
                    class="ml-3"
                    @click="deleteData(level.id)"
                  />
                </div>
                <div v-else>
                  <img
                    :src="require('@/static/images/IconCheck.svg')"
                    class="mr-3"
                    @click="saveDataTable(level)"
                  />
                  <img
                    :src="require('@/static/images/IconCancel.svg')"
                    class="ml-3"
                    @click="cancelEditDataTable(level)"
                  />
                </div>
              </template>
            </restricted-view>
          </td>
        </tr>
      </transition-group>
    </table>
  </div>
</template>

<script>
import SkillLevels from "@/services/skill/level";
import RestrictedView from "@/components/RestrictedView";
export default {
  name: "SkillLevel",
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  data() {
    return {
      edit: false,
      editLevel: [],
      levels: [],
    };
  },
  created() {
    this.getData();
  },
  methods: {
    async getData() {
      const res = await SkillLevels.getAll();
      return (this.levels = res.data.results);
    },
    async deleteData(id) {
      try {
        const res = await SkillLevels.delete(id);
        if (res.status === 204) {
          this.edit = false;
          const index = this.levels.findIndex((item) => item.id === id);
          this.levels.splice(index, 1);
          this.$toast.success("Deleted Successfully");
        }
      } catch (err) {
        this.$toast.error("Delete Failed");
      }
    },
    addDataToTable() {
      if (this.levels.find((level) => level.id === null) === undefined) {
        let data = {
          isEdit: false,
          editMode: true,
          level: {
            id: null,
            name: "",
            weight: "",
          },
        };
        this.levels.push(data);
      }
    },
    async saveDataTable(level) {
      if (level.isEdit === false) {
        try {
          const res = await SkillLevels.create(level);
          if (res.status === 201) {
            const index = this.levels.findIndex((e) => e.isEdit === false);
            this.levels.splice(index, 1);
            this.levels.push(res.data);
            this.$set(level, "editMode", false);
            this.$toast.success("Added Successfully");
          }
        } catch (err) {
          this.$toast.error("Add Failed");
        }
      } else {
        try {
          const res = await SkillLevels.update(level.id, level);
          if (res.status === 200) {
            this.$set(level, "editMode", false);
            this.editLevel = { ...level };
            this.$toast.success("Edited Successfully");
          }
        } catch (err) {
          this.$toast.error("Edit Failed");
        }
      }
    },
    editData(levelRow) {
      this.$set(levelRow, "editMode", true);
      levelRow.oldName = levelRow.name;
      levelRow.oldWeight = levelRow.weight;
    },
    cancelEditDataTable(levelRow) {
      if (levelRow.isEdit === false) {
        const index = this.levels.findIndex((e) => e.isEdit === false);
        this.levels.splice(index, 1);
      } else {
        this.$set(levelRow, "editMode", false);
        levelRow.name = levelRow.oldName;
        levelRow.weight = levelRow.oldWeight;
      }
    },
  },
};
</script>
<style scoped>
.border-top-left-radius {
  border-top-left-radius: 10px;
}

.border-top-right-radius {
  border-top-right-radius: 10px;
}

.btnHandleData {
  font-family: "Times New Roman", Times, serif;
  font-weight: bold;
  font-size: 16px;
  width: 8%;
  height: 45px;
  color: #ffffff;
  background: #25c9d0;
  border: 1px solid #c6c6c6;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 8px;
}

.list-enter-active {
  transition: all 0.3s ease;
}

.list-leave-active {
  transition: all 0.5s cubic-bezier(1, 0.5, 0.8, 1);
}

.list-enter,
.list-leave-to {
  transform: translateX(10px);
  opacity: 0;
}

.contentInput {
  border: 1px solid #707070;
}

.tableData {
  height: auto;
  width: 100%;
  border-collapse: collapse;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  transition: height 0.3s ease-in-out;
}

tr {
  transition: all 1s ease-in-out;
}

.formInput {
  width: 30%;
  border-collapse: collapse;
  height: 350px;
  padding-left: 10px !important;
}

td {
  border: 1px solid #707070;
  border-spacing: 0;
  height: 50px;
}

img {
  cursor: pointer;
}

p {
  color: #25c9d0;
}

i {
  color: #707070;
}

.nameColumn {
  width: 100%;
  height: 58px;
  color: #ffffff;
  background: #25c9d0;
  font-family: "Times New Roman", Times, serif;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  line-height: 58px;
}

i {
  width: 25%;
  font-size: 14px;
}

input {
  display: block;
  width: 200px;
  height: 28px;
  border: 1px solid;
  border-radius: 5px;
  padding-left: 8px;
}

.mainContent {
  margin-top: 70px;
}
</style>
