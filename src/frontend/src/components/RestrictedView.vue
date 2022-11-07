<template>
  <span>
    <slot v-if="this.scope && permitIfAllScope()"></slot>
    <slot v-if="this.scopes && permitIfOneOfAllScope()"></slot>
  </span>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "RestrictedView",
  props: {
    scope: Array,
    scopes: Array,
  },
  computed: {
    ...mapGetters({
      tokenInfo: "scope/tokenInfo",
    }),
  },
  methods: {
    permitIfAllScope() {
      return !this.scope.some((n) => {
        return this.tokenInfo["scope"].indexOf(n) === -1;
      });
    },
    permitIfOneOfAllScope() {
      return this.scopes.some((n) => {
        return this.tokenInfo["scope"].indexOf(n) !== -1;
      });
    },
  },
};
</script>

<style scoped></style>
