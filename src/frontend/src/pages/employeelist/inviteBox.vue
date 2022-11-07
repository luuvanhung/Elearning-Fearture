<template>
  <div class="mt-5 col-6 mx-auto">
    <div class="card-header bg-info">
      <h2 class="text-white text-center">Welcome to Company App Management</h2>
    </div>
    <div
      v-show="admin === 'true'"
      class="d-flex justify-content-center card-body bg-light my-auto py-5"
    >
      <router-link
        to="/invite"
        class="btn btn-info float-right px-4 py-2 mr-4 text-uppercase font-weight-bold"
      >
        <font-awesome-icon :icon="['fas', 'user-plus']" />
        INVITE
      </router-link>
      <router-link
        to="/import"
        class="btn btn-info float-right px-4 py-2 mr-4 text-uppercase font-weight-bold"
      >
        <font-awesome-icon :icon="['fas', 'file-import']" />
        IMPORT FILE
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "InviteBox",
  data() {
    return {
      admin: localStorage.getItem("is_admin"),
    };
  },
};
</script>

<style scoped></style>
