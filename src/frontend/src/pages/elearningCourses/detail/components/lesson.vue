<template>
  <div>
    <div class="title-bar mt-3">
      <h3 class="p-3 text-white text-capitalize">
        {{ chapters.title }}
      </h3>
      <el-badge
        :value="chapters.attachments.length"
        class="item"
        type="warning"
      >
        <el-popover placement="bottom" trigger="click">
          <div v-if="chapters.attachments.length">
            <el-tooltip
              class="item"
              v-for="attachment in chapters.attachments"
              :key="attachment.id"
              effect="light"
              :content="
                attachment.forced_read
                  ? attachment_tooltips.FORCED_READ_ATTACHMENT
                  : attachment_tooltips.COMMON_ATTACHMENT
              "
              placement="left"
            >
              <el-tag class="d-flex p-2 mt-2 mb-2" style="margin-right: 0">
                <a
                  :href="!attachment.forced_read && attachment.file"
                  :style="{
                    opacity: +!attachment.forced_read,
                  }"
                  :download="!attachment.forced_read"
                >
                  <img
                    class="btn-download mr-2"
                    :src="require('@/static/images/download-svgrepo-com.svg')"
                  />
                </a>
                <a
                  :href="attachment.file"
                  target="_blank"
                  class="d-flex align-items-center"
                >
                  <img
                    class="btn-video mr-2"
                    :src="
                      require(`@/static/images/${
                        mimetype_icons[getMimeType(attachment.mine_type)]
                      }`)
                    "
                  />
                  <p>{{ attachment.original_name }}</p>
                </a>
              </el-tag>
            </el-tooltip>
          </div>
          <div v-else>
            <p>This lesson contains no Attachment</p>
          </div>
          <el-button slot="reference">Attachments</el-button>
        </el-popover>
      </el-badge>
    </div>
    <div class="mt-3 mb-3">
      <quill-editor
        class="view-form"
        :disabled="true"
        :options="VIEW_OPTIONS"
        v-model="chapters.content"
      />
    </div>
  </div>
</template>

<script>
import { MIMETYPES, MIMETYPE_ICONS } from "@/const/MimeTypes";
import { TOOLTIPS } from "@/const/AssignmentDetail";
import { VIEW_OPTIONS } from "@/const/quillEditorModules.js";

export default {
  props: ["chapters"],
  data() {
    return {
      VIEW_OPTIONS: VIEW_OPTIONS,
      currentLesson: {},
    };
  },
  computed: {
    mimetype_icons() {
      return MIMETYPE_ICONS;
    },
    attachment_tooltips() {
      return TOOLTIPS;
    },
  },
  methods: {
    getMimeType(originalType) {
      for (const type in MIMETYPES) {
        if (MIMETYPES[type].includes(originalType)) return type;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.item {
  margin-right: 30px;
}
.title-bar {
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  background-color: #25c9d0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.el-tag {
  height: 100%;
}
.btn-download {
  width: 25px;
  filter: invert(65%) sepia(66%) saturate(518%) hue-rotate(90deg)
    brightness(88%) contrast(95%);
}

.btn-file {
  width: 25px;
}
.style-video {
  margin: 10px;
}
.cam_video {
  width: 100%;
  height: 100%;
}
.btn-video {
  width: 30px;
}
.btn-download {
  width: 25px;
  filter: invert(65%) sepia(66%) saturate(518%) hue-rotate(90deg)
    brightness(88%) contrast(95%);
}
@import "@/assets/scss/main.scss";
</style>
