<template>
  <svg ref="svg-path-container" class="svg-path-container"></svg>
</template>

<script>
import {
  PATH_STOKE_COLOR,
  PATH_STOKE_WIDTH,
  PATH_FILL,
} from "@/const/organizationChart";

export default {
  name: "SvgPath",
  props: {
    numberOfChange: Number,
    rootGroupData: Object,
  },
  watch: {
    numberOfChange: function () {
      let svgContainer = this.$refs["svg-path-container"];
      svgContainer.innerHTML = "";
      const rootContentRef = this.$parent.$refs.content;
      this.iterateOrgData(this.rootGroupData, rootContentRef, svgContainer);
    },
  },
  data() {
    return {};
  },
  mounted() {
    let svgContainer = this.$refs["svg-path-container"];
    const rootContentRef = this.$parent.$refs.content;
    this.iterateOrgData(this.rootGroupData, rootContentRef, svgContainer);
  },
  methods: {
    iterateOrgData(orgParentData, orgRef, container) {
      // check if parent data has `isShowChildren` field value is false => not draw paths
      if (
        orgParentData.isShowChildren !== undefined &&
        !orgParentData.isShowChildren
      ) {
        return;
      }
      const orgParentDiv = this.getContentRef(orgRef, orgParentData);
      let svgOuter = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "svg"
      );
      if (orgParentData.type === "team") {
        const childRef = this.getChildRef(orgRef, orgParentData);
        let orgChildDiv = this.getContentRef(childRef, orgParentData);
        let connectingPathInfo = this.getPathConnectInfo(
          orgParentDiv,
          orgChildDiv
        );
        let path = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "path"
        );
        path.setAttribute("stroke", PATH_STOKE_COLOR);
        path.setAttribute("stroke-width", PATH_STOKE_WIDTH);
        path.setAttribute("fill", PATH_FILL);
        path.setAttribute("d", connectingPathInfo);
        svgOuter.appendChild(path);
        container.appendChild(svgOuter);
        return;
      }
      if (orgParentData.float_users) {
        const childRef = this.getChildRef(orgRef, orgParentData.float_users);
        let orgChildDiv = this.getContentRef(
          childRef,
          orgParentData.float_users
        );
        let connectingPathInfo = this.getPathConnectInfo(
          orgParentDiv,
          orgChildDiv
        );
        let path = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "path"
        );
        path.setAttribute("stroke", PATH_STOKE_COLOR);
        path.setAttribute("stroke-width", PATH_STOKE_WIDTH);
        path.setAttribute("fill", PATH_FILL);
        path.setAttribute("d", connectingPathInfo);
        svgOuter.appendChild(path);
      }
      orgParentData.children.forEach((orgChildData) => {
        const childRef = this.getChildRef(orgRef, orgChildData)[0];
        let orgChildDiv = this.getContentRef(childRef, orgChildData);
        let connectingPathInfo = this.getPathConnectInfo(
          orgParentDiv,
          orgChildDiv
        );
        let path = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "path"
        );
        path.setAttribute("stroke", PATH_STOKE_COLOR);
        path.setAttribute("stroke-width", PATH_STOKE_WIDTH);
        path.setAttribute("fill", PATH_FILL);
        path.setAttribute("d", connectingPathInfo);

        svgOuter.appendChild(path);

        if (orgChildData.children !== undefined) {
          this.iterateOrgData(orgChildData, childRef, svgOuter);
        }

        container.appendChild(svgOuter);
      });
    },
    getPathConnectInfo(orgParent, orgChild) {
      let parentOffsetX = orgParent.offsetLeft + 0.5 * orgParent.offsetWidth;
      let parentOffsetY = orgParent.offsetTop + orgParent.offsetHeight;
      let childOffsetX = orgChild.offsetLeft + 0.5 * orgChild.offsetWidth;
      let childOffsetY = orgChild.offsetTop;

      let svgContainer = this.$refs["svg-path-container"];
      svgContainer.setAttribute(
        "width",
        orgParent.offsetWidth +
          (orgParent.offsetLeft > orgChild.offsetLeft
            ? orgParent.offsetLeft
            : orgChild.offsetLeft)
      );
      if (svgContainer.getAttribute("height") < childOffsetY) {
        svgContainer.setAttribute("height", childOffsetY);
      }

      let gapX = childOffsetX - parentOffsetX;
      let gapY = Math.abs(childOffsetY - parentOffsetY);

      let curveX = 0.15 * gapX;
      let curveY = 0.15 * gapY;
      let minCurve =
        orgParent.offsetLeft === orgChild.offsetLeft
          ? Math.abs(curveX)
          : curveY;
      let isClockwise = parentOffsetX > childOffsetX ? 1 : 0;
      let signum = curveX > 0 ? 1 : -1;

      /*
      This path is separated into 3 lines:
      - 1st: vertical line start from parent position Y down and then make a curve
      - 2nd: horizontal line start after 1st line to child position X
      - 3rd: vertical line start after 2nd line to child position
      */
      let endLine1Vertical = parentOffsetY + minCurve;
      let endCurveX = parentOffsetX + minCurve * signum;
      let endCurveY = parentOffsetY + minCurve * 2;
      let endLine2Horizontal = childOffsetX - minCurve * signum;
      let endLine3Vertical = parentOffsetY + minCurve * 3;

      return `M ${parentOffsetX} ${parentOffsetY} V${endLine1Vertical} A${minCurve} ${minCurve} 0 0 ${isClockwise} ${endCurveX} ${endCurveY} H${endLine2Horizontal} A${minCurve} ${minCurve} 0 0 ${
        1 - isClockwise
      } ${childOffsetX} ${endLine3Vertical} V${childOffsetY}`;
    },
    getContentRef(orgRef, orgChildData) {
      return orgRef.$refs[
        `content-block-${orgChildData.type}-${orgChildData.id}`
      ];
    },
    getChildRef(orgRef, orgChildData) {
      return orgRef.$refs[
        `child-block-${orgChildData.type}-${orgChildData.id}`
      ];
    },
  },
};
</script>

<style lang="scss" scoped></style>
