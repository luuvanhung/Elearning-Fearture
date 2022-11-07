<template>
  <div v-if="attributesOfSideItem['children']">
    <li class="dropdown_list_container category">
      <div class="dropdown">
        <div
          class="dropdown_header mx-auto d-flex align-items-center"
          @click="show_dropdown()"
        >
          <div class="sidebar-item-icon first-level-item">
            <img
              :src="require('@/static/images/' + attributesOfSideItem['icon'])"
              class="filter icon"
            />
          </div>
          <span>{{ sideItem }}</span>
          <img
            :src="require(`@/static/images/iconDropdown.svg`)"
            :class="{ iconDropdown: dropdowned[sideItem] }"
            class="filter ml-auto"
          />
        </div>
      </div>
    </li>
    <div>
      <div class="dropdown_content" :class="{ active: dropdowned[sideItem] }">
        <ul class="list-unstyled components p-0">
          <div
            v-for="(childItem, childItemTitle) in attributesOfSideItem[
              'children'
            ]"
            :key="childItemTitle"
          >
            <div
              v-if="!childItem['scopes']"
              :class="clickedState(childItem['path'])"
            >
              <li class="category">
                <router-link
                  :to="childItem['path']"
                  class="btn font-weight-bold text-left"
                >
                  <div class="sidebar-item-icon">
                    <img
                      :src="require('@/static/images/' + childItem['icon'])"
                      class="filter icon"
                    />
                  </div>
                  <span>{{ childItemTitle }}</span>
                </router-link>
              </li>
            </div>
            <restricted-view v-else :scopes="childItem['scopes']">
              <template v-slot:default>
                <div :class="clickedState(childItem['path'])">
                  <li class="category">
                    <router-link
                      :to="childItem['path']"
                      class="btn font-weight-bold text-left"
                    >
                      <div class="sidebar-item-icon">
                        <img
                          :src="require('@/static/images/' + childItem['icon'])"
                          class="filter icon"
                        />
                      </div>
                      <span>{{ childItemTitle }}</span>
                    </router-link>
                  </li>
                </div>
              </template>
            </restricted-view>
          </div>
        </ul>
      </div>
    </div>
  </div>
  <div v-else :class="clickedState(attributesOfSideItem['path'])">
    <li class="category">
      <router-link
        :to="attributesOfSideItem['path']"
        class="btn font-weight-bold text-left"
      >
        <div class="sidebar-item-icon first-level-item">
          <img
            :src="require('@/static/images/' + attributesOfSideItem['icon'])"
            class="filter icon"
          />
        </div>
        <span>{{ sideItem }}</span>
      </router-link>
    </li>
  </div>
</template>

<script>
import RestrictedView from "@/components/RestrictedView.vue";
export default {
  props: {
    sideItem: String,
    attributesOfSideItem: Object,
    dropdowned: Object,
    buttonIsHighlighted: Object,
  },
  components: {
    RestrictedView,
  },
  methods: {
    show_dropdown: function () {
      const key = this.sideItem;
      const state = this.dropdowned[key];
      this.$emit("setDropdownedState", key, !state);
    },
    clickedState(key) {
      return this.buttonIsHighlighted[key] ? "clicked" : "unClicked";
    },
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/scss/sidebar.scss";
</style>
