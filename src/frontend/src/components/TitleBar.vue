<template>
  <div class="title-bar mt-3">
    <h2 v-if="title" class="p-3 text-white font-weight-bold text-capitalize">
      {{ title }}
    </h2>
    <h3 v-if="sub_title" class="p-3 text-white text-capitalize">
      {{ sub_title }}
    </h3>
  </div>
</template>
<script>
export default {
  name: "TitleBar",
  props: {
    title: String,
    sub_title: String,
  },
};
</script>
<style scoped>
.title-bar {
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  background-color: #25c9d0;
}
h2 {
  font-size: 20px;
}
h3 {
  font-size: 18px;
}
</style>
