<template>
  <div>
    <restricted-view :scopes="['skill_definition:edit']">
      <template v-slot:default>
        <div class="d-flex justify-content-end mt-5">
          <button
            type="button"
            class="btn btn-primary"
            @click="dialogAdd = true"
          >
            <font-awesome-icon :icon="['fas', 'plus']" />
            <span class="ml-2">Add</span>
          </button>
        </div>
      </template>
    </restricted-view>
    <table class="tableData mt-2">
      <colgroup>
        <col class="col-2" />
        <col class="col-2" />
        <col class="col-6" />
        <col class="col-2" />
      </colgroup>
      <thead class="name-column">
        <tr>
          <td class="border-top-left-radius">Skill</td>
          <td>Levels</td>
          <td>Requirements</td>
          <td class="border-top-right-radius">Actions</td>
        </tr>
      </thead>
      <transition-group
        name="list"
        mode="out-in"
        tag="tbody"
        class="text-center"
      >
        <template v-for="skillDefinition in skillDefinitions">
          <tr v-for="(item, index) in skillDefinition.data" :key="item.id">
            <td :rowspan="skillDefinition.data.length" v-if="index === 0">
              {{ skillDefinition.name }}
            </td>
            <td>{{ item.level.name }}</td>
            <td class="text-left p-2" style="white-space: pre-wrap">
              {{ item.requirements }}
            </td>
            <td :rowspan="skillDefinition.data.length" v-if="index === 0">
              <restricted-view :scopes="['skill_definition:edit']">
                <template v-slot:default>
                  <img
                    :src="require('@/static/images/IconEdit.svg')"
                    @click="editData(skillDefinition)"
                  />
                  <img
                    :src="require('@/static/images/IconDelete.svg')"
                    @click="dialogDelete = true"
                  />
                </template>
              </restricted-view>
            </td>
            <el-dialog :visible.sync="dialogDelete" width="30%">
              <h4>Are you sure to delete this element?</h4>
              <div class="mt-3">
                <img
                  :src="require('@/static/images/IconCheck.svg')"
                  class="mr-3"
                  @click="deleteData(skillDefinition.id)"
                />
                <img
                  :src="require('@/static/images/IconCancel.svg')"
                  class="ml-3"
                  @click="dialogDelete = false"
                />
              </div>
            </el-dialog>
          </tr>
        </template>
      </transition-group>
    </table>
    <el-dialog
      :visible.sync="dialogAdd"
      :before-close="handleClose"
      destroy-on-close
    >
      <AddSkillDefinition @update-definition="updateData" />
    </el-dialog>
    <el-dialog
      :visible.sync="dialogEdit"
      destroy-on-close
      :before-close="handleClose"
    >
      <EditSkillDefinition
        :skillDefinitionEdit="skillDefinitionEdit"
        @update-skill="updateData"
      />
    </el-dialog>
    <div class="d-flex justify-content-center mt-5">
      <el-pagination
        background
        layout="prev, pager, next"
        :current-page.sync="page"
        :page-size="page_size"
        :total="totalRecords"
        @current-change="updateData"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import AddSkillDefinition from "./AddSkillDefinition";
import EditSkillDefinition from "./EditSkillDefinition";
import SkillDefinition from "@/services/skill/definition";
import RestrictedView from "@/components/RestrictedView";

export default {
  components: { EditSkillDefinition, AddSkillDefinition, RestrictedView },
  created() {
    this.getData();
  },
  data() {
    return {
      dialogAdd: false,
      dialogEdit: false,
      dialogDelete: false,
      skillDefinitions: [],
      skillDefinitionEdit: "",
      page: 1,
      page_size: 12,
      totalRecords: 0,
    };
  },
  methods: {
    async getData() {
      const res = await SkillDefinition.getAll(this.page, this.page_size);
      this.totalRecords = res.data.count;
      this.skillDefinitions = this.handleDataAPI(res.data.results);
    },
    handleClose(done) {
      this.$confirm("Are you sure to close this dialog?")
        .then(() => {
          done();
        })
        .catch((err) => {
          console.log(err);
        });
    },
    editData(data) {
      this.skillDefinitionEdit = data;
      this.dialogEdit = true;
    },
    async deleteData(skill_id) {
      try {
        const res = await SkillDefinition.deleteAll(skill_id);
        if (res.status === 204) {
          this.dialogDelete = false;
          const index = this.skillDefinitions.findIndex(
            (skill) => skill.id === skill_id
          );
          if (index >= 0) {
            this.skillDefinitions.splice(index, 1);
            this.$toast.success("Delete success");
          }
        }
      } catch (err) {
        this.$toast.error("Delete Failed");
      }
    },
    handleDataAPI(dataAPI) {
      const uniqueSkill = _.uniqBy(dataAPI, "skill.id");
      return uniqueSkill.map((skillArray) => {
        const newData = {
          id: skillArray.skill.id,
          name: skillArray.skill.name,
          data: [],
        };
        dataAPI.forEach((item) => {
          if (item.skill.id === skillArray.skill.id) {
            newData.data.push(item);
          }
        });
        return newData;
      });
    },
    async updateData(page) {
      await this.getData(page, this.page_size);
    },
  },
};
</script>

<style scoped>
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

button {
  width: 8%;
  height: 45px;
  color: #ffffff;
  background: #25c9d0;
  font-weight: bold;
  font-family: "Times New Roman", Times, serif;
  border: none;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
}

.name-column {
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

img {
  cursor: pointer;
}

tbody tr td {
  border: 1px solid #707070;
  border-spacing: 0;
  height: 50px;
}

.tableData {
  height: auto;
  width: 100%;
  border-collapse: collapse;
  transition: height 0.3s ease-in-out;
}

.border-top-left-radius {
  border-top-left-radius: 10px;
}

.border-top-right-radius {
  border-top-right-radius: 10px;
}

tr {
  transition: all 1s ease-in-out;
}
</style>
