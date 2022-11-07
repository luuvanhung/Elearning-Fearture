<template>
  <el-form :model="contactCols" :rules="rules" ref="refContactForm">
    <el-form-item
      class="contact-form-item d-flex flex-column align-item-center flex-sm-row"
      label="The column of employee's Team:"
      prop="team"
    >
      <el-select v-model="contactCols.team" :placeholder="placeholder">
        <el-option
          v-for="(col, index) in cols"
          :key="index"
          :label="col"
          :value="index"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      class="contact-form-item d-flex flex-column align-item-center flex-sm-row"
      label="The column of employee's Name:"
      prop="name"
    >
      <el-select v-model="contactCols.name" :placeholder="placeholder">
        <el-option
          v-for="(col, index) in cols"
          :key="index"
          :label="col"
          :value="index"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      class="contact-form-item d-flex flex-column align-item-center flex-sm-row"
      label="The column of employee's Role:"
      prop="role"
    >
      <el-select v-model="contactCols.role" :placeholder="placeholder">
        <el-option
          v-for="(col, index) in cols"
          :key="index"
          :label="col"
          :value="index"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      class="contact-form-item d-flex flex-column align-item-center flex-sm-row"
      label="The column of employee's Email:"
      prop="email"
    >
      <el-select v-model="contactCols.email" :placeholder="placeholder">
        <el-option
          v-for="(col, index) in cols"
          :key="index"
          :label="col"
          :value="index"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      class="contact-form-item d-flex flex-column align-item-center flex-sm-row"
      label="The column of employee's Phone:"
      prop="phone"
    >
      <el-select v-model="contactCols.phone" :placeholder="placeholder">
        <el-option
          v-for="(col, index) in cols"
          :key="index"
          :label="col"
          :value="index"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      class="contact-form-item d-flex flex-column align-item-center flex-sm-row"
      label="The column of employee's On Boarding:"
      prop="onBoarding"
    >
      <el-select v-model="contactCols.onBoarding" :placeholder="placeholder">
        <el-option
          v-for="(col, index) in cols"
          :key="index"
          :label="col"
          :value="index"
        ></el-option>
      </el-select>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  props: ["cols", "defaultValue"],
  data() {
    return {
      contactCols: this.defaultValue,
      placeholder: "Can not be detected",
    };
  },
  computed: {
    rules() {
      return Object.keys(this.contactCols).reduce(
        (rules, key) => (
          (rules[key] = {
            validator: this.validate,
            trigger: "change",
            message: "Please select column",
          }),
          rules
        ),
        {}
      );
    },
  },
  methods: {
    validate(_rule, value, callback) {
      if (value === null && !Number.isInteger(value)) {
        callback(new Error());
      } else {
        callback();
      }
    },
  },
  watch: {
    contactCols: {
      deep: true,
      handler: function () {
        this.$emit("input", this.contactCols);
      },
    },
  },
};
</script>

<style lang="scss">
.contact-form-item {
  & > .el-form-item__content {
    @media (min-width: 576px) {
      margin-left: auto;
    }
  }
  & > .el-form-item__label {
    font-weight: 500;
    color: #000000;
    text-align: start;
  }
}
</style>
