<template>
  <div>
    <el-form
      ref="form"
      :model="form"
      label-width="120px"
      @submit.native.prevent="onSubmit('form')"
    >
      <el-form-item prop="title" :rules="rules" label="Title">
        <el-input v-model="form.title"></el-input>
      </el-form-item>

      <el-form-item label="Description">
        <el-input type="textarea" v-model="form.description"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" :disabled="isDisable" native-type="submit"
          >Update</el-button
        >
        <el-button @click="handleClose">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { mapActions } from "vuex";

export default {
  name: "UpdateTopicModal",
  data() {
    return {
      isDisable: false,
      rules: [
        {
          required: true,
          message: "Topic's title cannot empty",
          trigger: "blur",
        },
      ],
    };
  },
  props: {
    dialogUpdateTopic: Boolean,
    form: Object,
  },
  methods: {
    ...mapActions("elearning", ["updateTopic"]),
    async onSubmit(formName) {
      await this.$refs[formName].validate(async (valid, obj) => {
        if (valid) {
          this.isDisable = true;
          let topic = await this.updateTopic(this.form);
          if (topic) {
            this.$emit("update:dialogUpdateTopic", false);
          }
          this.isDisable = false;
        }
      });
    },
    handleClose() {
      this.$confirm("Are you sure to stop updating topic?")
        .then((_) => {
          this.$emit("update:dialogUpdateTopic", false);
        })
        .catch((_) => {});
    },
  },
};
</script>
