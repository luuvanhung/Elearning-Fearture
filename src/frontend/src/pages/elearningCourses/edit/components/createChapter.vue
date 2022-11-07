<template>
  <div>
    <TitleBar title="Create new chapter" />
    <el-card style="color: black">
      <el-form
        ref="formChapter"
        label-position="top"
        label-width="auto"
        size="large"
        :model="chapter"
        :rules="formRules"
        v-loading="chapterLoading"
        @submit.native.prevent="saveChapter(chapter)"
      >
        <el-form-item label="Chapter" prop="title">
          <el-input placeholder="Chapter's title" v-model="chapter.title" />
        </el-form-item>
        <el-form-item label="Prerequisite chapter">
          <el-tooltip
            effect="dark"
            :content="TOOLTIPS.prerequisite_chapter"
            placement="top"
          >
            <el-select
              filterable
              clearable
              remote
              reserve-keyword
              v-model="chapter.previous_chapter"
              value-key="title"
              style="width: 100%"
            >
              <el-option
                v-for="chap in availablePreviousChapters(chapter)"
                :key="chap.id"
                :label="chap.title"
                :value="chap"
              ></el-option>
            </el-select>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="Description" prop="description">
          <el-input type="textarea" :rows="3" v-model="chapter.description" />
        </el-form-item>
        <el-form-item>
          <div style="display: flex; flex-flow: row">
            <el-tooltip
              :disabled="changed"
              effect="light"
              content="Can only click when data change"
              placement="bottom"
              style="margin-right: 10px"
            >
              <div>
                <el-button
                  type="primary"
                  native-type="submit"
                  :disabled="!changed"
                  >Save</el-button
                >
              </div>
            </el-tooltip>
            <el-button @click="$emit('viewEditCourse')">Cancel</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import TitleBar from "@/components/TitleBar.vue";
import ChapterService from "@/services/e-learning/chapter";
const TOOLTIPS = {
  prerequisite_chapter:
    "Select chapter that must be accomplished before approach current chapter",
};
var hash = require("object-hash");

export default {
  props: {
    chapters: Array,
  },
  components: {
    TitleBar,
  },
  data() {
    return {
      TOOLTIPS: TOOLTIPS,
      course_id: null,
      formRules: {
        title: [
          {
            required: true,
            message: "Please input title",
            trigger: "blur",
          },
        ],
      },
      chapter: {
        course_id: this.course_id,
        title: null,
        description: null,
      },
      chapterLoading: false,
      last_hash: null,
      changed: false,
    };
  },
  watch: {
    chapter: {
      deep: true,
      handler(newValue, oldValue) {
        const newHash = hash(newValue);
        if (oldValue && newHash != this.last_hash) {
          this.changed = true;
        }
        this.last_hash = newHash;
      },
    },
  },
  created() {
    this.course_id = this.$route.params.id;
  },
  methods: {
    availablePreviousChapters(currentChapter) {
      let listChapter = [];
      for (const element of this.chapters) {
        if (element.id === currentChapter.id) break;
        listChapter.push({ id: element.id, title: element.title });
      }
      return listChapter;
    },
    async saveChapter(data) {
      this.$refs.formChapter.validate(async (valid, obj) => {
        if (valid) {
          this.chapterLoading = true;
          const response = await ChapterService.create({
            course_id: this.course_id,
            title: data.title,
            description: data.description,
            previous_chapter_id: data.previous_chapter
              ? data.previous_chapter.id
              : null,
          });
          if (response.data) {
            this.last_hash = hash(this.chapter);
            this.changed = false;
            this.$emit("viewEditChapter", response.data);
          }
          this.chapterLoading = false;
        }
      });
    },
    async cancel() {
      this.$emit("viewEditCourse");
    },
  },
};
</script>

<style lang="scss" scoped></style>
