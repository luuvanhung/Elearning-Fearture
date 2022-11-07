<template>
  <div>
    <el-descriptions :column="1">
      <template #extra>
        <el-tooltip
          effect="light"
          content="Save course before add chapter"
          placement="bottom"
        >
          <div>
            <el-button
              :disabled="true"
              type="primary"
              icon="el-icon-circle-plus"
              size="medium"
            >
              Add chapter
            </el-button>
          </div>
        </el-tooltip>
      </template>
      <el-descriptions-item label="Total chapters: ">
        {{ totalChapters }}
      </el-descriptions-item>
    </el-descriptions>
  </div>
</template>

<script>
export default {
  props: {
    initialChapters: Array,
    course_id: String,
    currentLesson: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
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
      courseProps: {
        children: "lessons",
        label: "title",
      },
    };
  },
  computed: {
    totalChapters() {
      return this.chapters.length;
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
