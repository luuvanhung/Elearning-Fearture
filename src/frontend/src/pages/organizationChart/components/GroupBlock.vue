<template>
  <div class="org-container" :ref="`org-container-${type}-${id}`">
    <div class="content-container">
      <div
        class="content-block"
        :ref="`content-block-${type}-${id}`"
        :style="{ 'background-color': background_color, color: color }"
        @mousedown="isClickingOnContent = true"
        @mousemove="isClickingOnContent = false"
        @mouseup="handleMouseEventOnContentBlock"
      >
        <div class="avatar-block">
          <router-link :to="`/profile/${profileId}`" tag="span">
            <img
              :src="avatar"
              alt
              srcset
              width="50px"
              height="50px"
              class="avatar-img"
            />
          </router-link>
        </div>
        <div class="name-block">
          <div class="org-name">{{ name }}</div>
          <hr />
          <router-link :to="`/profile/${profileId}`" tag="span">
            <div class="manager-name">{{ managerName }}</div>
          </router-link>
        </div>
      </div>
    </div>

    <template v-if="isShowChildren">
      <div v-if="orgData.type !== 'team'" class="children-container">
        <FloatingMembers
          v-if="orgData.type === 'office' && orgData.float_users"
          :floatingMembers="orgData.float_users"
          :ref="`child-block-${orgData.float_users.type}-${orgData.float_users.id}`"
        />

        <GroupBlock
          v-for="childGroup in orgData.children"
          :key="`${childGroup.type}-${childGroup.id}`"
          :orgData="childGroup"
          :reRenderPaths="reRenderPaths"
          :ref="`child-block-${childGroup.type}-${childGroup.id}`"
          @hook:mounted="mountedChildren"
        ></GroupBlock>
      </div>
      <div v-else class="children-container">
        <FloatingMembers
          :floatingMembers="{
            ...orgData,
            data: orgData.children.map((member) => ({
              ...member,
              id: member.member_id,
            })),
          }"
          :ref="`child-block-${orgData.type}-${orgData.id}`"
        >
          <template v-slot:header>Members</template>
        </FloatingMembers>
      </div>
    </template>
  </div>
</template>

<script>
import { ORG_TYPES, API_IMAGE_SRC } from "@/const/organizationChart";
import logo from "@/static/images/icon.png";
import FloatingMembers from "./FloatingMemberBlock.vue";

export default {
  name: "GroupBlock",
  props: {
    orgData: Object,
    reRenderPaths: Function,
  },
  components: {
    FloatingMembers,
  },
  data() {
    return {
      id: Number,
      type: String,
      name: String,
      managerName: String,
      background_color: String,
      color: String,
      avatar: logo,
      isShowChildren: false,
      isChildrenCreated: false,
      isClickingOnContent: false,
      profileId: "",
    };
  },
  created() {
    this.fetchDataFromProps();
    this.isShowChildren =
      this.orgData.children !== undefined && this.orgData.children.length > 0;
    this.orgData.isShowChildren = this.isShowChildren;
  },
  methods: {
    fetchDataFromProps() {
      this.id = this.orgData.id;
      this.type = this.orgData.type;
      this.name = this.type + ": " + this.orgData.name;
      this.managerName = this.orgData.manager_name;
      this.background_color = ORG_TYPES[this.orgData.type].background_color;
      this.color = ORG_TYPES[this.orgData.type].color;
      if (this.orgData.avatar) {
        this.avatar = `${API_IMAGE_SRC}/${this.orgData.avatar}`;
      }
      this.profileId = this.orgData.manager_id;
    },
    switchShowingChildrenState() {
      if (
        this.orgData.children !== undefined &&
        this.orgData.children.length > 0
      ) {
        this.isShowChildren = !this.isShowChildren;
        this.orgData.isShowChildren = this.isShowChildren;

        if (!this.isShowChildren) {
          this.isChildrenCreated = false;
          setTimeout(
            function () {
              this.reRenderPaths();
            }.bind(this),
            0
          );
        } else {
          const startTime = new Date().getTime();
          let waitUntilChildrenCreated = setInterval(
            function () {
              if (
                this.isChildrenCreated ||
                new Date().getTime() > startTime + 3000
              ) {
                this.reRenderPaths();
                clearInterval(waitUntilChildrenCreated);
              }
            }.bind(this),
            0
          );
        }
      }
    },
    mountedChildren() {
      this.isChildrenCreated = true;
    },
    handleMouseEventOnContentBlock() {
      if (this.isClickingOnContent) {
        this.switchShowingChildrenState();
      }
      this.isClickingOnContent = false;
    },
  },
};
</script>

<style lang="scss" scoped>
@import "./Block.scss";
</style>
