<template>
  <div>
    <div @click="onClick" id="pptx-container"></div>
  </div>
</template>

<script>
export default {
  props: {
    attachment: Object,
    assignment_chapter_lesson_attachment: Object,
  },
  data() {
    return {
      page: "0",
      numPages: "1",
      container: null,
      auto: null,
    };
  },
  mounted() {
    this.onLoadPpt();
  },
  watch: {
    page() {
      if (
        parseInt(this.page) > 0 &&
        this.assignment_chapter_lesson_attachment
      ) {
        let trackingData = {
          current_page: parseInt(this.page),
        };
        if (
          this.page == this.numPages &&
          !this.assignment_chapter_lesson_attachment.read
        ) {
          trackingData = {
            ...trackingData,
            read: true,
          };
        }
        this.$emit("onProgressChange", trackingData);
      }
    },
  },
  methods: {
    onClick() {
      this.page = $("#slides-slide-num")[0].innerText;
      this.numPages = $("#slides-total-slides-num")[0].innerText;
    },
    onLoadPpt() {
      this.container = $("#pptx-container");
      this.auto = $("#slides-play-pause");
      $("#pptx-container").officeToHtml({
        url: this.attachment.file,
        pptxSetting: {
          slidesScale: "150%",
          mediaProcess: true,
          slideModeConfig: {
            first: 1,
            nav: true,
            navTxtColor: "black",
            keyBoardShortCut: false,
            showSlideNum: true,
            showTotalSlideNum: true,
            loop: true,
            background: false,
            transition: "default",
            transitionTime: 0.5,
          },
        },
      });
    },
  },
};
</script>

<style>
#pptx-container {
  margin-left: auto;
  margin-right: auto;
  width: 960px;
  height: 540px;
}
</style>
