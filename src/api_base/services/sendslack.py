import threading

from api_base.services.slack import SlackResponseService


class SlackThread(threading.Thread):
    def __init__(
        self,
        text=None,
        channel=None,
    ):
        self.text = text
        self.channel = channel
        threading.Thread.__init__(self)

    def run(self):
        try:
            slack_response_service = SlackResponseService(channel=self.channel)
            slack_response_service.send_message(
                text=self.text,
            )
        except Exception as e:
            print(str(e))


class SendSlack:
    @staticmethod
    def start(text, channel):
        SlackThread(text=text, channel=channel).start()
