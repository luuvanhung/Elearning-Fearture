<template>
  <div>
    <el-row>
      <el-col :span="11" class="m-2">
        <el-descriptions :column="1">
          <el-descriptions-item label="Total chapters: ">{{
            totalChapter
          }}</el-descriptions-item>
        </el-descriptions>
      </el-col>
    </el-row>
    <el-tree
      :data="course"
      :props="courseProps"
      node-key="id"
      accordion
      :expand-on-click-node="false"
    >
      <span class="custom-tree-node" slot-scope="{ node, data }">
        <template v-if="data.isRoot" style="background-color: red">
          <span>
            <span class="text">{{ data.title }}</span>
          </span>
        </template>
        <template v-else>
          <span class="text">
            <i
              :class="
                data.type === 'VIDEO'
                  ? 'el-icon-video-camera'
                  : 'el-icon-document'
              "
            ></i>
            {{ data.title }}
          </span>
          <span>
            <el-tooltip
              effect="light"
              content="Lesson's detail"
              placement="bottom"
            >
              <el-button
                style="font-size: 20px"
                type="text"
                icon="el-icon-info"
                @click="infoLesson(node, data)"
              ></el-button>
            </el-tooltip>
          </span>
        </template>
      </span>
    </el-tree>
  </div>
</template>

<script>
export default {
  props: {
    chapters: {
      default: () => [],
      type: Array,
    },
    courseId: String,
  },
  data() {
    return {
      filesList: [],
      course: [],
      courseProps: {
        children: "lessons",
        label: "title",
      },
    };
  },
  computed: {
    totalChapter() {
      return this.chapters.length;
    },
  },
  methods: {
    infoLesson(node) {
      this.$emit("detailLessons", node.data);
    },
  },
  created() {
    this.chapters.forEach((element) => {
      this.course.push({ ...element, editable: null, isRoot: true });
    });
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
.cam_video {
  width: 100%;
  height: 100%;
}
.quill-editor {
  :deep(iframe) {
    pointer-events: none;
  }
}
</style>
