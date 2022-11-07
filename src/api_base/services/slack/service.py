from slack_sdk.webhook import WebhookClient

from .base import SlackBaseService


class SlackResponseService(SlackBaseService):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    def send_ephemeral_message(self, user, text, blocks=None):
        if blocks is not None:
            self.client.chat_postEphemeral(
                channel=self.channel, user=user, text=text, blocks=blocks
            )
        else:
            self.client.chat_postEphemeral(channel=self.channel, user=user, text=text)

    def send_message(self, text, channel=None, blocks=None):
        if channel is None:
            if blocks is not None:
                self.client.chat_postMessage(
                    channel=self.channel, text=text, blocks=blocks
                )
            else:
                self.client.chat_postMessage(channel=self.channel, text=text)
        else:
            if blocks is not None:
                self.client.chat_postMessage(channel=channel, text=text, blocks=blocks)
            else:
                self.client.chat_postMessage(channel=channel, text=text)

    def upload_file(self, file, initial_comment=None):
        if initial_comment is not None:
            self.client.files_upload(
                channels=self.channel, file=file, initial_comment=initial_comment
            )
        elif initial_comment is None:
            self.client.files_upload(channels=self.channel, file=file)


class SlackWebhookService:
    def __init__(self, response_url):
        self.webhook = WebhookClient(response_url)

    def send_response_to_interacting(self, text, blocks=None):
        if blocks is not None:
            self.webhook.send(text=text, blocks=blocks)
        else:
            self.webhook.send(text=text)
        return
