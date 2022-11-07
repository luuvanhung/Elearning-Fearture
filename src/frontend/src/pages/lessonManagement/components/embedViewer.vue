<template>
  <div>
    <videoViewer
      v-if="isVideo"
      :attachment="attachment"
      :assignment_chapter_lesson_attachment="
        assignment_chapter_lesson_attachment
      "
      :forced_read="attachment.forced_read"
      class="full-content"
      @onProgressChange="onProgressChange"
      :listTranscript="listTranscript"
    ></videoViewer>
    <wordViewer
      v-else-if="isWord"
      :attachment="attachment"
      :assignment_chapter_lesson_attachment="
        assignment_chapter_lesson_attachment
      "
      class="full-content"
      @onProgressChange="onProgressChange"
    ></wordViewer>
    <pdfViewer
      v-else-if="isPdf"
      :prefix="currentURLPrefix"
      :attachment="attachment"
      :assignment_chapter_lesson_attachment="
        assignment_chapter_lesson_attachment
      "
      class="full-content"
      @onProgressChange="onProgressChange"
    ></pdfViewer>
    <powerpointViewer
      v-else-if="isPowerpoint"
      :attachment="attachment"
      :assignment_chapter_lesson_attachment="
        assignment_chapter_lesson_attachment
      "
      class="full-content"
      @onProgressChange="onProgressChange"
    ></powerpointViewer>
    <unsupportViewer
      v-else
      :attachment="attachment"
      class="full-content"
    ></unsupportViewer>
  </div>
</template>
<script>
import LessonService from "@/services/e-learning/lesson";
import AssignmentService from "@/services/e-learning/assignment";
import EmbedAttachmentsService from "@/services/e-learning/embedAttachments";
import { MIMETYPES } from "@/const/MimeTypes";
import videoViewer from "./videoViewer.vue";
import wordViewer from "./wordViewer.vue";
import pdfViewer from "./pdfViewer.vue";
import powerpointViewer from "./powerpointViewer.vue";
import unsupportViewer from "./unsupportViewer.vue";
export default {
  components: {
    videoViewer,
    wordViewer,
    pdfViewer,
    powerpointViewer,
    unsupportViewer,
  },
  props: {
    idLesson: String,
  },
  data() {
    return {
      attachment: {
        id: null,
        file: null,
        mine_type: null,
        length: null,
        chapter: null,
        lesson: null,
        original_name: null,
        responser: null,
        transcript: null,
      },
      listTranscript: [],
      assignment_chapter_lesson_attachment: null,
      currentURLPrefix: document.URL.split(":")[0],

      value: "English",

      script: [],
    };
  },
  async mounted() {
    await this.fetchAttachment();
  },
  computed: {
    isVideo() {
      return MIMETYPES.videos.indexOf(this.attachment.mine_type) >= 0;
    },
    isWord() {
      return MIMETYPES.words.indexOf(this.attachment.mine_type) >= 0;
    },
    isPdf() {
      return MIMETYPES.pdfs.indexOf(this.attachment.mine_type) >= 0;
    },
    isPowerpoint() {
      return MIMETYPES.powerpoints.indexOf(this.attachment.mine_type) >= 0;
    },
  },
  methods: {
    // onVideoEnded() {
    //   },
    onProgressChange(trackingData) {
      AssignmentService.editAssignmentChapterLessonAttachment(
        this.$route.params.assignment_id,
        this.$route.params.assignment_chapter_id,
        this.$route.params.assignment_chapter_lesson_id,
        this.$route.params.assignment_chapter_lesson_attachment_id,
        trackingData
      );
    },
    async fetchAttachment() {
      await EmbedAttachmentsService.get(this.$route.params.id).then(
        (response) => {
          if (response && response.data) {
            this.attachment = response.data;
          }
        }
      );
      if (this.$route.params.assignment_chapter_lesson_attachment_id) {
        await AssignmentService.getAssignmentChapterLessonAttachment(
          this.$route.params.assignment_id,
          this.$route.params.assignment_chapter_id,
          this.$route.params.assignment_chapter_lesson_id,
          this.$route.params.assignment_chapter_lesson_attachment_id
        ).then((response) => {
          if (response) {
            this.assignment_chapter_lesson_attachment = response;
          }
        });
      }
      if (MIMETYPES.videos.indexOf(this.attachment.mine_type) >= 0)
        await this.fetchTranscript();
    },
    async fetchTranscript() {
      const response = await EmbedAttachmentsService.getTranscript(
        this.attachment.id
      );
      if (response && response.status == "200")
        this.listTranscript = response.data;
    },
  },
};
</script>
<style>
.title {
  display: inline-block;
  width: 30%;
  padding-left: 40px;
  font-weight: 700;
}
.transcript_nav {
  margin: 16px 0;
  padding-top: 10px;
  width: 1200px;
  border-top: 2px solid #d7d7d7;
}
.el-scrollbar__view {
  width: 1200px;
  height: 250px;
}
.row_table {
  height: 50px;
  margin: 14px;
  border-radius: 4px;
  background-color: #fff;
}
.el-table_1_column_1 {
  display: inline-block;
  padding-left: 20px;
}
.el-table_1_column_2 {
  display: inline-block;
  padding-left: 20px;
  width: 90%;
}
.full-content {
  width: 100%;
  height: 100%;
}
</style>
