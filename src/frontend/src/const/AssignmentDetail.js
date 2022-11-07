const TOOLTIPS = {
  COMMON_ATTACHMENT: "This attachment CAN BE DOWNLOADED",
  FORCED_READ_ATTACHMENT: "This attachment MUST BE READ ONLINE!",
};

const ASSIGNMENT_STATUSES = {
  IN_PROGRESS: {
    detail: "In Progress",
    icon: "el-icon-edit-outline",
    tooltip: "You are working on this Lesson",
  },
  COMPLETED: {
    detail: "Completed",
    icon: "el-icon-success",
    tooltip: "You have completed this Lesson",
  },
  OVERDUE: {
    detail: "Overdue",
    icon: "el-icon-s-release",
    tooltip: "You are overdued on this lesson",
  },
  OPEN: {
    detail: "Open",
    icon: "",
    tooltip: "This Lesson is open to start working on",
  },
  LOCK: {
    detail: "Lock",
    icon: "el-icon-lock",
    tooltip: "This Lesson is locked with you",
  },
};

export { TOOLTIPS, ASSIGNMENT_STATUSES };
