from api_base.services.slack.base import SlackBaseService


class SlackUserInfoService(SlackBaseService):
    def get_user_email_by_slack_id(self, user_slack_id):
        response = self.client.users_info(user=user_slack_id)
        return response.data.get("user").get("profile").get("email")
