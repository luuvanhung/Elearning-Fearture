from common.constants.wit_constants import WitEntities
from common.constants.workday_constants import Workday
from utils.datetime_utils import (
    date_string_to_datetime,
    datetime_to_string,
    get_current_date,
    minus_date,
    plus_date,
)


class BaseParser:
    intents_data_transfer_object = {}

    def __init__(self, wit_response):
        self.wit_response = wit_response
        self.intents = self.wit_response.get("intents")[0]
        self.entities = self.wit_response.get("entities")

    def get_text(self):
        self.intents_data_transfer_object["text"] = self.wit_response.get("text")
        return self

    def get_sentence_intent(self, intent_name):
        self.intents_data_transfer_object["user_intent"] = intent_name
        return self

    def get_date_time(self):
        if self.entities.get(WitEntities.WIT_DATETIME):
            self.process_wit_datetime()
        elif self.entities.get(WitEntities.WIT_DURATION):
            self.process_wit_duration()
        else:
            self.process_no_datetime_predicted()
        return self

    @staticmethod
    def get_date_from_wit_datetime(wit_date_time):
        return wit_date_time[: wit_date_time.find("T")]

    def process_wit_datetime(self):
        # If wit response more than 2 datetime milestone and no one is relevant to others
        # ex: "I will off today and tomorrow"

        if len(self.entities[WitEntities.WIT_DATETIME]) > 1 and (
            self.entities[WitEntities.WIT_DATETIME][0].get("from") is None
            or self.entities[WitEntities.WIT_DATETIME][
                len(self.entities[WitEntities.WIT_DATETIME]) - 1
            ].get("from")
            is None
        ):
            first_date_value = self.get_date_from_wit_datetime(
                self.entities[WitEntities.WIT_DATETIME][0].get("value")
            )
            last_date_value = self.get_date_from_wit_datetime(
                self.entities[WitEntities.WIT_DATETIME][
                    len(self.entities[WitEntities.WIT_DATETIME]) - 1
                ].get("value")
            )
            """
            "wit$datetime:datetime": [
                {
                    ...
                    "body": "today",
                    "confidence": 0.xxx,
                    "type": "value",
                    "grain": "day",
                    "value": "2022-02-09T00:00:00.000+07:00",
                    "values": [...]
                },
                {
                    ...
                    "body": "tomorrow",
                    "confidence": 0.xxx,
                    "type": "value",
                    "grain": "day",
                    "value": "2022-02-10T00:00:00.000+07:00",
                    "values": [...]
                }
                ....
            ]
            """

            if date_string_to_datetime(first_date_value) < date_string_to_datetime(
                last_date_value
            ):
                self.intents_data_transfer_object["date_time"] = {
                    "type": Workday.FULL,
                    "from_date": first_date_value,
                    "from_time": Workday.DEFAULT_START_HOUR,
                    "to_date": last_date_value,
                    "to_time": Workday.DEFAULT_END_HOUR,
                }
            else:
                self.intents_data_transfer_object["date_time"] = {
                    "type": Workday.FULL,
                    "from_date": last_date_value,
                    "from_time": Workday.DEFAULT_START_HOUR,
                    "to_date": first_date_value,
                    "to_time": Workday.DEFAULT_END_HOUR,
                }

        # If user want to take many days off
        elif "from" in self.entities[WitEntities.WIT_DATETIME][0]:
            from_date = self.get_date_from_wit_datetime(
                self.entities[WitEntities.WIT_DATETIME][0].get("from").get("value")
            )

            if self.entities[WitEntities.WIT_DATETIME][0].get("to") is not None:
                # This is using for: wit detected the "to" (have the "to" param in response)
                # as example:
                # ex:"I want to off from now to friday"
                """
                "wit$datetime:datetime": [
                    {
                        ...
                        "name": "wit$datetime",
                        "body": "from now to next friday",
                        "confidence": 0.xx,
                        "from": {
                            "grain": "second",
                            "value": "2022-01-09T13:15:57.000+07:00"
                        },
                        "to": {
                            "grain": "second",
                            "value": "2022-01-15T00:00:00.000+07:00"
                        },
                        "values": [...]
                    }
                ]
                """

                to_value_of_wit_rsp = self.get_date_from_wit_datetime(
                    self.entities[WitEntities.WIT_DATETIME][0].get("to").get("value")
                )

                # Handle cases: maybe user want to create a half-day leave request
                if (
                    self.entities[WitEntities.WIT_DATETIME][0].get("to").get("grain")
                    == WitEntities.HOUR
                ):
                    # Wit does not detect morning or afternoon,
                    # so we have to check keyword in user's message.
                    # Consider to implementing a keywords' synonym collector later
                    if (
                        Workday.MORNING.lower()
                        in self.wit_response.get(WitEntities.TEXT).lower()
                    ):
                        self.intents_data_transfer_object["date_time"] = {
                            "type": Workday.MORNING,
                            "from_date": from_date,
                            "from_time": Workday.DEFAULT_START_HOUR,
                            "to_date": to_value_of_wit_rsp,
                            "to_time": Workday.DEFAULT_END_HOUR_MORNING,
                        }
                    elif (
                        Workday.AFTERNOON.lower()
                        in self.wit_response.get(WitEntities.TEXT).lower()
                    ):
                        self.intents_data_transfer_object["date_time"] = {
                            "type": Workday.AFTERNOON,
                            "from_date": from_date,
                            "from_time": Workday.DEFAULT_START_HOUR_AFTERNOON,
                            "to_date": to_value_of_wit_rsp,
                            "to_time": Workday.DEFAULT_END_HOUR,
                        }
                else:
                    # The responded value of "to" is greater 1 date than the demand of user,
                    # if the response having {"grain": "day"}, so we minus it by 1.
                    # Ex: "I will off from monday(Dec 12th,2000) to friday(Dec 16th, 2000)"
                    # but wit responses: "Dec 17th, 2000"

                    to_date = minus_date(
                        date_string=to_value_of_wit_rsp, minus_number=1
                    )
                    self.intents_data_transfer_object["date_time"] = {
                        "type": Workday.FULL,
                        "from_date": from_date,
                        "from_time": Workday.DEFAULT_START_HOUR,
                        "to_date": to_date,
                        "to_time": Workday.DEFAULT_END_HOUR,
                    }
            elif (
                self.entities[WitEntities.WIT_DATETIME][
                    len(self.entities[WitEntities.WIT_DATETIME]) - 1
                ].get("to")
                is not None
            ):
                # This else is using for situation: wit detected the "from" but
                # can't not detect the "to" (don't have the "to" param in response)
                # so it will separate 2 wit/datetime milestones into 2 entities, but it still
                # has the "to" param in the second wit/datetime as example:

                # ex message: "I will off from now to the end of month"
                """
                WIT RESPONSE :
                "wit$datetime:datetime": [
                    {
                        ...
                        "body": "from today",
                        "confidence": 0.xx,
                        "from": {
                            "grain": "day",
                            "value": "2022-01-20T00:00:00.000+07:00"
                        },
                        "values": [...]
                    },
                    {
                        ...
                        "body": "end of month",
                        "confidence": 0.xx,
                        "from": {
                            "grain": "day",
                            "value": "2022-01-21T00:00:00.000+07:00"
                        },
                        "to": {
                            "grain": "day",
                            "value": "2022-02-01T00:00:00.000+07:00"
                        },
                        "values": [...]
                    }
                ],
                """
                to_date = self.get_date_from_wit_datetime(
                    self.entities[WitEntities.WIT_DATETIME][1].get("to").get("value")
                )
                self.intents_data_transfer_object["date_time"] = {
                    "type": Workday.FULL,
                    "from_date": from_date,
                    "from_time": Workday.DEFAULT_START_HOUR,
                    "to_date": minus_date(date_string=to_date, minus_number=1),
                    "to_time": Workday.DEFAULT_END_HOUR,
                }
            else:
                # This else below is using for situation: wit detected the "from" but
                # can't not detect the "to" (don't have the "to" param in response)
                # so it will separate 2 wit/datetime milestones into 2 entities as example:
                """
                ex message: "I will be off from now to THE next friday due to my personal issues"
                                                        ^
                ________________________________________| (incorrect grammar so Wit can not detect the "to")

                WIT RESPONSE :
                "wit$datetime:datetime": [
                    {
                        ...
                        "body": "from now",
                        "confidence": 0.xx,
                        "from": {
                            "grain": "second",
                            "value": "2022-01-09T12:57:34.000+07:00"
                        },
                        "values": [...]
                    },
                    {
                        ...
                        "body": "next friday",
                        "confidence": 0.xx,
                        "value": "2022-01-14T00:00:00.000+07:00",
                        "values": [...]
                    }
                ]
                """
                to_date = self.get_date_from_wit_datetime(
                    self.entities[WitEntities.WIT_DATETIME][1].get("value")
                )

                self.intents_data_transfer_object["date_time"] = {
                    "type": Workday.FULL,
                    "from_date": from_date,
                    "from_time": Workday.DEFAULT_START_HOUR,
                    "to_date": to_date,
                    "to_time": Workday.DEFAULT_END_HOUR,
                }

        # If user want to take a day off
        # ex: I want to off today
        else:
            # ex: I want to off today"
            """
            "wit$datetime:datetime": [
                {
                    ...
                    "body": "today",
                    "confidence": 0.xx,
                    "grain": "day",
                    "value": "2022-03-01T00:00:00.000+07:00",
                    "values": [...]
                }
            ],
            """
            date = self.get_date_from_wit_datetime(
                self.entities[WitEntities.WIT_DATETIME][0].get("value")
            )

            self.intents_data_transfer_object["date_time"] = {
                "type": Workday.FULL,
                "from_date": date,
                "from_time": Workday.DEFAULT_START_HOUR,
                "to_date": date,
                "to_time": Workday.DEFAULT_END_HOUR,
            }

    def process_wit_duration(self):
        current_date = datetime_to_string(get_current_date())
        date_wit_duration_from_current_date = plus_date(
            current_date,
            self.entities[WitEntities.WIT_DURATION][0].get("value") - 1,
        )

        self.intents_data_transfer_object["date_time"] = {
            "type": Workday.FULL,
            "from_date": current_date,
            "from_time": Workday.DEFAULT_START_HOUR,
            "to_date": date_wit_duration_from_current_date,
            "to_time": Workday.DEFAULT_END_HOUR,
        }

    def process_no_datetime_predicted(self):
        current_date = datetime_to_string(get_current_date())

        self.intents_data_transfer_object["date_time"] = {
            "type": Workday.FULL,
            "from_date": current_date,
            "from_time": Workday.DEFAULT_START_HOUR,
            "to_date": current_date,
            "to_time": Workday.DEFAULT_END_HOUR,
        }
