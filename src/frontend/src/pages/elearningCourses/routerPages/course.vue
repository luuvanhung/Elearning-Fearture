<template>
  <div>
    <router-view class="mt-3" :courseId="id"></router-view>
  </div>
</template>

<script>
export default {
  props: ["id"],
};
</script>

<style></style>
