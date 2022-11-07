import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";
const VIEW_OPTIONS = {
  modules: {
    syntax: {
      highlight: (text) => hljs.highlightAuto(text).value,
    },
  },
  placeholder: "",
  theme: "snow",
  readOnly: false,
};
export { VIEW_OPTIONS };
