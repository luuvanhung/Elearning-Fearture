<template>
  <div v-if="current_content">
    <TitleBar :title="assignment.course_name" v-show="assignment"></TitleBar>
    <el-row>
      <el-col :span="is_collapse ? 23 : 20">
        <div class="title-bar mt-3">
          <h3 class="p-3 text-white text-capitalize">
            {{
              isLesson(current_content.type)
                ? current_content.lesson_name
                : current_content.title
            }}
          </h3>
          <div
            class="d-flex align-items-center"
            v-if="isLesson(current_content.type)"
          >
            <el-tooltip
              v-show="!isOpen(current_content.status)"
              class="item"
              effect="light"
              :content="assignment_statuses[current_content.status].tooltip"
              placement="left"
            >
              <i
                :class="assignment_statuses[current_content.status].icon"
                class="mr-4"
                style="color: white; font-size: 24px; padding: 6px"
              ></i>
            </el-tooltip>
            <el-badge
              :value="number_of_unread_attachments"
              class="item"
              type="warning"
            >
              <el-popover placement="bottom" trigger="click">
                <div
                  v-if="
                    current_content.assignment_chapter_lesson_attachments.length
                  "
                >
                  <el-tooltip
                    class="item"
                    v-for="attachment in current_content.assignment_chapter_lesson_attachments"
                    :key="attachment.attachment.id"
                    effect="light"
                    :content="
                      attachment.attachment.forced_read
                        ? attachment_tooltips.FORCED_READ_ATTACHMENT
                        : attachment_tooltips.COMMON_ATTACHMENT
                    "
                    placement="left"
                  >
                    <el-tag
                      class="d-flex p-2 mt-2 mb-2"
                      style="margin-right: 0"
                      :class="{
                        'forced-read': attachment.attachment.forced_read,
                        read: attachment.read,
                      }"
                    >
                      <a
                        :href="
                          !attachment.attachment.forced_read &&
                          attachment.attachment.file
                        "
                        :style="{
                          opacity: +!attachment.attachment.forced_read,
                        }"
                        :download="!attachment.attachment.forced_read"
                      >
                        <img
                          class="btn-download mr-2"
                          :src="
                            require('@/static/images/download-svgrepo-com.svg')
                          "
                        />
                      </a>
                      <a
                        :href="attachment.file"
                        target="_blank"
                        @click="
                          onAttachmentClick(
                            attachment.attachment.id,
                            attachment.id
                          )
                        "
                        class="d-flex align-items-center"
                      >
                        <img
                          class="btn-video mr-2"
                          :src="
                            require(`@/static/images/${
                              mimetype_icons[
                                getMimeType(attachment.attachment.mine_type)
                              ]
                            }`)
                          "
                        />
                        <p>{{ attachment.attachment.original_name }}</p>
                      </a>
                    </el-tag>
                  </el-tooltip>
                </div>
                <div v-else>
                  <p>This lesson contains no Attachment</p>
                </div>
                <el-button slot="reference">Attachments</el-button>
              </el-popover>
            </el-badge>
          </div>
        </div>

        <!-- CONTENT -->
        <div class="lesson-content" v-if="isLesson(current_content.type)">
          <quill-editor
            class="view-form"
            :disabled="true"
            :options="VIEW_OPTIONS"
            v-model="current_content.lesson.content"
          />
          <div v-if="current_content.lesson_quizzes.length" class="container">
            <div v-for="quiz in current_content.lesson_quizzes" :key="quiz.id">
              <el-card
                style="
                  border-top: solid 12px #25c9d0;
                  border-radius: 12px;
                  color: black;
                  padding: 20px 30px;
                "
              >
                <h1 class="mb-5">{{ quiz.title }}</h1>
                <el-row>
                  <el-col :span="18">
                    <p style="font-size: 14px; color: #757171">
                      {{ quiz.description }}
                    </p>
                  </el-col>
                  <el-col
                    :span="4"
                    style="float: right; text-align: right; color: #25c9d0"
                  >
                    <span>
                      {{ `${quiz.threshold * 100}%` }}
                    </span>
                  </el-col>
                </el-row>
              </el-card>

              <question
                v-for="(question, index) in quiz.quiz_questions"
                :key="question.id"
                :question_id="question.id"
                :current_question="question"
                :questionIndex="index"
                :current_quiz="quiz"
                @updateQuizSubmittingData="updateQuizSubmittingData"
              ></question>

              <div class="d-flex align-items-center justify-content-center">
                <el-button class="mt-3" @click="onSubmitQuiz">Submit</el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- For Quiz -->
        <div v-else-if="isQuiz(current_content.type)" class="lesson-content">
          <div class="container">
            <el-card
              style="
                border-top: solid 12px #25c9d0;
                border-radius: 12px;
                color: black;
                padding: 20px 30px;
              "
            >
              <h1 class="mb-5">{{ current_content.title }}</h1>
              <el-row>
                <el-col :span="18">
                  <p style="font-size: 14px; color: #757171">
                    {{ current_content.description }}
                  </p>
                </el-col>
                <el-col
                  :span="4"
                  style="float: right; text-align: right; color: #25c9d0"
                >
                  <span>
                    {{ `${current_content.threshold * 100}%` }}
                  </span>
                </el-col>
              </el-row>
            </el-card>

            <question
              v-for="(question, index) in current_content.quiz_questions"
              :key="question.id"
              :question_id="question.id"
              :current_question="question"
              :questionIndex="index"
              :current_quiz="current_content"
              @updateQuizSubmittingData="updateQuizSubmittingData"
            ></question>

            <div class="d-flex align-items-center justify-content-center">
              <el-button class="mt-3" @click="onSubmitQuiz">Submit</el-button>
            </div>
          </div>
        </div>

        <!-- <div
          class="lesson-footer p-4 d-flex justify-content-between align-items-center"
          v-show="false"
        >
          <span
            :style="{
              opacity: assignment.content_ids.indexOf(current_content.id),
            }"
            @click="
              setCurrentContent(
                assignment.content_ids[
                  assignment.content_ids.indexOf(current_content.id) - 1
                ]
              )
            "
          >
            <i class="el-icon-d-arrow-left"></i>
            {{
              getLessonName(
                assignment.content_ids[
                  assignment.content_ids.indexOf(current_content.id) - 1
                ]
              )
            }}
          </span>
          <span
            :style="{
              opacity:
                assignment.content_ids.length -
                1 -
                assignment.content_ids.indexOf(current_content.id),
            }"
            @click="
              setCurrentContent(
                assignment.content_ids[
                  assignment.content_ids.indexOf(current_content.id) + 1
                ]
              )
            "
          >
            {{
              getLessonName(
                assignment.content_ids[
                  assignment.content_ids.indexOf(current_content.id) + 1
                ]
              )
            }}
            <i class="el-icon-d-arrow-right"></i>
          </span>
        </div> -->
      </el-col>

      <!-- MENU -->
      <el-col :span="is_collapse ? 1 : 4">
        <el-menu class="el-menu-vertical-demo" :collapse="is_collapse">
          <button class="collapse-btn" @click="is_collapse = !is_collapse">
            <i class="el-icon-d-arrow-right"></i>
          </button>

          <!-- Chapter Menu -->
          <el-submenu
            v-for="(chapter, index) in assignment.assignment_chapters"
            :key="chapter.id"
            :index="(index + 1).toString()"
            :disabled="isLocked(chapter.status)"
          >
            <template slot="title">
              <div v-if="!isLocked(chapter.status)">
                <i
                  v-if="isCompleted(chapter.status)"
                  class="el-icon-folder-checked"
                ></i>
                <i v-else class="el-icon-folder-opened"></i>
                <span slot="title">
                  {{ chapter.chapter_name }}
                </span>
              </div>
              <div v-else>
                <i class="el-icon-folder-opened" style="color: gray"></i>
                <span slot="title">
                  <el-tooltip
                    class="item"
                    effect="light"
                    :content="`You need to complete Chapter '${getChapterName(
                      chapter.previous_assignment_chapter_id
                    )}' first!`"
                    placement="left"
                  >
                    <span> {{ chapter.chapter_name }}</span>
                  </el-tooltip>
                </span>
              </div>
            </template>

            <!-- Inner Chapter Menu -->
            <el-menu-item-group>
              <el-menu-item
                v-for="(content, index) in chapter.contents"
                :key="content.id"
                :index="(index + 1).toString()"
                @click="setCurrentContent(content.id)"
                :disabled="isLesson(content.type) && isLocked(content.status)"
              >
                <template
                  slot="title"
                  v-if="isLesson(content.type) && !isLocked(content.status)"
                >
                  <i
                    v-if="isCompleted(content.status)"
                    class="el-icon-s-claim"
                  ></i>
                  <i v-else class="el-icon-s-order"></i>
                  <span slot="title">{{ content.lesson_name }}</span>
                  <i
                    class="status"
                    :class="assignment_statuses[content.status].icon"
                  ></i>
                </template>
                <template
                  slot="title"
                  v-else-if="isLesson(content.type) && isLocked(content.status)"
                >
                  <i class="el-icon-s-order" style="margin-right: 0"></i>
                  <span slot="title">
                    <el-tooltip
                      class="item"
                      effect="light"
                      :content="`You need to complete Lesson '${getLessonName(
                        content.previous_assignment_chapter_lesson_id
                      )}' first!`"
                      placement="left"
                    >
                      <span> {{ content.lesson_name }}</span>
                    </el-tooltip>
                  </span>
                  <i
                    class="status"
                    :class="assignment_statuses[content.status].icon"
                  ></i>
                </template>
                <template slot="title" v-else-if="isQuiz(content.type)">
                  <i class="el-icon-question"></i>
                  <span slot="title">{{ content.title }}</span>
                  <i
                    v-if="content.is_passed"
                    class="status el-icon-success"
                  ></i>
                </template>
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>
        </el-menu>
      </el-col>
    </el-row>

    <!-- Attachment View -->
    <el-drawer
      :destroy-on-close="true"
      :title="attachment_name"
      :visible.sync="is_viewing_attachment"
      direction="btt"
      custom-class="attachment-view"
      size="100%"
      @close="onAttachmentViewClose()"
    >
      <iframe :src="embedded_attachment_url" class="iframe-attachment"></iframe>
    </el-drawer>
  </div>

  <div v-else class="mt-3 d-flex align-items-center justify-content-center">
    <p>This assignment is empty</p>
  </div>
</template>

<script>
import AssignmentService from "@/services/e-learning/assignment";
import TitleBar from "@/components/TitleBar.vue";
import { MIMETYPES, MIMETYPE_ICONS } from "@/const/MimeTypes";
import { TOOLTIPS, ASSIGNMENT_STATUSES } from "@/const/AssignmentDetail";
import { VIEW_OPTIONS } from "@/const/quillEditorModules.js";
import question from "@/pages/elearningCourses/Quizzes/components/question.vue";

export default {
  data() {
    return {
      VIEW_OPTIONS: VIEW_OPTIONS,
      is_collapse: false,
      is_viewing_attachment: false,
      current_content: null,
      current_assignment_chapter: null,
      assignment: null,
      attachment_id: "",
      attachment_assignment_id: "",
      quiz_submitting_data: {
        quiz_result_details: [],
      },
    };
  },
  components: {
    TitleBar,
    question,
  },
  computed: {
    mimetype_icons() {
      return MIMETYPE_ICONS;
    },
    attachment_tooltips() {
      return TOOLTIPS;
    },
    assignment_statuses() {
      return ASSIGNMENT_STATUSES;
    },
    remaining_content_ids() {
      let remaining_content_ids = [];
      this.assignment.assignment_chapters.forEach((chapter) => {
        chapter.contents.forEach((content) => {
          if (
            (this.isLesson(content.type) &&
              !this.isCompleted(content.status)) ||
            this.isQuiz(content.type)
          )
            remaining_content_ids.push(content.id);
        });
      });
      return remaining_content_ids;
    },
    embedded_attachment_url() {
      return `/embed/${this.attachment_id}/${this.$route.params.id}/${this.current_content.assignment_chapter_id}/${this.current_content.id}/${this.attachment_assignment_id}`;
    },
    quiz_submitting_url() {
      if (this.isQuiz(this.current_content.type)) {
        if (this.current_content.assignment_chapter_id)
          return `${this.assignment.id}/chapters/${this.current_content.assignment_chapter_id}/quizzes/${this.current_content.id}/results`;
      }
      return "";
    },
    attachment_name() {
      let attachmentName = "";
      if (this.isLesson(this.current_content.type)) {
        this.current_content.assignment_chapter_lesson_attachments.forEach(
          (attachment) => {
            if (attachment.attachment.id === this.attachment_id)
              attachmentName = attachment.attachment.original_name;
          }
        );
        return attachmentName;
      } else return "";
    },
    number_of_unread_attachments() {
      return (
        this.isLesson(this.current_content.type) &&
        this.current_content &&
        this.current_content.assignment_chapter_lesson_attachments.filter(
          (attachment) => !attachment.read
        ).length
      );
    },
    number_of_unread_forced_read_attachments() {
      return (
        this.isLesson(this.current_content.type) &&
        this.current_content &&
        this.current_content.assignment_chapter_lesson_attachments.filter(
          (attachment) => !attachment.read && attachment.attachment.forced_read
        ).length
      );
    },
  },
  methods: {
    notBeingAssignedMessage() {
      this.$alert("This is not your assignment!", "", {
        confirmButtonText: "OK",
        type: "warning",
      })
        .then(() => {
          this.$router.push({ name: "MyAssignments" });
        })
        .catch(() => {
          this.$router.push({ name: "MyAssignments" });
        });
    },
    isOpen(status) {
      return status === "OPEN";
    },
    isLocked(status) {
      return status === "LOCK";
    },
    isCompleted(status) {
      return status === "COMPLETED";
    },
    isLesson(type) {
      return type === "lesson";
    },
    isQuiz(type) {
      return type === "quiz";
    },
    getLessonName(lessonId) {
      let lessonName = "";
      this.assignment.assignment_chapters.forEach((chapter) => {
        chapter.assignment_chapter_lessons.forEach((lesson) => {
          if (lesson.id === lessonId) {
            lessonName = lesson.lesson_name;
          }
        });
      });
      return lessonName;
    },
    getChapterName(chapterId) {
      let chapterName = "";
      this.assignment.assignment_chapters.forEach((chapter) => {
        if (chapter.id === chapterId) {
          chapterName = chapter.chapter_name;
        }
      });
      return chapterName;
    },
    getMimeType(originalType) {
      for (const type in MIMETYPES) {
        if (MIMETYPES[type].includes(originalType)) return type;
      }
    },
    updateQuizSubmittingData(questionSubmittingData) {
      this.quiz_submitting_data.quiz_result_details.forEach((question) => {
        if (question.question_id === questionSubmittingData.question_id) {
          question.quiz_result_detail_answers =
            questionSubmittingData.quiz_result_detail_answers;
        }
      });
    },
    scrollTop() {
      window.scroll({
        top: 0,
        behavior: "smooth",
      });
    },
    setCurrentContent(contentId) {
      // if (
      //   this.isLesson(this.current_content.type) &&
      //   this.number_of_unread_forced_read_attachments &&
      //   contentId !== this.current_content.id &&
      //   this.assignment.content_ids.indexOf(contentId) >
      //     this.assignment.content_ids.indexOf(this.current_content.id)
      // ) {
      //   this.$message({
      //     message: `You have ${this.number_of_unread_forced_read_attachments} attachment(s) that need to be finished reading!`,
      //     type: "warning",
      //     offset: 60,
      //   });
      // } else {
      //   this.assignment.assignment_chapters.forEach((chapter) => {
      //     chapter.contents.forEach((content) => {
      //       if (content.id === contentId) this.current_content = content;
      //     });
      //   });
      //   this.scrollTop();
      // }current_content.lesson

      this.assignment.assignment_chapters.forEach((chapter) => {
        chapter.contents.forEach((content) => {
          if (content.id === contentId) {
            this.current_content = content;
            this.current_assignment_chapter = chapter;
          }
        });
      });

      this.quiz_submitting_data = {
        quiz_result_details: [],
      };
      if (
        this.isQuiz(this.current_content.type) &&
        this.current_content.quiz_questions.length
      ) {
        this.current_content.quiz_questions.forEach((question) => {
          this.quiz_submitting_data.quiz_result_details.push({
            question_id: question.id,
            quiz_result_detail_answers: [],
          });

          question.question_answers.forEach((answer) => {
            this.quiz_submitting_data.quiz_result_details.forEach((quiz) => {
              if (quiz.question_id === question.id) {
                quiz.quiz_result_detail_answers.push({
                  answer_id: answer.id,
                  chosen: false,
                });
              }
            });
          });
        });
      }
      this.scrollTop();
    },
    async onAttachmentViewClose() {
      await this.getAssignment();
      this.setCurrentContent(this.current_content.id);
    },
    onAttachmentClick(attachmendId, attachmentAssignmentId) {
      this.attachment_id = attachmendId;
      this.attachment_assignment_id = attachmentAssignmentId;
      this.is_viewing_attachment = true;
    },
    async onSubmitQuiz() {
      if (!this.current_content.is_passed) {
        const quiz_result = await AssignmentService.submitQuiz(
          this.quiz_submitting_url,
          this.quiz_submitting_data
        );
        if (quiz_result.is_passed) {
          this.$alert(
            "Congrats! You have passed this Quiz!",
            "Congratulations",
            {
              confirmButtonText: "OK",
            }
          );
          await this.getAssignment();
          this.setCurrentContent(this.current_content.id);
          // Force re-rendering Question Component
          this.current_content.quiz_questions.forEach((question) => {
            question.id += 1;
          });
        } else {
          await this.getAssignment();
          this.$alert("You have failed! Let's try again!", "Failed", {
            confirmButtonText: "OK",
          });
        }
      } else {
        this.$alert("You have already passed this Quiz", "Information", {
          confirmButtonText: "OK",
        });
      }
    },
    async getAssignment() {
      const result = await AssignmentService.getDetail(this.$route.params.id);
      if (result) {
        this.assignment = result;
      } else {
        this.notBeingAssignedMessage();
      }
      this.preprogress();
    },
    preprogress() {
      this.assignment.content_ids = [];
      this.assignment.assignment_chapters.forEach((chapter) => {
        chapter.contents = [];
        if (chapter.assignment_chapter_lessons) {
          chapter.assignment_chapter_lessons.forEach((lesson) => {
            chapter.contents.push({
              ...lesson,
              type: "lesson",
            });
          });
        }
        if (chapter.chapter_quizzes) {
          chapter.chapter_quizzes.forEach((quiz) => {
            chapter.contents.push({
              ...quiz,
              type: "quiz",
              assignment_chapter_id: chapter.id,
              is_passed: false,
            });
          });
        }

        if (chapter.quiz_results.length) {
          const revered_quiz_results = chapter.quiz_results.reverse();
          revered_quiz_results.forEach((result) => {
            chapter.contents.forEach((content) => {
              if (this.isQuiz(content.type) && result.quiz.id === content.id) {
                content.is_passed = result.is_passed;
              }
            });
          });
        }

        chapter.contents.forEach((content) => {
          this.assignment.content_ids.push(content.id);
        });
      });
    },
  },
  async created() {
    await this.getAssignment();
    this.current_content =
      this.assignment.assignment_chapters[0].assignment_chapter_lessons[0];
  },
};
</script>

<style lang="scss" scoped>
.el-drawer__wrapper {
  margin: 80px 15px 30px 265px;
  border-radius: 10px;
  overflow: hidden;
  iframe {
    width: 100%;
    height: 100%;
  }
  .iframe-title {
    text-align: center;
  }
  header {
    color: red;
  }
}
.item {
  margin-right: 30px;
}
.title-bar {
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  background-color: #25c9d0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
h3 {
  font-size: 18px;
}
.lesson-content {
  padding: 15px 20px;
  background-color: #fff;
}
.lesson-footer {
  font-size: 15px;
  color: #585858;

  > span {
    cursor: pointer;

    &:hover {
      i {
        transition: all 0.2s ease-in-out;

        &.el-icon-d-arrow-left {
          transform: translateX(-10px);
        }
        &.el-icon-d-arrow-right {
          transform: translateX(10px);
        }
      }
    }
  }
}

.ql-video {
  width: 100% !important;
}

.el-menu {
  &.el-menu--collapse {
    float: right;
    .collapse-btn {
      transform: rotate(180deg);

      &:hover {
        transform: rotate(540deg);
      }
    }

    i {
      font-size: 24px;
    }
  }

  .collapse-btn {
    border: none;
    color: #25c9d0;
    font-size: 12px;
    background-color: #fff;
    position: absolute;
    top: 5px;
    left: -15px;
    border-radius: 50%;
    padding: 5px;
    z-index: 1000;
    cursor: pointer;
    transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);

    &:hover {
      transform: rotate(360deg);
      background-color: #25c9d0;
      color: #fff;
    }

    i {
      font-size: 16px;
    }
  }
}
.el-submenu {
  i {
    color: #25c9d0;
  }

  .is-active {
    font-weight: 700;
  }

  &__title {
    > img {
      width: 23px;
      height: 23px;
    }

    > span {
      line-height: 23px;
      font-size: 16px;
      font-weight: 600;
      display: inline-block;
      margin-left: 12px;
    }
  }
  & .el-menu-item {
    > .status {
      margin-left: 5px;
      font-size: 18px;
    }
  }
}
.el-menu--popup {
  & .el-menu-item {
    i {
      color: #25c9d0;
    }
    > .status {
      display: block;
      float: inline-end;
      margin-top: 19px;
      font-size: 18px;
    }
  }
}
.el-tag {
  height: 100%;

  &.forced-read {
    background-color: #fffbc3;
    border: 1px solid orange;
    color: #183568;
  }
  &.read {
    background-color: #c7ffec;
    border: 1px solid #47df01;
    color: #3f0c6e;
  }

  a {
    cursor: pointer;
  }
}
.el-tag + .el-tag {
  margin-left: 0 !important;
}
.btn-download {
  width: 25px;
  filter: invert(65%) sepia(66%) saturate(518%) hue-rotate(90deg)
    brightness(88%) contrast(95%);
}
.btn-video {
  width: 30px;
}
.ql-align-center {
  text-align: center;
}
@import "@/assets/scss/main.scss";
</style>
