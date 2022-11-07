from api_base.services.sendmail import SendMail
from django.conf import settings
from django.template.loader import render_to_string


class SendMailRequestOff:
    url_logo = "http://{}:{}/static/paradoxlogo.png".format(
        settings.API_HOST, settings.API_PORT
    )

    @classmethod
    def send_request(cls, leave_type, name_admin, name_user, list_email, date_off=None):
        content = render_to_string(
            "../templates/request_off.html",
            {
                "name_admin": name_admin,
                "name_user": name_user,
                "date_off": date_off,
                "link": settings.URL_WEB_INTERNAL,
                "leave_type": leave_type,
                "logo": cls.url_logo,
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Leave Request (Insurance)"
            SendMail.start([settings.DEFAULT_EMAIL_ADMIN], title, content)
            return
        else:
            title = "Leave Request"

        SendMail.start(list_email, title, content)

    @classmethod
    def send_forward_request(
        cls, name_admin, name_admin_manage, name_user, email, date_off=None
    ):
        content_user = render_to_string(
            "../templates/forward_request_off.html",
            {
                "name_admin": name_admin,
                "name_user": name_user,
                "name_admin_manage": name_admin_manage,
                "logo": cls.url_logo,
            },
        )

        content_manage = render_to_string(
            "../templates/forward_request_off_to_manage.html",
            {
                "name_admin": name_admin,
                "name_user": name_user,
                "name_admin_manage": name_admin_manage,
                "date_off": date_off,
                "link": settings.URL_WEB_INTERNAL,
                "logo": cls.url_logo,
            },
        )
        title = "Forward Leave Request"
        SendMail.start(email["user"], title, content_user)
        SendMail.start(email["admin"], title, content_manage)

    @classmethod
    def send_reject_request(
        cls, leave_type, name_user, name_admin, reason, list_email, date_offs=None
    ):
        content = render_to_string(
            "../templates/reject_request_off.html",
            {
                "name_admin": name_admin,
                "name_user": name_user,
                "date_offs": date_offs,
                "reason": reason,
                "logo": cls.url_logo,
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Reject Leave Request(Insurance)"
        else:
            title = "Reject Leave Request"
        SendMail.start(list_email, title, content)

    @classmethod
    def send_reject_request_to_manage(
            cls, leave_type, name_user, name_admin, choosed_approver, list_email, date_offs=None
    ):
        content = render_to_string(
            "../templates/reject_request_off_to_manage.html",
            {
                "name_admin": name_admin,
                "name_user": name_user,
                "choosed_approver": choosed_approver,
                "date_offs": date_offs,
                "logo": cls.url_logo,
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Reject Leave Request(Insurance)"
        else:
            title = "Reject Leave Request"
        SendMail.start(list_email, title, content)

    @classmethod
    def send_approve_request_to_user(
        cls, leave_type, name_user, name_admin, list_email, date_off=None
    ):
        content = render_to_string(
            "../templates/approve_request_off.html",
            {
                "name_admin": name_admin,
                "name_user": name_user,
                "date_off": date_off,
                "leave_type": leave_type,
                "logo": cls.url_logo,
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Approve off (Insurance)"
        else:
            title = "Approve Leave Request"

        SendMail.start(list_email, title, content)

    @classmethod
    def send_approve_request_to_manage(
        cls, leave_type, name_user, name_admin, choosed_approver, email_user, list_email, date_offs=None
    ):
        content = render_to_string(
            "../templates/leave_notice.html",
            {
                "name_user": name_user,
                "name_admin": name_admin,
                "choosed_approver": choosed_approver,
                "email_user": email_user,
                "date_offs": date_offs,
                "leave_type": leave_type,
                "logo": cls.url_logo,
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Approve off (Insurance)"
        else:
            title = "Approve Leave Request"

        SendMail.start(list_email, title, content)

    @classmethod
    def send_cancel_request(
            cls, leave_type, name_user, choosed_approver, list_email, date_offs=None
    ):
        content = render_to_string(
            "../templates/cancel_notice.html",
            {
                "name_user": name_user,
                "choosed_approver": choosed_approver,
                "date_offs": date_offs,
                "leave_type": leave_type,
                "logo": cls.url_logo,
                "link": f"{settings.URL_WEB_INTERNAL}",
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Cancel Leave Request (Insurance)"
        else:
            title = "Cancel Leave Request"
        SendMail.start(list_email, title, content)

    @classmethod
    def send_approve_cancel_request_to_user(
            cls, leave_type, name_user, name_admin, list_email, date_offs=None
    ):
        content = render_to_string(
            "../templates/approve_cancel_request_off.html",
            {
                "name_user": name_user,
                "date_offs": date_offs,
                "name_admin": name_admin,
                "leave_type": leave_type,
                "logo": cls.url_logo,
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Approve Cancel Leave Request (Insurance)"
        else:
            title = "Approve Cancel Leave Request"
        SendMail.start(list_email, title, content)

    @classmethod
    def send_approve_cancel_request_to_manage(
            cls, leave_type, name_user, name_admin, choosed_approver, list_email, date_offs=None
    ):
        content = render_to_string(
            "../templates/approve_cancel_request_off_to_manage.html",
            {
                "name_user": name_user,
                "date_offs": date_offs,
                "name_admin": name_admin,
                "choosed_approver": choosed_approver,
                "leave_type": leave_type,
                "logo": cls.url_logo,
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Approve Cancel Leave Request (Insurance)"
        else:
            title = "Approve Cancel Leave Request"
        SendMail.start(list_email, title, content)

    @classmethod
    def send_reject_cancel_request_to_user(
            cls, leave_type, name_user, name_admin, list_email, date_offs=None
    ):
        content = render_to_string(
            "../templates/reject_cancel_request_off.html",
            {
                "name_admin": name_admin,
                "name_user": name_user,
                "date_offs": date_offs,
                "leave_type": leave_type,
                "logo": cls.url_logo
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Reject Cancel Leave Request (Insurance)"
        else:
            title = "Reject Cancel Leave Request"
        SendMail.start(list_email, title, content)

    @classmethod
    def send_reject_cancel_request_to_manage(
            cls, leave_type, name_user, name_admin, choosed_approver, list_email, date_offs=None
    ):
        content = render_to_string(
            "../templates/reject_cancel_request_off_to_manage.html",
            {
                "name_admin": name_admin,
                "name_user": name_user,
                "choosed_approver": choosed_approver,
                "date_offs": date_offs,
                "leave_type": leave_type,
                "logo": cls.url_logo
            },
        )
        if leave_type.leave_type_group.is_insurance_pay:
            title = "Reject Cancel Leave Request (Insurance)"
        else:
            title = "Reject Cancel Leave Request"
        SendMail.start(list_email, title, content)
