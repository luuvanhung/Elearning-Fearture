<template>
  <div>
    <div id="container"></div>
    <div class="page-number" v-if="current_page > 0">
      {{ current_page }}/{{ numberOfPages }}
    </div>
  </div>
</template>
<script>
import * as docx from "docx-preview";
import { MIMETYPES } from "@/const/MimeTypes";

export default {
  props: {
    attachment: Object,
    assignment_chapter_lesson_attachment: Object,
  },
  data() {
    return {
      total_page: 0,
      current_page: 0,
      pages_top_offsets: [],
    };
  },
  async created() {
    await this.readFile();
    window.addEventListener("scroll", this.onPageChange);
  },
  computed: {
    type() {
      if (MIMETYPES.words.indexOf(this.attachment.mine_type) >= 0)
        return "office";
      return "text";
    },
    numberOfPages() {
      return this.pages_top_offsets.length;
    },
  },
  watch: {
    current_page() {
      if (this.assignment_chapter_lesson_attachment && this.current_page > 0) {
        let trackingData = {
          current_page: this.current_page,
        };

        if (
          this.current_page == this.numberOfPages &&
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
    onPageChange() {
      for (let index = this.pages_top_offsets.length - 1; index >= 0; index--) {
        if (window.pageYOffset > this.pages_top_offsets[index]) {
          this.current_page = index + 1;
          break;
        } else {
          this.current_page = 0;
        }
      }
    },
    async readFile() {
      if (this.attachment) {
        const { file } = this.attachment;
        if (file) {
          await fetch(file)
            .then((r) => r.blob())
            .then((blob) => {
              if (blob) {
                docx
                  .renderAsync(
                    blob,
                    document.getElementById("container"),
                    null,
                    {
                      debug: true,
                      experimental: true,
                      ignoreWidth: false,
                      inWrapper: true,
                      ignoreHeight: false,
                      breakPages: true,
                      ignoreLastRenderedPageBreak: false,
                      useMathMLPolyfill: true,
                    }
                  )
                  .then((x) => {
                    this.total_page = document.querySelectorAll(".docx").length;
                    if (this.total_page > 0) this.current_page = 1;
                    document
                      .querySelectorAll(".docx")
                      .forEach((section) =>
                        this.pages_top_offsets.push(section.offsetTop)
                      );
                  });
              }
            });
        }
      }
    },
  },
};
</script>
<style>
.docx-wrapper {
  padding-bottom: 200px;
}
.page-number {
  position: fixed;
  top: 0px;
  right: 0px;
  margin-right: 40px;
  margin-top: 30px;
  background-color: #fff;
  padding: 10px;
  border: solid #000 1px;
  border-radius: 5px;
}
</style>
