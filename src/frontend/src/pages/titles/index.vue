<template>
  <div class="title-page">
    <div v-if="!checkedListTitle">
      <h2 class="text-info text-center m-4">There's no titles yet</h2>
      <restricted-view :scopes="['title:create']">
        <template v-slot:default>
          <div class="d-flex justify-content-center">
            <el-button type="primary">
              <font-awesome-icon :icon="['fas', 'plus']" />
              Create Title
            </el-button>
          </div>
        </template>
      </restricted-view>
    </div>
    <div v-else>
      <el-row
        class="mt-3 mb-3 d-flex justify-content-between align-items-center"
      >
        <el-input
          class="ml-3"
          placeholder="Search here"
          v-model="searchName"
          style="width: 25%; order: -1"
        ></el-input>
        <restricted-view :scopes="['title:create']" style="order: 1">
          <template v-slot:default>
            <el-row>
              <el-button type="primary" class="mt-3" @click="showCreatingModal">
                <font-awesome-icon :icon="['fas', 'plus']" />
                Create New Title
              </el-button>
            </el-row>
          </template>
        </restricted-view>
      </el-row>
      <el-table
        highlight-current-row
        :data="search"
        header-cell-class-name="bg-header-table"
        border
        style="margin-bottom: 20px"
      >
        <el-table-column prop="title_name" sortable label="Titles Name">
          <template slot-scope="scope">
            <div class="text-center">
              <el-button
                type="text"
                @click="showUpdatingModal(scope.row.id, scope.row.title)"
              >
                <strong>{{ scope.row.title }}</strong>
              </el-button>
            </div>
          </template>
        </el-table-column>
        <el-table-column
          v-if="hasScope('title:destroy')"
          label="Action"
          width="300"
          align="center"
        >
          <template v-slot="scope">
            <el-button
              circle
              style="cursor: pointer"
              type="danger"
              icon="el-icon-delete"
              @click="showModalRemove(scope.row.id, scope.row.title)"
            ></el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-dialog :visible.sync="isDialogRemove" hide-footer hide-header="">
        <div class="d-block text-center text-danger">
          <h3>Remove title</h3>
        </div>
        <div class="d-block text-center mb-4 mt-4">
          Do you want to remove title
          <p class="text-danger d-inline">{{ currentTitleName }}</p>
        </div>
        <div class="d-flex justify-content-center">
          <el-button type="primary" @click="removeTitle">Remove</el-button>
          <el-button type="danger" @click="hideModal">Cancel</el-button>
        </div>
      </el-dialog>

      <el-dialog :visible.sync="isDialogCreate" hide-footer hide-header="">
        <div class="d-block text-center text-danger mb-4">
          <h3 v-if="isUpdating">{{ currentTitleName }}</h3>
          <h3 v-else>Create title</h3>
        </div>
        <el-form ref="form" :model="form" label-width="120px" :rules="rules">
          <el-form-item label="Title name" prop="title">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('form')">
              <span v-if="isUpdating">Update</span>
              <span v-else>Create</span>
            </el-button>
            <el-button type="danger" @click="hideModal">Cancel</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import TitleService from "@/services/titles/titles.services";
import RestrictedView from "@/components/RestrictedView";
import { mapGetters } from "vuex";

export default {
  name: "titles",
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  data() {
    return {
      rows: [],
      searchName: "",
      currentTitleId: "",
      currentTitleName: "",
      isDialogRemove: false,
      isDialogCreate: false,
      isUpdating: false,
      form: {
        title: "",
      },
      rules: {
        title: [
          {
            required: true,
            message: "Please input Title name",
            trigger: "blur",
          },
          {
            min: 1,
            max: 50,
            message: "Length should be 1 to 50",
            trigger: "blur",
          },
        ],
      },
    };
  },
  created() {
    this.getAllTitleData();
  },
  computed: {
    ...mapGetters({
      tokenInfo: "scope/tokenInfo",
    }),
    checkedListTitle: function () {
      return !!(
        (this.rows !== null) &
        (this.rows !== undefined) &
        (this.rows.length !== 0)
      );
    },
    search: function () {
      return this.rows.filter((data) =>
        data.title.toLowerCase().includes(this.searchName.toLowerCase())
      );
    },
  },
  methods: {
    async getAllTitleData() {
      const res = await TitleService.getAll();
      this.rows = res.data;
    },

    hasScope(scope) {
      return this.tokenInfo["scope"].indexOf(scope) !== -1;
    },

    showModalRemove(id, name) {
      this.currentTitleId = id;
      this.currentTitleName = name;
      this.isDialogRemove = true;
    },

    showUpdatingModal(id, name) {
      if (!this.hasScope("title:edit")) return;
      this.currentTitleId = id;
      this.currentTitleName = name;
      this.isDialogCreate = true;
      this.form.title = name;
      this.isUpdating = true;
    },

    hideModal() {
      this.isDialogRemove = false;
      this.isDialogCreate = false;
    },

    removeTitle: async function () {
      try {
        await TitleService.removeTitle(this.currentTitleId);
        this.$toast.success("Removed Successfully");
      } catch (e) {
        this.$toast.error("Remove Failed");
      }
      await this.getAllTitleData();
      this.isDialogRemove = false;
    },

    submitForm(form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          if (this.isUpdating) {
            this.updateTitle();
          } else {
            this.createTitle();
          }
        } else {
          return false;
        }
      });
    },

    showCreatingModal() {
      this.form.title = "";
      this.isDialogCreate = true;
      this.isUpdating = false;
    },

    async createTitle() {
      return TitleService.create(this.form)
        .then((res) => {
          if (res.data) {
            this.$toast.success("Added Successfully");
            this.form.title = "";
            this.isDialogCreate = false;
          } else {
            this.$toast.error("Input is not valid");
          }
          this.getAllTitleData();
        })
        .catch(() => {
          this.$toast.error("Input is not valid");
        });
    },

    async updateTitle() {
      if (this.form.title === this.currentTitleName) {
        this.isDialogCreate = false;
        return this.$toast.success("Updated Successfully");
      }
      return TitleService.update(this.currentTitleId, this.form)
        .then((res) => {
          if (res.data) {
            this.$toast.success("Updated Successfully");
            this.form.title = "";
            this.isDialogCreate = false;
          } else {
            this.$toast.error("Input is not valid");
          }
          this.getAllTitleData();
        })
        .catch(() => {
          this.$toast.error("Input is not valid");
        });
    },
  },
};
</script>
<style lang="scss">
@import "./style.scss";
</style>
