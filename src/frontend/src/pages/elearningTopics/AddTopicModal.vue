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
          >Create</el-button
        >
        <el-button @click="handleClose">Cancel</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { mapActions } from "vuex";

export default {
  name: "AddTopicModal",
  data() {
    return {
      form: {
        title: "",
        description: "",
      },
      rules: [
        {
          required: true,
          message: "Topic's title cannot empty",
          trigger: "blur",
        },
      ],
      isDisable: false,
    };
  },
  props: {
    dialogAddTopic: Boolean,
  },
  methods: {
    ...mapActions("elearning", ["addTopic"]),
    async onSubmit(formName) {
      await this.$refs[formName].validate(async (valid, obj) => {
        if (valid) {
          this.isDisable = true;
          let topic = await this.addTopic(this.form);
          if (topic) {
            this.$emit("update:dialogAddTopic", false);
            this.resetForm();
          }
          this.isDisable = false;
        }
      });
    },
    handleClose() {
      this.$confirm("Are you sure to stop creating topic?")
        .then((_) => {
          this.resetForm();
          this.$emit("update:dialogAddTopic", false);
        })
        .catch((_) => {});
    },
    resetForm() {
      this.form = {
        title: "",
        description: "",
      };
    },
  },
};
</script>
