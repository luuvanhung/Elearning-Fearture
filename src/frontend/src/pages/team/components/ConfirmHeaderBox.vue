<template>
  <div>
    <div class="d-flex form-item">
      The header is locate at row
      <el-select v-model="value">
        <el-option
          v-for="item in options"
          :key="item"
          :label="item + 1"
          :value="item"
        >
        </el-option>
      </el-select>
    </div>
    <div class="cols">
      <div v-for="(col, index) in header" :key="index">
        {{ col }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["headers"],

  data() {
    return {
      value: "",
    };
  },
  computed: {
    header() {
      return this.headers[this.value];
    },
    options() {
      return this.headers
        .map((row, index) => index)
        .filter(
          (option) => this.headers[option].filter((item) => !!item).length > 1
        );
    },
  },
  watch: {
    value() {
      this.$emit("input", this.value);
    },
  },
  created() {
    this.value = this.options[0];
  },
};
</script>

<style lang="scss" scoped>
.form-item {
  white-space: nowrap;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}
.cols {
  padding-bottom: 10px;
  display: flex;
  overflow-y: auto;
  &::-webkit-scrollbar {
    height: 10px;
  }

  /* Track */
  &::-webkit-scrollbar-track {
    background: white;
    border-radius: 50rem;
    outline: 1px solid #cbcddc;
  }

  /* Handle */
  &::-webkit-scrollbar-thumb {
    border: 2px solid white;
    background: #cbcddc;
    border-radius: 50rem;
  }
  & > div {
    padding: 0.5rem 1rem;
    white-space: nowrap;
    border: 2px solid #cbcddc;
    border-right: none;
    &:last-child {
      border-right: 2px solid #cbcddc;
    }
  }
}
</style>
