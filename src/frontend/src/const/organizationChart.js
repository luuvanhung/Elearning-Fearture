import env from "../../env";

const ORG_TYPES = {
  group: {
    name: "group",
    background_color: "#fbeaeb",
    color: "#2e3c7e",
  },
  office: {
    name: "office",
    background_color: "#f2edd7",
    color: "#755139",
  },
  department: {
    name: "department",
    background_color: "#BDFFF6",
    color: "#E23C52",
  },
  team: {
    name: "team",
    background_color: "#9cc3d5",
    color: "#2163b2",
  },
  member: {
    name: "member",
    background_color: "#dce2f0",
    color: "#50586c",
  },
  floating_users: {
    name: "floating_users",
    background_color: "#ebebde",
    color: "#777764",
  },
};

const PATH_STOKE_COLOR = "#000";
const PATH_STOKE_WIDTH = "1px";
const PATH_FILL = "none";

const API_IMAGE_SRC = env.VUE_APP_API_URL
  ? `${env.VUE_APP_API_URL}/files`
  : "/api/v1/files";

export {
  ORG_TYPES,
  API_IMAGE_SRC,
  PATH_STOKE_COLOR,
  PATH_STOKE_WIDTH,
  PATH_FILL,
};
