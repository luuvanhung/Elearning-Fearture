<template>
  <div>
    <div>
      <div class="d-flex bd-highlight">
        <div class="mr-auto p-2 bd-highlight">
          <el-date-picker
            placeholder="Search by date"
            v-model="search"
            value-format="yyyy-MM-dd"
          >
          </el-date-picker>
        </div>
        <restricted-view :scopes="['lunches:edit']">
          <template v-slot:default>
            <div class="p-2 bd-highlight">
              <el-button
                icon="el-icon-circle-plus-outline"
                type="primary"
                @click="addNewItem"
              >
                Add
              </el-button>
            </div>
          </template>
        </restricted-view>
      </div>
      <el-table
        highlight-current-row
        :data="
          desserts.filter(
            (item) =>
              !search || item.date.toLowerCase().includes(search.toLowerCase())
          )
        "
        header-cell-class-name="bg-header-table"
        border
      >
        <el-table-column label="Date" width="250" align="center">
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-date-picker
                :picker-options="{ firstDayOfWeek: 1 }"
                value-format="yyyy-MM-dd"
                class="data-input"
                v-model="scope.row.date"
                type="date"
                placeholder="Pick a date*"
              >
              </el-date-picker>
            </div>
            <div v-else>
              {{ scope.row.date }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="name_provider" label="Provider" align="center">
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-select
                v-model="scope.row.provider"
                placeholder="Provider*"
                class="data-input"
              >
                <el-option
                  v-for="provider in providers"
                  :label="provider.name"
                  :value="provider.id"
                  :key="provider.id"
                >
                </el-option>
              </el-select>
            </div>
            <div v-else>
              {{ scope.row.name_provider }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="Note">
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                type="textarea"
                class="dont-break-out"
                v-model="scope.row.note"
                :rows="10"
                :placeholder="scope.row.note === '' ? 'Note*' : scope.row.note"
              >
              </el-input>
            </div>
            <div v-else class="dont-break-out">
              {{ scope.row.note }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="has_veggie" label="Veggie" width="100">
          <template v-slot="scope">
            <el-checkbox
              v-model="scope.row.has_veggie"
              :disabled="!scope.row.editMode"
              >Veggie</el-checkbox
            >
          </template>
        </el-table-column>
        <el-table-column label="Action" width="150" align="center">
          <template v-slot="scope">
            <restricted-view :scopes="['lunches:edit']">
              <template v-slot:default>
                <div v-if="scope.row.editMode">
                  <el-button
                    circle
                    @click="saveEdit(scope.row, scope.$index)"
                    type="success"
                    icon="el-icon-check"
                  ></el-button>
                  <el-button
                    circle
                    type="danger"
                    icon="el-icon-close"
                    @click="cancelEdit(scope.$index)"
                  />
                </div>
                <div v-else>
                  <el-button
                    circle
                    style="cursor: pointer"
                    @click="editItem(scope.row)"
                    type="primary"
                    icon="el-icon-edit"
                  ></el-button>
                  <el-button
                    circle
                    style="cursor: pointer"
                    type="danger"
                    icon="el-icon-delete"
                    @click="deleteItem(scope.row)"
                  />
                </div>
              </template>
            </restricted-view>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="d-flex justify-content-center mt-5 mb-3">
      <el-pagination
        background
        layout="prev, pager, next"
        :page-count="dessertData.page_number"
        :current-page.sync="page"
        :page-size="itemsPerPage"
        @current-change="changePages"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import LunchScheduleService from "@/services/lunch_management/lunch_schedule";
import ProviderService from "@/services/lunch_management/provider";
import RestrictedView from "@/components/RestrictedView";

export default {
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  data: () => ({
    page: 1,
    itemsPerPage: 12,
    dessertData: {},
    editedIndex: -1,
    createdItem: {
      provider: "",
      note: "",
      date: "",
      has_veggie: false,
    },
    tempItem: {
      provider: "",
      note: "",
      date: "",
      has_veggie: false,
    },
    editedItem: {
      provider: "",
      note: "",
      date: "",
      has_veggie: false,
    },
    providers: [],
    isAdding: false,
    search: "",
  }),

  created() {
    this.getLunches();
    this.getProviders();
  },

  computed: {
    desserts() {
      return this.dessertData.results;
    },
  },

  methods: {
    async getLunches() {
      const params = {
        page: this.page,
        page_size: this.itemsPerPage,
      };
      const response = await LunchScheduleService.get(params);
      if (response) {
        this.dessertData = response;
      }
    },

    async getProviders() {
      const listProviders = await ProviderService.get();
      this.providers = listProviders.data ? listProviders.data : [];
    },

    editItem(item) {
      this.cancelAllEditMode();
      this.$set(item, "editMode", true);
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.tempItem = Object.assign({}, item);
    },

    async deleteItem(item) {
      if (
        confirm("Are you sure you want to delete this item?") &&
        this.desserts.splice(this.desserts.indexOf(item), 1) &&
        (await LunchScheduleService.delete(item.id))
      ) {
        this.$toast.success("Deleted Successfully");
      } else {
        this.$toast.error("Delete Failed");
      }
    },

    addNewItem() {
      this.cancelAllEditMode();
      this.desserts.unshift(this.createdItem);
      this.$set(this.createdItem, "editMode", true);
      this.isAdding = true;
    },

    async createNewItem(item) {
      try {
        const res = await LunchScheduleService.create(item);
        this.desserts.splice(0, 1);
        this.desserts.unshift(res.data);
        this.createdItem = {};
        this.isAdding = false;
        this.$set(this.createdItem, "editMode", false);
        this.$toast.success("Created Successfully!");
        await this.getLunches();
      } catch (e) {
        this.$toast.error("Create Failed");
      }
    },

    cancelCreate() {
      this.createdItem = {};
      this.$set(this.createdItem, "editMode", false);
      this.desserts.splice(0, 1);
      this.isAdding = false;
    },

    async changePages() {
      await this.getLunches(this.page, this.itemsPerPage);
    },

    async saveEdit(item, index) {
      if (!item.date || !item.provider || !item.note.trim()) {
        if (!this.isAdding) this.cancelEdit(index);
        this.$toast.error("Missing Data");
        return;
      }
      if (this.isAdding) {
        await this.createNewItem(item);
        return;
      }
      this.editedItem = Object.assign({}, item);
      Object.assign(this.desserts[this.editedIndex], this.editedItem);
      const data = {
        date: this.editedItem.date,
        note: this.editedItem.note,
        has_veggie: this.editedItem.has_veggie,
        provider: this.editedItem.provider,
      };
      const lunch = await LunchScheduleService.update({
        id: this.editedItem.id,
        data,
      });
      if (lunch && lunch.data.msg) {
        const content = lunch.data.msg;
        this.$toast.error(content);
      }
      if (lunch && lunch.data.note) {
        this.$toast.success("Updated Successfully!");
      }
      this.$set(item, "editMode", false);
      await this.getLunches();
    },

    cancelEdit(index) {
      if (this.isAdding) {
        this.cancelCreate();
        return;
      }
      this.$set(this.tempItem, "editMode", false);
      this.$set(this.desserts, index, this.tempItem);
    },

    cancelAllEditMode() {
      this.desserts.forEach((element, index) => {
        if (element.editMode) this.cancelEdit(index);
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
