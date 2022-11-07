import $ from "jquery";
import { accessToken } from "@/helper/accessToken";

/**
 * Check access permission to auth routes
 */
export function checkAccessMiddleware(to, from, next) {
  const isAuthRoute = accessToken();
  if (to.name == "Verify" || to.name == "ResetPassword") return next();
  if (to.name !== "Login" && !isAuthRoute) return next({ name: "Login" });
  return next();
}

export function setPageTitleMiddleware(to, from, next) {
  window.document.title = "Paradox";
  next();
}

//Todo: Re design home page to remote this midleware
/**
 * responsive midle ware
 */
export function responsiveMiddleware(to, from, next) {
  if (
    to.name === "Login" ||
    to.name === "Index" ||
    to.name === "Verify" ||
    to.name === "ResetPassword"
  ) {
    $("#content-area").removeClass("nav-menu-active");
  } else if (window.innerWidth >= 768) {
    $("#content-area").addClass("nav-menu-active");
  } else if ($(".nav-menu").length > 0 && $(".nav-menu").hasClass("d-none")) {
    $("#content-area").removeClass("nav-menu-active");
  }
  next();
}
