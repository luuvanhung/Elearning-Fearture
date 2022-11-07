<template>
  <div id="pdfvuer">
    <div id="buttons" class="nav-buttons">
      <span class="item item-button" v-if="checkSize" @click="onBackButtonClick"
        >Back</span
      >
      <span class="item">{{ page }} / {{ numPages ? numPages : "∞" }}</span>
      <span class="item item-button" v-if="checkSize" @click="onNextButtonClick"
        >Forward</span
      >
      <span class="item item-button" @click="onZoomInButtonClick">Zoom -</span>
      <span class="item">{{ formattedZoom }} %</span>
      <span class="item item-button" @click="onZoomOutButtonClick">Zoom +</span>
    </div>
    <pdf
      :src="url"
      v-for="i in numPages"
      :key="i"
      :id="i"
      :page="i"
      :scale.sync="scale"
      style="width: 100%; margin: 20px auto"
      :annotation="true"
      :resize="true"
      @link-clicked="handle_pdf_link"
    >
      <template slot="loading"> loading content here... </template>
    </pdf>
  </div>
</template>
<script>
import pdf from "pdfvuer";
export default {
  components: {
    pdf,
  },
  props: {
    attachment: Object,
    prefix: String,
    assignment_chapter_lesson_attachment: Object,
  },
  data() {
    return {
      page: 1,
      baseUrl: this.attachment.file,
      numPages: 0,
      errors: [],
      scale: "page-width",
    };
  },

  computed: {
    url() {
      return `${this.prefix}${this.baseUrl.substring(
        this.baseUrl.indexOf(":")
      )}`;
    },
    formattedZoom() {
      return Number.parseInt(this.scale * 100);
    },
  },
  watch: {
    show: function (s) {
      if (s) {
        this.getPdf();
      }
    },
    page: function (p) {
      // tracking
      if (this.assignment_chapter_lesson_attachment && this.page > 0) {
        let trackingData = {
          current_page: this.page,
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
  mounted() {
    this.getPdf();
  },
  methods: {
    checkSize() {
      return this.formattedZoom > 80;
    },
    onBackButtonClick() {
      this.page -= this.page > 1 ? 1 : 0;
      document.getElementById(this.page).scrollIntoView();
    },
    onNextButtonClick() {
      this.page += this.page < this.numPages ? 1 : 0;
      document.getElementById(this.page).scrollIntoView();
    },
    onZoomInButtonClick() {
      this.scale -= this.scale > 0.2 ? 0.1 : 0;
    },
    onZoomOutButtonClick() {
      this.scale += this.scale < 2 ? 0.1 : 0;
    },

    handle_pdf_link: function (params) {
      var page = document.getElementById(String(params.pageNumber));
      page.scrollIntoView();
    },
    getPdf() {
      var self = this;
      self.pdfdata = pdf.createLoadingTask(this.url);
      self.pdfdata.then((pdf) => {
        self.numPages = pdf.numPages;
        window.onscroll = function () {
          changePage();
        };

        function changePage() {
          var i = 1,
            count = Number(pdf.numPages);
          let extraHeight = document.querySelectorAll(".page")[0].offsetHeight;
          do {
            if (
              window.pageYOffset + window.innerHeight - extraHeight / 3 >=
                self.findPos(document.getElementById(i)) &&
              window.pageYOffset + window.innerHeight - extraHeight / 3 <=
                self.findPos(document.getElementById(i + 1))
            ) {
              self.page = i == 0 ? 1 : i;
            }
            i++;
          } while (i < count);
          if (
            window.pageYOffset + window.innerHeight - extraHeight / 3 >=
            self.findPos(document.getElementById(i))
          ) {
            self.page = i == 0 ? 1 : i;
          }
        }
      });
    },
    findPos(obj) {
      return obj.offsetTop;
    },
  },
};
</script>
<style scoped>
#buttons {
  margin-left: 0 !important;
  margin-right: 0 !important;
}
.content {
  padding: 16px;
}
.item {
  padding: 5px;
  margin: 10px;
}
.nav-buttons {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  background-color: #00000022;
  z-index: 10;
}
.item-button:hover {
  background-color: #00000088;
  cursor: pointer;
}
</style>
