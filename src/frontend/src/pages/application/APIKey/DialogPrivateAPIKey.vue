<template>
  <div style="margin-top: 15px">
    <el-input
      placeholder="Please input"
      v-model="privateAPIKey"
      class="input-with-select"
      :readonly="true"
    >
      <el-button type="primary" slot="append" @click="handleCopyToClipboard"
        >Copy</el-button
      >
    </el-input>
  </div>
</template>

<script>
export default {
  props: {
    privateAPIKey: { type: String, default: "" },
  },
  methods: {
    handleCopyToClipboard() {
      this.writeToClipboard(this.privateAPIKey);
      this.$toast.success("Copied Successfully");
    },
    writeToClipboard(str) {
      navigator.clipboard.writeText(str);
    },
  },
};
</script>
