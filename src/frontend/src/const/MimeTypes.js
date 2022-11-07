const MIMETYPES = {
  videos: [
    "video/x-msvideo",
    "video/mp4",
    "video/mpeg",
    "video/ogg",
    "video/mp2t",
    "video/webm",
    "video/3gpp",
    "video/3gpp2",
  ],
  pdfs: ["application/pdf"],
  words: [
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ],
  powerpoints: [
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
  ],
};
const ACCEPTEDTYPES =
  ".docx, .ppt, .pptx, .pdf, .mp4, .mpeg, .ogg, .mp2t, .webm, .video/3gpp, .video/3gpp2, ";

const MIMETYPE_ICONS = {
  videos: "video-icon.svg",
  pdfs: "pdf-icon.svg",
  words: "word-icon.svg",
  powerpoints: "powerpoint-icon.svg",
};

export { MIMETYPES, ACCEPTEDTYPES, MIMETYPE_ICONS };
