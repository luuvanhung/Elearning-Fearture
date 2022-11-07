<template>
  <div class="video-container">
    <div>
      <video-player
        v-if="attachment.file"
        ref="videoPlayer"
        :options="playerOptions"
        :playsinline="true"
        customEventName="customstatechangedeventname"
        @timeupdate="onPlayerTimeupdate($event)"
        @ended="onPlayerEnded($event)"
      ></video-player>
    </div>
    <div class="transcript_nav" v-if="show">
      <p class="title">Transcript</p>
    </div>
    <el-scrollbar class="scrollbar" v-if="show">
      <div
        v-for="data in listTranscript"
        :key="data.id"
        class="row_table d-flex justify-content-center align-items-center"
      >
        <div class="el-table_1_column_1">
          <span class="cell">{{ data.displayTime }}</span>
        </div>
        <div class="el-table_1_column_2">{{ data.content }}</div>
      </div>
    </el-scrollbar>
  </div>
</template>
<script>
import "video.js/dist/video-js.css";
import { videoPlayer } from "vue-video-player";
import { MIMETYPES } from "@/const/MimeTypes";

export default {
  components: {
    videoPlayer,
  },
  props: ["attachment", "forced_read", "listTranscript"],
  data() {
    return {
      currentTime: 0,
      listIdTranscript: [],
      selectRowTrans: null,
      oldSelectRowTrans: null,

      value: "English",
      options: [
        {
          value: "English",
          lable: "English",
        },
        {
          value: "Vietnamese",
          lable: "Vietnamese",
        },
      ],
      show: false,
      script: [],
    };
  },
  computed: {
    player() {
      return this.$refs.videoPlayer.player;
    },
    playerOptions() {
      return {
        muted: true,
        language: "en",
        width: "1440px",
        height: "700px",
        playbackRates: [0.5, 1.0, 1.5, 2.0],
        sources: [
          {
            type: this.attachment.mine_type,
            src: this.attachment.file,
          },
        ],
        controlBar: {
          progressControl: {
            seekBar: true,
          },
        },
      };
    },
  },
  watch: {
    listTranscript: function () {
      this.fetchTranscript();
      if (this.listTranscript.length > 0) this.show = true;
    },
    currentTime: function () {
      const index = this.listIdTranscript.indexOf(this.currentTime);
      if (index !== -1) {
        this.oldIndex = this.listIdTranscript[index - 1];
        this.select(this.currentTime);
      }
    },
    selectRowTrans: function () {
      if (this.oldSelectRowTrans != null) {
        const parentList = document.querySelectorAll(".el-table_1_column_1");
        for (let i = 0; i < parentList.length; i++) {
          const child = parentList[i].querySelector(".cell");
          if (child.innerHTML == this.changeSecondToDate(this.oldIndex)) {
            let obj = child.closest(".row_table");
            obj.style.backgroundColor = "#fff";
            obj.style.color = "black";
            obj.scrollIntoView();
            break;
          }
        }
      }
    },
  },
  methods: {
    fetchTranscript() {
      this.listTranscript.map((el) => {
        el.id,
          el.script_at_second,
          el.content,
          (el.displayTime = this.changeSecondToDate(el.script_at_second));
      });
      this.listTranscript.forEach((element) => {
        this.listIdTranscript.push(element.script_at_second);
      });
    },
    select(index) {
      if (this.selectRowTrans) {
        this.oldSelectRowTrans = this.selectRowTrans.cloneNode(true);
      }
      const parentList = document.querySelectorAll(".el-table_1_column_1");
      for (let i = 0; i < parentList.length; i++) {
        const child = parentList[i].querySelector(".cell");
        if (child.innerHTML == this.changeSecondToDate(index)) {
          this.selectRowTrans = child.closest(".row_table");
          this.selectRowTrans.style.backgroundColor = "#52C6CF";
          this.selectRowTrans.style.color = "#fff";
          break;
        }
      }
    },
    onPlayerTimeupdate(player) {
      this.currentTime = Math.floor(player.cache_.currentTime);
    },
    onPlayerEnded(player) {
      let trackingData = {
        read: true,
      };
      this.$emit("onProgressChange", trackingData);
    },
    changeSecondToDate(seconds) {
      return new Date(seconds * 1000).toISOString().slice(11, 19);
    },
  },
  created() {
    if (
      !JSON.parse(process.env.VUE_APP_ALLOW_SEEKING_VIDEO.toLowerCase()) &&
      this.forced_read
    ) {
      this.player.controlBar.progressControl.disable();
    }
  },
};
</script>
<style scoped>
.video-container {
  max-width: 1440px;
  margin: 0 auto;
}
.video-js {
  width: 100%;
}
.title {
  display: inline-block;
  width: 30%;
  padding-left: 40px;
  font-weight: 700;
}
.transcript_nav {
  margin: 16px 0;
  padding-top: 10px;
  width: 1440px !important;
}
.scrollbar {
  padding-top: 10px;
  padding-bottom: 20px;
  padding-left: 20px;
  padding-right: 20px;
  background-color: #e9ecef;
}
.el-scrollbar__view {
  width: 1400px;
  height: 180px;
}
.row_table {
  height: 40px;
  width: 1440px;
  margin: 14px;
  border-radius: 4px;
  background-color: #fff;
}
.el-table_1_column_1 {
  line-height: 40px;
  display: inline-block;
  padding-left: 20px;
}
.el-table_1_column_2 {
  display: inline-block;
  padding-left: 20px;
  width: 90%;
  line-height: 40px;
}
</style>
