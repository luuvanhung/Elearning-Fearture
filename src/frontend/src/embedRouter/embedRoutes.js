import EmbedViewer from "@/pages/lessonManagement/components/embedViewer";
export const embedRoutes = [
  {
    path: "/embed/:id",
    name: "embed",
    component: EmbedViewer,
    children: [
      {
        path: ":assignment_id/:assignment_chapter_id/:assignment_chapter_lesson_id/:assignment_chapter_lesson_attachment_id",
        name: "EmbedAssignment",
        component: EmbedViewer,
      },
    ],
  },
];
