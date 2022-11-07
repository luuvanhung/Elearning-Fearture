import { accessToken } from "@/helper/accessToken";

export default function ({ redirect }) {
  if (accessToken()) {
    redirect("/");
  }
}
