<template>
  <restricted-view :scopes="['provider:view']">
    <template v-slot:default>
      <div class="d-flex bd-highlight">
        <div class="mr-auto p-2 bd-highlight">
          <el-input placeholder="Search by name" v-model="search"></el-input>
        </div>
        <restricted-view :scopes="['provider:edit']">
          <template v-slot:default>
            <div class="p-2 bd-highlight">
              <el-button type="primary" class="ml-4">
                <download-excel
                  :fetch="fetchDataForExportExcel"
                  :fields="json_fields"
                  worksheet="My Worksheet"
                  title="Providers"
                  name="provider.xls"
                >
                  <font-awesome-icon :icon="['fas', 'file-export']" />
                  Export file
                </download-excel>
              </el-button>
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
              !search || item.name.toLowerCase().includes(search.toLowerCase())
          )
        "
        header-cell-class-name="bg-header-table"
        border
      >
        <el-table-column prop="name" label="Name" align="center">
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                v-model="scope.row.name"
                :placeholder="scope.row.name === '' ? 'Name*' : scope.row.name"
              >
              </el-input>
            </div>
            <div v-else>
              {{ scope.row.name }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="Phone" width="150" align="center">
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                v-model="scope.row.phone"
                type="number"
                placeholder="Phone*"
              ></el-input>
            </div>
            <div v-else>
              {{ scope.row.phone }}
            </div>
          </template>
        </el-table-column>
        <el-table-column
          prop="budget"
          label="Budget"
          width="150"
          align="center"
        >
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                v-model="scope.row.budget"
                type="number"
                placeholder="Budget*"
              ></el-input>
            </div>
            <div v-else>
              {{ scope.row.budget }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="address" label="Address">
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                type="textarea"
                :rows="3"
                class="dont-break-out"
                v-model="scope.row.address"
                :placeholder="
                  scope.row.address === '' ? 'Address*' : scope.row.address
                "
              >
              </el-input>
            </div>
            <div v-else class="dont-break-out">
              {{ scope.row.address }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="link" label="Link">
          <template v-slot="scope">
            <div v-if="scope.row.editMode">
              <el-input
                class="dont-break-out"
                v-model="scope.row.link"
                :placeholder="scope.row.link === '' ? 'Link' : scope.row.link"
              ></el-input>
            </div>
            <div v-else class="dont-break-out">
              {{ scope.row.link }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="has_vegetarian" label="Veggie" width="100">
          <template v-slot="scope">
            <el-checkbox
              v-model="scope.row.has_vegetarian"
              :disabled="!scope.row.editMode"
              >Veggie</el-checkbox
            >
          </template>
        </el-table-column>
        <el-table-column label="Action" width="150" align="center">
          <template v-slot="scope">
            <restricted-view :scopes="['provider:edit']">
              <template v-slot:default>
                <div v-if="scope.row.editMode">
                  <el-button
                    circle
                    style="cursor: pointer"
                    @click="saveEdit(scope.row, scope.$index)"
                    type="success"
                    icon="el-icon-check"
                  ></el-button>
                  <el-button
                    circle
                    style="cursor: pointer"
                    type="danger"
                    icon="el-icon-close"
                    @click="cancelEdit(scope.$index)"
                  />
                </div>
                <div v-else>
                  <el-button
                    circle
                    style="cursor: pointer"
                    @click="editItem(scope.row, scope.$index)"
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
    </template>
  </restricted-view>
</template>

<script>
import ProviderService from "@/services/lunch_management/provider";
import {
  required,
  minLength,
  maxLength,
  minValue,
} from "vuelidate/lib/validators";
import RestrictedView from "@/components/RestrictedView";

export default {
  middleware: "authentication",
  components: {
    RestrictedView,
  },
  validations: {
    createdItem: {
      name: { required },
      phone: {
        required,
        minLength: minLength(10),
        maxLength: maxLength(10),
      },
      address: { required },
      budget: {
        required,
        minValue: minValue(1000),
      },
      link: { required },
    },
  },
  data: () => ({
    json_fields: {
      Name: "name",
      Phone: "phone",
      Budget: "budget",
      Address: "address",
      Link: "link",
      Veggie: "has_vegetarian",
    },
    search: "",
    desserts: [],
    editedIndex: -1,
    createdItem: {
      name: "",
      phone: "",
      budget: "",
      address: "",
      link: "",
    },
    tempItem: {
      name: "",
      phone: "",
      budget: "",
      address: "",
      link: "",
    },
    editedItem: {
      name: "",
      phone: "",
      budget: "",
      address: "",
      link: "",
    },
    isAdding: false,
  }),

  created: async function () {
    await this.getProviders();
  },

  methods: {
    fetchDataForExportExcel() {
      return this.desserts;
    },
    async getProviders() {
      const providers = await ProviderService.get();
      this.desserts = providers.data;
    },

    addNewItem() {
      this.cancelAllEditMode();
      this.desserts.unshift(this.createdItem);
      this.$set(this.createdItem, "editMode", true);
      this.isAdding = true;
    },

    cancelCreate() {
      this.createdItem = {};
      this.$set(this.createdItem, "editMode", false);
      this.desserts.splice(0, 1);
      this.isAdding = false;
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
        (await ProviderService.delete(item.id))
      ) {
        this.$toast.success("Deleted Successfully");
      } else {
        this.$toast.error("Delete Failed");
      }
    },

    async createNewItem(item) {
      try {
        const res = await ProviderService.create(item);
        this.desserts.splice(0, 1);
        this.desserts.unshift(res.data);
        this.createdItem = {};
        this.isAdding = false;
        this.$set(this.createdItem, "editMode", false);
        this.$toast.success("Created Successfully!");
        await this.getProviders();
      } catch (e) {
        this.$toast.error("Create Failed");
      }
    },

    async saveEdit(item, _index) {
      if (!this.validateData(item)) {
        return;
      }
      if (this.isAdding) {
        await this.createNewItem(item);
        return;
      }
      this.editedItem = Object.assign({}, item);
      Object.assign(this.desserts[this.editedIndex], this.editedItem);
      const provider = await ProviderService.update({
        id: this.editedItem.id,
        data: this.editedItem,
      });
      if (provider && provider.data.msg) {
        const content = provider.data.msg;
        this.$toast.error(content);
      }
      if (provider && provider.data.name) {
        const content = "Updated Successfully!";
        this.$toast.success(content);
      }
      this.$set(item, "editMode", false);
      await this.getProviders();
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

    validateData(item) {
      let error;
      if (
        !item.name.trim() ||
        !item.phone ||
        !item.budget ||
        !item.address.trim() ||
        !item.link.trim()
      ) {
        error = "Missing Data";
      } else if (
        !/[(84)0][35789]([0-9]{8})$/.test(item.phone) &&
        !/[(84)0]2([0-9]{9})$/.test(item.phone)
      ) {
        error = "Phone number is incorrect";
      } else if (item.budget < 0) {
        error = "Budget is incorrect";
      }
      if (error) {
        this.$toast.error(error);
      }
      return !error;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
