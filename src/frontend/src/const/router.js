export const ROUTERS = {
  // ROUTER & SIDEBAR
  // SideBar - Company Calendar
  Calendar: "/",
  // SideBar - Employee Management
  EmployeeList: "/employeelist",
  Skill: "/skill",
  Titles: "/titles",
  // SideBar - Organization
  OrganizationChart: "/organization-chart",
  Teams: "/teams",
  SeatMap: "/seat-map",
  Events: "/events",
  // SideBar - Evaluation Management
  EvaluationTemplateManage: "/evaluation-form-templates",
  Evaluations: "/evaluations",
  // SideBar - Leave Management
  LeaveManage: "/leaves",
  LeaveReports: "/leave-reports",
  LeaveTypes: "/leave-types",
  BonusLeaves: "/bonus-leaves",
  // SideBar - WFH Managemen
  WFHManage: "/workfromhome",
  // SiderBar - Lunch Management
  LunchCalendar: "/lunches",
  LunchSchedules: "/lunch-schedules",
  LunchProviders: "/lunch-providers",
  LunchBookings: "/lunch-bookings",
  //SiderBar - Elearning
  Courses: "/courses",
  CourseCreate: "/courses/new-course",
  CourseDetail: "courses/:id",
  CourseEdit: "courses/:id/edit",
  Topics: "/topics",
  MyAssignments: "/my-assignments", // SideBar Settings
  AssingnmentUser: "my-assignments/:id",
  IntegratedApplication: "/setting/integrated-application",
  Office: "/setting/offices",
  ManageRole: "/roles",

  // ROUTER
  Page404: "*",
  Login: "/login",
  LoggedInLayout: "",
  ResetPassword: "/resetPassword",
  ChangePassword: "/changepassword",
  Verify: "/verify",
  // Profile
  Profile: "/profile/:id",
  // Team
  TeamDetail: "/teams/:id",
  CreateTeam: "/create-team",
  AddMember: "/addMember/:id",
  ImportFromExcel: "/import-from-excel",
  // Evaluation
  NewEvaluation: "/evaluations/new",
  EvaluationImportExcel: "/evaluations/import",
  EvaluationDetail: "/evaluations/:id",
  // Leave's children
  MyRequest: "/",
  AddNewRequest: "new-request",
  RequestApproval: "approvals",
  OfficeRequest: "office-requests",
  // Leave-Report's children
  MyReport: "/",
  MyTeamReport: "my-team",
  OfficeReport: "offices",
  // LeaveType's children
  LeaveTypesChild: "/",
  LeaveTypeGroups: "leave-type-groups",
  // LeaveBonus's children
  BonusLeave: "/",
  BonusType: "bonus-types",
  // EvaluationTemplateManage 's children
  MyEvaluationTemplate: "/",
  EvaluationTemplateFormType: "evaluation-templates-types",
  AddNewEvaluationTemplate: "new-evaluation-form-template",
  EditEvaluationTemplate: ":id",
  // WFH 's children
  WFHRequest: "/",
  AddNewWFHRequest: "new-request",
  WFHOfficeRequest: "wfh-office-requests",
  // Skill 's children
  SearchSkill: "/",
  ReportSkill: "reports",
  LevelSkill: "levels",
  DefinitionSkill: "definitions",
  PositionSkill: "position",
  // OfficeInformation
  OfficeInformation: "/setting/offices/:id",
  // Course Management
  DetailLesson: "/lessons/:id",
  assignments: "/assignments",
  QuizDetail: "quiz/:quizId",
};
