import env from "../../../env";

export default {
  EMAIL: "Email must be valid",
  MAX: "{_field_} may not be greater than {length} characters",
  REQUIRED: "{_field_} can not be empty",
  MESSAGE: `The domain "${env.END_MAIL}" will be added automatically if you does not specify.`,
  IMPORT_FILE_TIP:
    "Files, if you need to update, please delete the selected files first",
  FILE_REQUIRED: "Please input fields and name",
};
