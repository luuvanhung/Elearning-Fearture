<template>
  <div class="mt-3">
    <div :class="['d-flex', isAdmin ? 'bd-highlight' : 'user-bd-highlight']">
      <restricted-view :scope="['elearning_topic:edit']">
        <div class="mr-auto bd-highlight">
          <el-button
            type="primary"
            icon="el-icon-circle-plus"
            @click="dialogAddTopic = true"
            size="medium"
            >Add Topic</el-button
          >
        </div>
      </restricted-view>
      <div>
        <el-input placeholder="Search by Title" v-model="title"></el-input>
      </div>
    </div>
    <el-table
      highlight-current-row
      :data="filterTopic.slice((page - 1) * page_size, page * page_size)"
      v-loading="loading"
      style="width: 100%"
    >
      <el-table-column type="index" sortable align="center" width="80" />

      <el-table-column sortable prop="title" label="Title" width="200">
        <template slot-scope="scope">
          <div class="dont-break-out">
            <p>{{ scope.row.title }}</p>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="description" label="Description" min-width="500">
        <template slot-scope="scope">
          <div class="dont-break-out">
            <p>{{ scope.row.description }}</p>
          </div>
        </template>
      </el-table-column>

      <el-table-column
        sortable
        prop="updated_at"
        label="Updated at"
        width="150"
        align="center"
      >
        <template slot-scope="scope">
          <div class="dont-break-out">
            <p>{{ scope.row.updated_at | datetimeFormatter }}</p>
          </div>
        </template>
      </el-table-column>
      <restricted-view :scope="['elearning_topic:edit']">
        <el-table-column
          fixed="right"
          label="Operations"
          width="160"
          align="center"
          prop="id"
        >
          <template slot-scope="scope">
            <el-tooltip
              effect="light"
              :content="TOOLTIPS.delete_topic"
              placement="bottom"
            >
              <el-popconfirm
                confirm-button-text="Delete"
                cancel-button-text="No"
                title="Delete this topic?"
                @confirm="handleDeleteTopic(scope.row.id)"
              >
                <template slot="reference">
                  <el-button
                    style="font-size: 20px"
                    type="text"
                    icon="el-icon-delete"
                  />
                </template>
              </el-popconfirm>
            </el-tooltip>
            <el-tooltip
              effect="light"
              :content="TOOLTIPS.edit_topic"
              placement="bottom"
            >
              <el-button
                type="text"
                style="font-size: 20px"
                icon="el-icon-edit"
                @click="handleUpdateTopic(scope.row)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </restricted-view>
    </el-table>

    <el-pagination
      class="pagination"
      background
      hide-on-single-page
      layout="prev, pager, next"
      :current-page="page"
      :page-size="page_size"
      @current-change="changePages"
      :page-count="pageCount"
    ></el-pagination>

    <el-dialog
      title="Add Topic"
      :visible.sync="dialogAddTopic"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <AddTopicModal :dialogAddTopic.sync="dialogAddTopic" />
    </el-dialog>

    <el-dialog
      title="Edit Topic"
      :visible.sync="dialogUpdateTopic"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <UpdateTopicModal
        :dialogUpdateTopic.sync="dialogUpdateTopic"
        :form="currentTopic"
      />
    </el-dialog>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import RestrictedView from "@/components/RestrictedView.vue";
import TopicService from "@/services/e-learning/topic";
import AddTopicModal from "@/pages/elearningTopics/AddTopicModal";
import UpdateTopicModal from "@/pages/elearningTopics/UpdateTopicModal";

const TOOLTIPS = {
  edit_topic: "Edit this topic",
  delete_topic: "Delete this topic",
};

export default {
  name: "Topics",
  data() {
    return {
      TOOLTIPS: TOOLTIPS,
      title: null,
      loading: false,
      page: 1,
      page_size: 10,
      dialogAddTopic: false,
      dialogUpdateTopic: false,
      currentTopic: null,
      isAdmin: JSON.parse(localStorage.getItem("is_admin")),
    };
  },
  components: {
    AddTopicModal,
    UpdateTopicModal,
    RestrictedView,
  },
  methods: {
    ...mapActions("elearning", ["deleteTopic"]),
    async changePages(newPage) {
      this.page = newPage;
    },
    async handleDeleteTopic(topic_id) {
      const response = await this.deleteTopic(topic_id);
      if (
        this.filterTopic.length % this.page_size === 0 &&
        this.filterTopic.length !== 0 &&
        this.pageCount + 1 === this.page
      ) {
        this.page = this.page - 1;
      }
    },
    handleUpdateTopic(topic) {
      this.currentTopic = { ...topic };
      this.dialogUpdateTopic = true;
    },
  },
  computed: {
    ...mapState("elearning", ["topics"]),
    pageCount() {
      return Math.ceil(this.filterTopic.length / this.page_size);
    },
    filterTopic() {
      let topicAfterFilter = this.topics;
      let titleAfterProcessing =
        this.title !== null && this.title !== ""
          ? this.title.trim().toLowerCase()
          : null;
      if (titleAfterProcessing) {
        topicAfterFilter = this.topics.filter((val) =>
          val.title.toLowerCase().includes(titleAfterProcessing)
        );
      }
      return topicAfterFilter;
    },
  },
  watch: {
    title: function () {
      this.page = 1;
    },
  },
  filters: {
    datetimeFormatter: function (value) {
      if (!value) return "";
      let date = new Date(value);
      let result = date.toLocaleDateString() + "\n" + date.toLocaleTimeString();
      return result;
    },
  },
};
</script>

<style scoped>
.user-bd-highlight {
  justify-content: flex-end;
}
.bd-highlight {
  justify-content: space-between;
}
.el-table {
  margin-top: 15px;
  font-size: 1rem;
}
.el-button {
  font-size: 1rem;
}
.pagination {
  text-align: center;
  margin-top: 35px;
}
.dont-break-out {
  word-wrap: break-word !important; /* IE 5.5-7 */
  white-space: -moz-pre-wrap !important; /* Firefox 1.0-2.0 */
  white-space: pre-wrap !important; /* current browsers */
  overflow-wrap: break-word !important;
  word-break: break-word !important;
}
</style>
