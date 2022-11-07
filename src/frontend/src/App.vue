<template>
  <router-view></router-view>
</template>

<script>
export default {
  head() {
    return {
      title: "Homepage",
    };
  },
};
</script>
<style>
@import "./assets/css/bootstrap-grid.css";
body {
  overscroll-behavior-x: none !important;
}
</style>
