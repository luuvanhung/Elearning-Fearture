<template>
  <div>
    <probation-form />
    <go-top
      :size="30"
      :right="50"
      :bottom="50"
      fg-color="#109fa5"
      bg-color="#dce2e321"
      :radius="3"
      weight="bold"
      ripple-bg="rgba(0, 0, 0, .3)"
      :max-width="0"
      :tabindex="-1"
    >
      TOP
    </go-top>
  </div>
</template>
<script>
import GoTop from "@inotom/vue-go-top";
import ProbationForm from "./probationForm";

export default {
  name: "ProbationDetail",
  middleware: "authentication",
  components: {
    GoTop,
    ProbationForm,
  },
};
</script>
