<template>
  <svg
    :ref="`container-svg-${objectData.id}`"
    xmlns="http://www.w3.org/2000/svg"
  >
    <circle
      :ref="`resizer-svg-${objectData.id}`"
      xmlns="http://www.w3.org/2000/svg"
      style="cursor: nwse-resize"
      r="10"
      stroke="blue"
      stroke-width="1"
      fill="white"
      :id="`resizer-svg-${objectData.id}`"
    ></circle>

    <svg
      :ref="`deleter-svg-${objectData.id}`"
      :id="`deleter-svg-${objectData.id}`"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 40 40"
      width="16px"
      height="16px"
      @click="deleteObject(objectData.id)"
    >
      <path
        fill="#f78f8f"
        d="M21 24.15L8.857 36.293 4.707 32.143 16.85 20 4.707 7.857 8.857 3.707 21 15.85 33.143 3.707 37.293 7.857 25.15 20 37.293 32.143 33.143 36.293z"
      />
      <path
        fill="#c74343"
        d="M33.143,4.414l3.443,3.443L25.15,19.293L24.443,20l0.707,0.707l11.436,11.436l-3.443,3.443 L21.707,24.15L21,23.443l-0.707,0.707L8.857,35.586l-3.443-3.443L16.85,20.707L17.557,20l-0.707-0.707L5.414,7.857l3.443-3.443 L20.293,15.85L21,16.557l0.707-0.707L33.143,4.414 M33.143,3L21,15.143L8.857,3L4,7.857L16.143,20L4,32.143L8.857,37L21,24.857 L33.143,37L38,32.143L25.857,20L38,7.857L33.143,3L33.143,3z"
      />
    </svg>
  </svg>
</template>

<script>
import ObjectService from "@/services/seat_map/object.services.js";

const IMAGE_SVG_PREFIX = "image-svg";
const RESIZER_SVG_PREFIX = "resizer-svg";
const CONTAINER_SVG_PREFIX = "container-svg";
const DELETER_SVG_PREFIX = "deleter-svg";

export default {
  name: "Object",
  props: {
    objectData: Object,
    objectType: Object,
    deleteObject: Function,
  },
  data() {
    return {
      IMAGE_SVG_PREFIX,
      RESIZER_SVG_PREFIX,
      CONTAINER_SVG_PREFIX,
      DELETER_SVG_PREFIX,
      resizerPoint: {
        x: null,
        y: null,
      },
      dragPoint: {
        x: null,
        y: null,
      },
      isUpdatingObject: false,
    };
  },
  mounted() {
    const container = this.$refs[`container-svg-${this.objectData.id}`];

    fetch(this.objectType.svg_file)
      .then((res) => res.text())
      .then(async (svg) => {
        container.insertAdjacentHTML("afterbegin", svg);
        const svgImage = container.getElementsByTagName("svg")[0];
        this.setPropertiesObject(container, svgImage);
      });
  },
  methods: {
    setPropertiesObject(container, svgImage) {
      let width = this.objectData.width;
      let height = this.objectData.height;
      let x = this.objectData.offset_x;
      let y = this.objectData.offset_y;

      svgImage.setAttribute("width", width);
      svgImage.setAttribute("height", height);
      container.setAttribute("x", x);
      container.setAttribute("y", y);
      container.addEventListener("mousedown", this.startDrag);

      svgImage.setAttribute(
        "id",
        `${this.IMAGE_SVG_PREFIX}-${this.objectData.id}`
      );
      svgImage.setAttribute("style", "cursor: grabbing;");

      container = this.$refs[`container-svg-${this.objectData.id}`];
      const bbox = container.getBBox();
      const xCorner = bbox.x + bbox.width;
      const yCorner = bbox.y + bbox.height;

      const resizer = this.$refs[`resizer-svg-${this.objectData.id}`];
      const deleter = this.$refs[`deleter-svg-${this.objectData.id}`];
      resizer.setAttribute("cx", String(xCorner));
      resizer.setAttribute("cy", String(yCorner));
      deleter.setAttribute("x", String(0));
      deleter.setAttribute("y", String(yCorner));

      resizer.addEventListener("mousedown", this.resizerMouseDown);
    },

    resizerMouseDown(e) {
      this.resizerPoint = {
        x: e.clientX,
        y: e.clientY,
      };
      const target = e.target;
      target.addEventListener("mousemove", this.resizerMouseMove);
      target.addEventListener("mouseup", this.clearResizeEvent);
      target.addEventListener("mouseleave", this.clearResizeEvent);
    },

    resizerMouseMove(e) {
      const current_points = {
        x: e.clientX,
        y: e.clientY,
      };

      const image = document.getElementById(
        `${this.IMAGE_SVG_PREFIX}-${this.objectData.id}`
      );
      let w = parseFloat(image.getAttribute("width"));
      let h = parseFloat(image.getAttribute("height"));

      const dx = current_points.x - this.resizerPoint.x;
      const dy = current_points.y - this.resizerPoint.y;

      w += dx;
      h += dy;

      image.setAttribute("width", w);
      image.setAttribute("height", h);

      // update resizer
      let resizer = this.$refs[`resizer-svg-${this.objectData.id}`];
      let cx = parseFloat(resizer.getAttribute("cx"));
      let cy = parseFloat(resizer.getAttribute("cy"));

      cx += dx;
      cy += dy;

      resizer.setAttribute("cx", cx);
      resizer.setAttribute("cy", cy);
      const deleter = this.$refs[`deleter-svg-${this.objectData.id}`];
      deleter.setAttribute("x", 0);
      deleter.setAttribute("y", cy);

      this.resizerPoint = current_points;
    },

    async clearResizeEvent(e) {
      if (!this.isUpdatingObject) {
        this.isUpdatingObject = true;
        e.target.removeEventListener("mousemove", this.resizerMouseMove);

        const image = document.getElementById(
          `${this.IMAGE_SVG_PREFIX}-${this.objectData.id}`
        );

        this.objectData.width = parseFloat(image.getAttribute("width"));
        this.objectData.height = parseFloat(image.getAttribute("height"));

        const res = await ObjectService.update(this.objectData);
        if (!res || res.status !== 200) {
          this.$toast.error("Update Failed!");
        }
        this.isUpdatingObject = false;
      }
    },

    startDrag(e) {
      const container = this.$refs[`container-svg-${this.objectData.id}`];
      const deleter = this.$refs[`deleter-svg-${this.objectData.id}`];
      if (
        !e.target.id.startsWith(this.RESIZER_SVG_PREFIX) &&
        !deleter.contains(e.target) &&
        container.contains(e.target)
      ) {
        const svg = e.target;
        this.dragPoint = {
          x: e.layerX,
          y: e.layerY,
        };
        svg.addEventListener("mousemove", this.drag);
        svg.addEventListener("mouseup", this.endDrag);
        svg.addEventListener("mouseleave", this.endDrag);
      }
    },

    drag(e) {
      e.preventDefault();
      const container = this.$refs[`container-svg-${this.objectData.id}`];
      const currentDragPoint = {
        x: e.layerX,
        y: e.layerY,
      };
      const dx = currentDragPoint.x - this.dragPoint.x;
      const dy = currentDragPoint.y - this.dragPoint.y;
      let x = parseFloat(container.getAttribute("x"));
      let y = parseFloat(container.getAttribute("y"));

      x = x ? x : 0;
      y = y ? y : 0;
      x += dx;
      y += dy;
      container.setAttribute("x", x);
      container.setAttribute("y", y);

      this.dragPoint = currentDragPoint;
    },

    async endDrag(e) {
      if (!this.isUpdatingObject) {
        this.isUpdatingObject = true;
        e.target.removeEventListener("mousemove", this.drag);
        const container = this.$refs[`container-svg-${this.objectData.id}`];
        this.objectData.offset_x = parseFloat(container.getAttribute("x"));
        this.objectData.offset_y = parseFloat(container.getAttribute("y"));

        const res = await ObjectService.update(this.objectData);
        if (!res || res.status !== 200) {
          this.$toast.error("Update Failed!");
        }
        this.isUpdatingObject = false;
        e.target.removeEventListener("mouseup", this.endDrag);
        e.target.removeEventListener("mouseleave", this.endDrag);
      }
    },
  },
};
</script>

<style></style>
