<template>
  <div v-if="newTitles.length > 0">
    <p style="font-size: 24px">Titles will be added to the system</p>
    <ul style="margin: 10px 20px">
      <template v-for="item in newTitles">
        <li class="divider" :key="item">{{ item }}</li>
      </template>
    </ul>
  </div>
  <div v-else class="no-data">
    <p>No new titles</p>
  </div>
</template>

<script>
export default {
  name: "ConfirmAddNewTitle",
  props: ["defaultValue"],
  data() {
    return {
      newTitles: this.defaultValue,
    };
  },
  watch: {
    newTitles() {
      this.$emit("input", this.newTitles);
    },
  },
};
</script>
