<template>
  <div
    class="org-container"
    :ref="`org-container-${floatingMembers.type}-${floatingMembers.id}`"
  >
    <div class="content-container">
      <div
        class="content-block"
        :style="{ 'background-color': background_color, color: color }"
        :ref="`content-block-${floatingMembers.type}-${floatingMembers.id}`"
      >
        <div class="name-block">
          <div class="org-name">
            <h3>
              <slot name="header">Floating Members</slot>
            </h3>
          </div>
          <hr />
          <div
            class="member-block"
            v-for="member in floatingMembers.data"
            :key="member.id"
          >
            <div class="avatar-block">
              <img
                :src="
                  !member.avatar ? logo : `${API_IMAGE_SRC}/${member.avatar}`
                "
                width="50px"
                height="50px"
                class="avatar-img"
              />
            </div>
            <router-link :to="`/profile/${member.id}`" tag="span">
              <div class="manager-name">
                {{ member.name || member.member_name }}
              </div>
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
  name: "FloatingMembers",
  props: {
    floatingMembers: Object,
  },
  components: {},
  data() {
    return {
      background_color: "",
      color: "",
      logo,
      API_IMAGE_SRC,
    };
  },
  created() {
    this.background_color =
      ORG_TYPES[this.floatingMembers.type].background_color;
    this.color = ORG_TYPES[this.floatingMembers.type].color;
  },
  methods: {},
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
