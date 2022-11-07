<template>
  <div class="dialog-create-api-key">
    <el-form-item label="API Key" class="api-key-form-item">
      <!-- TABLE API KEY -->
      <el-table
        v-if="listAPIKey !== null"
        class="api-table"
        style="width: 100%"
        border
        stripe
        highlight-current-row
        :data="listAPIKey"
      >
        <el-table-column
          label="Prefix"
          prop="prefix"
          align="center"
          width="133"
        ></el-table-column>
        <el-table-column
          label="Name"
          prop="name"
          align="center"
          sortable
        ></el-table-column>
        <!-- BUTTON DELETE API KEY -->
        <el-table-column align="center" label="Action" width="88">
          <template slot-scope="scope">
            <el-popconfirm
              confirm-button-text="OK"
              cancel-button-text="No, Thanks"
              icon="el-icon-info"
              icon-color="red"
              title="Are you sure to delete this?"
              @confirm="handleClickDeleteAPIKey(scope.row)"
            >
              <el-button slot="reference" class="bt-delete-api-key">
                <img :src="require('@/static/images/IconDelete.svg')" />
              </el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <!-- BUTTON CREATE API KEY -->
      <div class="bt-create-api-key">
        <el-button type="primary" @click="handleClickNewAPIKey">
          Create New API Key
        </el-button>
      </div>

      <!-- DIALOG CREATE API KEY -->
      <el-dialog
        width="30%"
        title="Create API Key"
        :visible.sync="dialogCreateAPIKey"
        append-to-body
      >
        <el-form
          class="form-create-api-key"
          ref="formCreateAPI"
          :inline="true"
          :model="formCreateAPI"
          :rules="rulesFormCreateAPIKey"
          @submit.native.prevent="handleSubmitNewAPIKey"
        >
          <el-form-item label="Name:" class="name-input" prop="name">
            <el-input
              placeholder="Enter API key name"
              v-model="formCreateAPI.name"
              ref="nameNewAPI"
            ></el-input>
          </el-form-item>
          <el-form-item label="Scopes">
            <ScopesSelector
              ref="apiKeySelectScopes"
              :scopes="scopes"
              :selectedScopes="formCreateAPI.scopes"
              @handleUpdateScopes="handleUpdateScopes"
            />
          </el-form-item>
          <el-form-item class="bt-create">
            <el-button native-type="submit" type="primary">Create</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>

      <!-- DIALOG CREATE SUCCESS API KEY -->
      <el-dialog
        width="30%"
        class="dialog-no-header"
        :visible.sync="dialogCreateSuccessAPIKey"
        :close-on-click-modal="false"
        :close-on-press-escape="false"
        append-to-body
      >
        <center>
          <p>This is the API Key, it's secret, save it somewhere safe:</p>
          <p>(Note: that this key is only issued once)</p>
          <DialogPrivateAPIKey :privateAPIKey="privateAPIKey" />
        </center>
      </el-dialog>
    </el-form-item>
  </div>
</template>

<script>
import APIKeyService from "../../../services/application/apiKey.service";
import ScopesSelector from "../ScopesSelector.vue";
import DialogPrivateAPIKey from "./DialogPrivateAPIKey.vue";

export default {
  components: {
    DialogPrivateAPIKey,
    ScopesSelector,
  },
  props: {
    allScopeConst: { type: Array, default: () => [] },
    currApp: { type: Object, default: () => {} },
  },
  watch: {
    currApp: {
      async handler(newApp) {
        this.currApp = newApp;
        this.formCreateAPI.scopes = newApp.scope;
        await this.getListAPIKey();
      },
      deep: true,
    },
  },
  data() {
    return {
      listAPIKey: [
        {
          prefix: "",
          name: "",
          application_id: -1,
        },
      ],
      formCreateAPI: {
        name: "",
        scopes: [],
      },
      privateAPIKey: "",
      rulesFormCreateAPIKey: {
        name: [
          { required: true, message: "Please input name", trigger: "blur" },
        ],
      },
      dialogCreateAPIKey: false,
      dialogCreateSuccessAPIKey: false,
    };
  },
  async mounted() {
    await this.getListAPIKey();
  },
  methods: {
    async handleClickDeleteAPIKey({ prefix }) {
      const success = await APIKeyService.deleteAPIKeyByPrefix(prefix);
      if (success) {
        this.getListAPIKey();
        this.$toast.success("Delete Successfully");
      } else {
        this.$toast.error("Delete Failed");
      }
    },
    handleClickNewAPIKey() {
      this.showDialogCreateAPIKey();
      this.focusNameNewAPI();
      this.clearFormNewAPI();
      this.resetValidateNewAPIKey();
      this.resetApiKeySelectScopes();
    },
    handleSubmitNewAPIKey() {
      this.$refs["formCreateAPI"].validate(async (valid) => {
        if (!valid) return false;

        const data = {
          name: this.formCreateAPI.name,
          application_id: this.currApp.id,
          scope: this.strApiKeyScopes,
        };
        const success = await APIKeyService.createAPIKey(data);
        if (success) {
          this.$toast.success("Created Successfully");
          this.privateAPIKey = success;
          this.hideDialogCreateAPIKey();
          this.dialogCreateSuccessAPIKey = true;
          this.getListAPIKey();
        }
      });
    },
    async getListAPIKey() {
      const res = await APIKeyService.getListAPIKey();
      const id = this.currApp.id;
      this.listAPIKey = filterAPIKeyByAppId(res);

      function filterAPIKeyByAppId(listAPIKey) {
        if (listAPIKey) {
          const list = listAPIKey.filter((e) => e.application_id == id);
          return list && list.length > 0 ? list : null;
        }

        return null;
      }
    },
    focusNameNewAPI() {
      this.$nextTick(() => this.$refs.nameNewAPI.focus());
    },
    clearFormNewAPI() {
      this.formCreateAPI.name = "";
    },
    resetValidateNewAPIKey() {
      try {
        this.getComponent("formCreateAPI").resetFields();
      } catch {
        return;
      }
    },
    handleUpdateScopes(scopes) {
      this.formCreateAPI.scopes = scopes;
    },
    resetApiKeySelectScopes() {
      try {
        let selectScopes = this.getComponent("apiKeySelectScopes");
        selectScopes.resetCollapse();
        selectScopes.reset_all = false;
        selectScopes.select_all = false;
      } catch {
        return;
      }
    },
    getComponent(name) {
      return this.$refs[name];
    },
    showDialogCreateAPIKey() {
      this.dialogCreateAPIKey = true;
    },
    hideDialogCreateAPIKey() {
      this.dialogCreateAPIKey = false;
    },
  },
  computed: {
    scopes() {
      return this.allScopeConst
        .map((scope) => ({
          ...scope,
          children: scope.children.filter(
            (children) =>
              !!this.currApp.scope.find((scope) => scope === children.scope)
          ),
        }))
        .filter((parent) => parent.children.length > 0);
    },
    strApiKeyScopes() {
      return this.formCreateAPI.scopes.join(" ");
    },
  },
};
</script>

<style lang="scss">
@import "./style.scss";
</style>
