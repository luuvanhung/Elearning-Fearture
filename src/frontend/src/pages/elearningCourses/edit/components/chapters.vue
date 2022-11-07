<template>
  <div>
    <el-descriptions :column="1">
      <template #extra>
        <el-button
          type="primary"
          icon="el-icon-circle-plus"
          @click="createChapter"
          size="medium"
          >Add chapter</el-button
        >
      </template>
      <el-descriptions-item label="Total chapters: ">
        {{ totalChapters }}
      </el-descriptions-item>
    </el-descriptions>
    <el-tree
      ref="treeChapter"
      node-key="id"
      :data="chapters"
      :props="courseProps"
      :default-expanded-keys="defaultExpandedKey"
      accordion
      :expand-on-click-node="false"
      @node-click="clickNode"
    >
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <template v-if="data.isRoot" style="background-color: red">
          <span class="text">{{ data.title }}</span>
          <span>
            <el-tooltip
              effect="light"
              :content="
                lessonViewCreate
                  ? TOOLTIPS.block_add_lesson
                  : TOOLTIPS.add_lesson
              "
              placement="top"
            >
              <span>
                <el-button
                  class="icon-btn"
                  icon="el-icon-circle-plus"
                  type="text"
                  size="medium"
                  :disabled="lessonViewCreate"
                  @click="createLesson(data)"
                ></el-button>
              </span>
            </el-tooltip>
            <el-tooltip
              effect="light"
              :content="TOOLTIPS.edit_chapter"
              placement="top"
            >
              <el-button
                class="icon-btn"
                type="text"
                icon="el-icon-edit"
                @click="editChapter(data)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              effect="light"
              :content="TOOLTIPS.delete_chapter"
              placement="top"
            >
              <el-popconfirm
                confirm-button-text="Delete"
                cancel-button-text="No"
                :title="`Remove Chapter ${data.title}?`"
                @confirm="removeChapter(node, data)"
              >
                <template slot="reference">
                  <el-button
                    class="icon-btn"
                    type="text"
                    icon="el-icon-delete"
                  />
                </template>
              </el-popconfirm>
            </el-tooltip>
          </span>
        </template>
        <template v-else>
          <span class="text">
            <i class="el-icon-document"></i>
            {{ data.title }}
          </span>
          <span>
            <el-tooltip
              effect="light"
              :content="TOOLTIPS.edit_lesson"
              placement="top"
            >
              <el-button
                class="icon-btn"
                type="text"
                icon="el-icon-edit"
                @click="editLesson(node, data)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              effect="light"
              :content="TOOLTIPS.delete_lesson"
              placement="top"
            >
              <el-popconfirm
                confirm-button-text="Delete"
                cancel-button-text="No"
                title="Remove this lesson?"
                @confirm="removeLesson(node, data)"
              >
                <template slot="reference">
                  <el-button
                    class="icon-btn"
                    type="text"
                    icon="el-icon-delete"
                  />
                </template>
              </el-popconfirm>
            </el-tooltip>
          </span>
        </template>
      </span>
    </el-tree>
  </div>
</template>

<script>
import { convertDuration } from "@/utils/convertDuration";
import ChapterService from "@/services/e-learning/chapter";
import LessonService from "@/services/e-learning/lesson";
const TOOLTIPS = {
  block_add_lesson: "Save or Cancel current lesson before add new one",
  add_lesson: "Add new lesson",
  edit_chapter: "Edit this chapter",
  delete_chapter: "Delete this chapter",
  edit_lesson: "Edit this lesson",
  delete_lesson: "Delete this lesson",
};
export default {
  props: {
    initialChapters: Array,
    course_id: String,
    lessonViewCreate: Boolean,
    currentLesson: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      TOOLTIPS: TOOLTIPS,
      formRules: {
        title: [
          {
            required: true,
            message: "Please input title",
            trigger: "blur",
          },
        ],
      },
      chapters: this.initialChapters.map((chapter) => ({
        isRoot: true,
        ...chapter,
      })),
      currentChapter: null,
      editingChapter: null,
      courseProps: {
        children: "lessons",
        label: "title",
      },
      selectedChapter: null,
      chapterLoading: false,
      lessonLoading: false,
    };
  },
  computed: {
    totalChapters() {
      return this.chapters.length;
    },
    defaultExpandedKey() {
      if (this.currentLesson)
        return this.currentLesson.chapter ? [this.currentLesson.chapter] : [];
      return this.currentChapter ? [this.currentChapter.id] : [];
    },
  },
  methods: {
    convertDuration,
    clickNode(node, nodeTree, tree) {
      if (!node.isRoot)
        this.$emit("viewEditLesson", {
          ...node,
          chapter: nodeTree.parent.data.id,
        });
    },
    allowDrop(draggingNode, dropNode, type) {
      if (type == "inner")
        return !draggingNode.data.isRoot && dropNode.data.isRoot ? true : false;
      else {
        return draggingNode.data.isRoot == dropNode.data.isRoot ? true : false;
      }
    },
    expandNode(node, nodeTree, tree) {
      this.$emit("setExpandedChapters", node.id, true);
    },
    collapseNode(node, nodeTree, tree) {
      this.$emit("setExpandedChapters", node.id, false);
    },
    dropNode(draggingNode, dropNode, dropType, ev) {
      if (draggingNode.data.isRoot) {
        for (let i = this.chapters.length - 1; i > 0; i--) {
          this.$set(this.chapters[i], "previous_chapter", {
            id: this.chapters[i - 1].id,
            title: this.chapters[i - 1].title,
          });
        }
        this.$emit("updateChapters", this.chapters);
      }
    },
    async createChapter() {
      this.$emit("viewCreateChapter");
    },
    async createLesson(chapter) {
      this.currentChapter = chapter;
      const response = await LessonService.create({
        course_id: this.course_id,
        chapter_id: chapter.id,
        title: "Untitled lesson",
      });
      if (response.data) {
        this.$emit("viewCreateLesson", chapter, response.data);
      } else this.$emit("viewEditCourse");
    },
    async removeChapter(node, data) {
      const parent = node.parent;
      const lessons = parent.data.lessons || parent.data;
      const index = lessons.findIndex((d) => d.id === data.id);
      if (data.id) {
        if (data.lessons.length > 0) {
          await this.$confirm(
            "This chapter contain lessons, do you want to delete?"
          );
        }
        await ChapterService.delete({
          id: data.id,
          course_id: this.course_id,
        });
        this.$emit("updateChapters", this.chapters);
        this.$emit("viewEditCourse");
      }
      lessons.splice(index, 1);
    },
    async removeLesson(node, data) {
      const parent = node.parent;
      const lessons = parent.data.lessons || parent.data;
      const index = lessons.findIndex((d) => d.id === data.id);
      lessons.splice(index, 1);
      if (this.currentLesson.id == data.id) this.$emit("viewEditCourse");
      const response = await LessonService.delete({
        course_id: this.course_id,
        chapter_id: node.parent.data.id,
        id: data.id,
      });
      if (response.status === 204) {
        this.$toast.success("Lesson deleted!");
      }
    },
    editChapter(data) {
      this.$emit("viewEditChapter", data);
    },
    editLesson(node, data) {
      this.$emit("viewEditLesson", { ...data, chapter: node.parent.data.id });
    },
  },
};
</script>

<style lang="scss" scoped>
.el-descriptions {
  margin-bottom: 20px !important;
  :deep(.el-descriptions__header) {
    display: inline;
  }
  :deep(.el-descriptions__extra) {
    float: right;
  }
  .el-button {
    padding: 10px 20px;
  }
}
.icon-btn {
  font-size: 20px;
}
.el-submenu {
  background-color: #25c9d0 !important;
  :deep(.el-submenu__title) {
    display: flex;
    color: white !important;
    &:hover {
      background-color: #25c9d0 !important;
    }
  }
}
i {
  color: #25c9d0 !important;
}
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 20px;
  padding-right: 8px;
  white-space: inherit;
}
</style>
