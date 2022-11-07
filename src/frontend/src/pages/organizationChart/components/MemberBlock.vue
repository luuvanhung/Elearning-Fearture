<template>
  <div
    class="org-container"
    :ref="`org-container-${orgData.type}-${orgData.id}`"
  >
    <div class="content-container">
      <div
        class="content-block"
        :ref="`content-block-${orgData.type}-${orgData.id}`"
        :style="{ 'background-color': background_color, color: color }"
        @mousedown="isClickingOnContent = true"
        @mousemove="isClickingOnContent = false"
        @mouseup="handleMouseEventOnContentBlock"
      >
        <div class="name-block">
          <div
            class="member-block"
            v-for="children in orgData.children"
            :key="children.member_id"
          >
            <div class="avatar-block">
              <img
                :src="
                  !children.avatar ? avatar : createAvatarURL(children.avatar)
                "
                width="50px"
                height="50px"
                class="avatar-img"
              />
            </div>
            <router-link :to="createProfileURL(children.member_id)" tag="span">
              <div class="manager-name">{{ children.member_name }}</div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ORG_TYPES, API_IMAGE_SRC } from "@/const/organizationChart";
import logo from "@/static/images/icon.png";

export default {
  name: "MemberBlock",
  props: {
    orgData: Object,
  },
  components: {},
  data() {
    return {
      id: Number,
      type: String,
      name: String,
      memberName: String,
      background_color: String,
      color: String,
      avatar: logo,
      isClickingOnContent: false,
      profileId: "",
      API_IMAGE_SRC: String,
    };
  },
  created() {
    this.fetchDataFromProps();
  },
  methods: {
    fetchDataFromProps() {
      this.id = this.orgData.id;
      this.type = this.orgData.type;
      this.name = this.type;
      this.memberName = this.orgData.member_name;
      this.background_color = ORG_TYPES[this.orgData.type].background_color;
      this.color = ORG_TYPES[this.orgData.type].color;
    },
    handleMouseEventOnContentBlock() {
      if (this.isClickingOnContent) {
        window.location.href = `/profile/${this.orgData.member_id}`;
      }
      this.isClickingOnContent = false;
    },
    createAvatarURL(avatar) {
      return API_IMAGE_SRC + "/" + avatar;
    },
    createProfileURL(id) {
      return "/profile/" + id;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./Block.scss";
@import "./MemberBlock.scss";

.member-block {
  display: flex;
  padding-top: 10px;
  align-items: center;

  .manager-name {
    padding-left: 10px;
  }
}
</style>
