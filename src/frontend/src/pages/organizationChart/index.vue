<template>
  <div
    class="org-outer-box"
    ref="org-outer-box"
    id="org-outer-box"
    v-dragscroll
    @touchmove.prevent
    @scroll.prevent
    @wheel.prevent="scrollToZoom($event)"
  >
    <div
      class="organization-chart-container"
      ref="organization-chart-container"
    >
      <div ref="content-block">
        <GroupBlock
          :reRenderPaths="reRenderPaths"
          :orgData="rootGroup"
          v-if="rootGroup"
          ref="content"
          @hook:mounted="showPath"
        />
      </div>
      <div class="path-container" ref="svg-line-outer-box">
        <SvgPath
          :rootGroupData="rootGroup"
          :numberOfChange="numberOfChange"
          v-if="rootGroup && isShowingPath"
          ref="svg-line"
          @hook:mounted="scrollViewToCenter"
        />
      </div>
    </div>
    <div class="lmask" ref="loading-mask"></div>
  </div>
</template>

<script>
import GroupBlock from "./components/GroupBlock.vue";
import SvgPath from "./components/SvgPath.vue";
import officeService from "@/services/office/office.service.js";

export default {
  name: "OrganizationChart",
  middleware: "authentication",
  components: {
    GroupBlock,
    SvgPath,
  },
  data() {
    return {
      rootGroup: null,
      maxWidthIndexTree: 1,
      maxHeightIndexTree: 1,
      zoom: 1,
      ZOOM_SPEED: 0.05,
      isShowingPath: false,
      numberOfChange: 0,
    };
  },
  async created() {
    const res = await officeService.getOrganizationTree();
    this.rootGroup = res.data;
  },

  mounted() {},

  methods: {
    scrollToZoom(e) {
      const component = this.$refs["organization-chart-container"];
      const orgOuterBox = this.$refs["org-outer-box"];
      const ratioX = orgOuterBox.scrollLeft / orgOuterBox.scrollWidth;
      if (e.deltaY < 0) {
        component.style.transform = `scale(${(this.zoom += this.ZOOM_SPEED)})`;
      } else {
        if (this.zoom - this.ZOOM_SPEED > 0) {
          component.style.transform = `scale(${(this.zoom -=
            this.ZOOM_SPEED)})`;
        }
      }
      orgOuterBox.scrollLeft = ratioX * orgOuterBox.scrollWidth;
    },
    scrollViewToCenter() {
      const rootGroupBlockRef =
        this.$refs.content.$refs[
          `content-block-${this.rootGroup.type}-${this.rootGroup.id}`
        ];
      rootGroupBlockRef.scrollIntoView({
        behavior: "smooth",
        inline: "center",
      });
      this.$refs["loading-mask"].style.display = "none";
      this.isShowingPath = true;
    },
    reRenderPaths() {
      this.numberOfChange++;
    },
    showPath() {
      this.isShowingPath = true;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./index.scss";
</style>
