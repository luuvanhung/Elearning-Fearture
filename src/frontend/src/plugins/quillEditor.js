import Vue from "vue";
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";
import quillEditor from "vue-quill-editor";
import Quill from "quill";
import { ImageDrop } from "quill-image-drop-module";
import ImageResize from "quill-image-resize-vue";
import VideoResize from "quill-video-resize-module";
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";
import "quill/dist/quill.bubble.css";

let BaseImageFormat = Quill.import("formats/image");
let BaseVideoFormat = Quill.import("formats/video");
const ImageFormatAttributesList = ["alt", "height", "width", "style"];
class ImageFormat extends BaseImageFormat {
  static formats(domNode) {
    return ImageFormatAttributesList.reduce(function (formats, attribute) {
      if (domNode.hasAttribute(attribute)) {
        formats[attribute] = domNode.getAttribute(attribute);
      }
      return formats;
    }, {});
  }
  format(name, value) {
    if (ImageFormatAttributesList.indexOf(name) > -1) {
      if (value) {
        this.domNode.setAttribute(name, value);
      } else {
        this.domNode.removeAttribute(name);
      }
    } else {
      super.format(name, value);
    }
  }
}
class VideoFormat extends BaseVideoFormat {
  static formats(domNode) {
    return ImageFormatAttributesList.reduce(function (formats, attribute) {
      if (domNode.hasAttribute(attribute)) {
        formats[attribute] = domNode.getAttribute(attribute);
      }
      return formats;
    }, {});
  }
  format(name, value) {
    if (ImageFormatAttributesList.indexOf(name) > -1) {
      if (value) {
        this.domNode.setAttribute(name, value);
      } else {
        this.domNode.removeAttribute(name);
      }
    } else {
      super.format(name, value);
    }
  }
}
Quill.register(ImageFormat, true);
Quill.register(VideoFormat, true);

Quill.register("modules/imageDrop", ImageDrop);
Quill.register("modules/imageResize", ImageResize);
Quill.register("modules/videoResize", VideoResize);
const toolbarOptions = [
  ["bold", "italic", "underline", "strike"], // toggled buttons
  ["blockquote", "code-block"],

  [{ header: 1 }, { header: 2 }], // custom button values
  [{ list: "ordered" }, { list: "bullet" }],
  [{ script: "sub" }, { script: "super" }], // superscript/subscript
  [{ indent: "-1" }, { indent: "+1" }], // outdent/indent
  [{ direction: "rtl" }], // text direction

  [{ size: ["small", false, "large", "huge"] }], // custom dropdown
  [{ header: [1, 2, 3, 4, 5, 6, false] }],
  ["link", "image", "video"],
  [{ color: [] }, { background: [] }], // dropdown with defaults from theme
  [{ font: [] }],
  [{ align: [] }],

  ["clean"], // remove formatting button
];
const quill = {
  modules: {
    syntax: {
      highlight: (text) => hljs.highlightAuto(text).value,
    },
    toolbar: toolbarOptions,
    imageResize: {
      displaySize: true,
      readOnly: false,
    },
    imageDrop: true,
    videoResize: {
      modules: ["Resize", "DisplaySize", "Toolbar"],
      handleStyles: {
        backgroundColor: "black",
        border: "none",
        color: "white",
      },
      displayStyles: {
        backgroundColor: "black",
        border: "none",
        color: "white",
      },
      toolbarStyles: {
        backgroundColor: "black",
        border: "none",
        color: "white",
      },
    },
  },
  placeholder: "",
  theme: "snow",
  readOnly: false,
};

Vue.use(quillEditor, quill);
