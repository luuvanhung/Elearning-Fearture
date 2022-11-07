<template>
  <div class="my-container">
    <div class="selection-container">
      <div class="add-container">
        <h3 class="add-title">Add new object type</h3>
        <div>
          <input
            type="file"
            name="shape"
            accept=".svg"
            @change="fetchAddedImage"
          />
        </div>
        <div class="preview-image-block">
          <img :src="addedObjectType.url" alt="" />
        </div>
        <div class="name-block">
          <input
            type="text"
            style="width: 100%"
            placeholder="Input new object type name"
            v-model="addedObjectType.name"
          />
        </div>
        <div class="btn-add-block">
          <div class="btn btn-primary" @click="addNewObjectType">Add</div>
        </div>
      </div>

      <div class="select-object-type-container">
        <p style="text-align: center">Select objectType add to map</p>
        <div class="object-types-container">
          <div
            class="object-type-box"
            v-for="objectType in allObjectTypes"
            :key="objectType.id"
          >
            <div class="object-type-info">
              <img :src="objectType.svg_file" alt="" />
              <div class="object-type-name">{{ objectType.name }}</div>
            </div>
            <div
              class="btn add-object-type-action"
              @click="addObject(objectType)"
            >
              Add
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="map-container">
      <svg
        ref="map-container"
        xmlns="http://www.w3.org/2000/svg"
        width="1000"
        height="1000"
      >
        <object :data="require('@/static/images/send-to-right.svg')" />
        <Object
          v-for="object in allObjects"
          :key="object.id"
          :objectData="object"
          :deleteObject="deleteObject"
          :objectType="
            allObjectTypes.find(
              (objectType) => objectType.id === object.object_type
            )
          "
        />
      </svg>
    </div>
  </div>
</template>

<script>
import ObjectTypeService from "@/services/seat_map/objectType.services.js";
import ObjectService from "@/services/seat_map/object.services.js";
import Object from "./components/object.vue";

const IMAGE_SVG_PREFIX = "image-svg";
const RESIZER_SVG_PREFIX = "resizer-svg";
const CONTAINER_SVG_PREFIX = "container-svg";
const DELETER_SVG_PREFIX = "deleter-svg";

const DELETE_ICON = "./simple-delete.svg";

export default {
  name: "SeatMap",
  components: {
    Object,
  },
  data() {
    return {
      addedObjectType: {
        svg_file: null,
        name: "",
        url: "",
      },
      allObjectTypes: null,
      allObjects: [],
      resizerPoint: {
        x: null,
        y: null,
      },
      dragPoint: {
        x: null,
        y: null,
      },
      resizingObject: null,
      draggingElement: null,
      isUpdatingObject: false,
      IMAGE_SVG_PREFIX,
      RESIZER_SVG_PREFIX,
      CONTAINER_SVG_PREFIX,
      DELETER_SVG_PREFIX,
      DELETE_ICON,
    };
  },

  async created() {
    await this.fetchallObjectTypes();
    await this.fetchAllObjects();
  },

  methods: {
    async fetchallObjectTypes() {
      const res = await ObjectTypeService.getAll();
      if (res && res.status === 200) {
        this.allObjectTypes = res.data;
      } else {
        this.$toast.error("Cannot get object types");
      }
    },

    async fetchAllObjects() {
      const res = await ObjectService.getAll();
      if (res && res.status === 200) {
        this.allObjects = res.data;
      } else {
        this.$toast.error("Cannot get objects");
      }
    },

    async addNewObjectType() {
      const formdata = new FormData();
      formdata.append("svg_file", this.addedObjectType.svg_file);
      formdata.append("name", this.addedObjectType.name);
      if (this.addedObjectType.svg_file && this.addedObjectType.name) {
        const res = await ObjectTypeService.create(formdata);
        if (res && res.status === 201) {
          this.$toast.success("Create successfully");
          this.addedObjectType = {
            svg_file: null,
            name: "",
            url: "",
          };
          const newObjectType = {
            id: res.data.id,
            svg_file: res.data.svg_file,
            name: res.data.name,
          };
          this.allObjectTypes.unshift(newObjectType);
        } else {
          this.$toast.error("Create Failed");
        }
      }
    },

    fetchAddedImage(event) {
      const image = event.target.files[0];
      this.addedObjectType.svg_file = image;
      this.addedObjectType.url = URL.createObjectURL(image);
    },

    addObject(objectType) {
      const mapObjectContainer = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "svg"
      );
      fetch(objectType.svg_file)
        .then((res) => res.text())
        .then(async (svg) => {
          mapObjectContainer.insertAdjacentHTML("afterbegin", svg);
          const svgImage = mapObjectContainer.getElementsByTagName("svg")[0];

          let w = parseFloat(svgImage.getAttribute("width"));
          let h = parseFloat(svgImage.getAttribute("height"));
          let x = parseFloat(svgImage.getAttribute("x"));
          let y = parseFloat(svgImage.getAttribute("y"));

          w = w ? w : 512;
          h = h ? h : 512;
          x = x ? x : 0;
          y = y ? y : 0;

          const newObject = {
            width: w,
            height: h,
            offset_x: x,
            offset_y: y,
            object_type: objectType.id,
          };

          const res = await ObjectService.create(newObject);
          if (!res || res.status !== 201) {
            this.$toast.error("Create object fail!");
            mapObjectContainer.remove();
            return;
          }

          newObject.id = res.data.id;
          newObject.managed_by_user = res.data.managed_by_user;
          newObject.prioritized = res.data.prioritized;

          this.allObjects.push(newObject);
          mapObjectContainer.remove();
        });
    },

    async deleteObject(objectId) {
      const res = await ObjectService.delete(objectId);
      if (res && res.status === 204) {
        const deletedObject = this.allObjects.find(
          (object) => object.id === objectId
        );
        this.allObjects.splice(this.allObjects.indexOf(deletedObject), 1);
        this.$toast.success("Delete success");
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./index.scss";
</style>
