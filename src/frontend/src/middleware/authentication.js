import { accessToken } from "@/helper/accessToken";

export default function ({ redirect }) {
  // If the user is not authenticated
  if (accessToken() === undefined) {
    redirect("/login");
  }
}
