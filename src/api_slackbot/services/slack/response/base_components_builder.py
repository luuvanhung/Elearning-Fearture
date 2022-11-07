import json

from common.constants.slack_constants.dialog_content import RequestDialogContent
from common.constants.workday_constants import Workday


class BaseComponentsBuilder:
    def __init__(self):
        self.interactive_response_dto = []
        self.sub_component_builder = SubComponentBuilder()

    def create_header_text(self, text: str):
        self.interactive_response_dto.append(
            self.sub_component_builder.header_builder(text)
        )
        return self

    def create_mrkdwn_text(self, text: str):
        self.interactive_response_dto.append(
            self.sub_component_builder.section_mrkdwn_text_builder(mrkdwn_text=text)
        )
        return self

    def create_actions_section(self, action_elements: list):
        self.interactive_response_dto.append(
            {
                "type": "actions",
                "elements": [action_element for action_element in action_elements],
            }
        )
        return self

    def create_accessory_section(self, section_title: str, accessory: dict):
        self.interactive_response_dto.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": section_title,
                },
                "accessory": accessory,
            }
        )
        return self

    def create_button(
        self,
        button_data: dict,
        button_values: dict,
        action_id_data: dict,
        confirm_data: dict = None,
    ):
        return self.sub_component_builder.button_builder(
            buttons={
                "text": button_data["text"],
                "style": button_data["style"],
                "values": json.dumps(button_values),
                "action_id": json.dumps(action_id_data),
            },
            confirm_text_info=confirm_data,
        )

    @staticmethod
    def get_from_time_by_date_off_type(date_off_type):
        if date_off_type in [Workday.FULL, Workday.MORNING_SHIFT_TIME]:
            return "08:00"
        elif date_off_type == Workday.AFTERNOON_SHIFT_TIME:
            return "13:30"

    @staticmethod
    def get_to_time_by_date_off_type(date_off_type):
        if date_off_type in [Workday.FULL, Workday.AFTERNOON_SHIFT_TIME]:
            return "17:30"
        elif date_off_type == Workday.MORNING_SHIFT_TIME:
            return "12:00"

    def get_response_dto(self):
        return self.interactive_response_dto


class SubComponentBuilder:
    @staticmethod
    def mrkdwn_text_builder(mrkdwn_text):
        return {"type": "mrkdwn", "text": mrkdwn_text}

    @staticmethod
    def plain_text_builder(plain_text):
        return {"type": "plain_text", "text": plain_text, "emoji": True}

    def section_plain_text_builder(self, plain_text):
        return {
            "type": "section",
            "text": self.plain_text_builder(plain_text=plain_text),
        }

    def section_mrkdwn_text_builder(self, mrkdwn_text):
        return {
            "type": "section",
            "text": self.mrkdwn_text_builder(mrkdwn_text=mrkdwn_text),
        }

    def confirm_action_builder(self, confirm_text_info):
        return {
            "title": self.plain_text_builder(plain_text=confirm_text_info.get("title")),
            "text": self.mrkdwn_text_builder(mrkdwn_text=confirm_text_info.get("text")),
            "confirm": self.plain_text_builder(
                plain_text=confirm_text_info.get("confirm")
            ),
            "deny": self.plain_text_builder(plain_text=confirm_text_info.get("deny")),
        }

    def button_builder(self, buttons, confirm_text_info):
        if confirm_text_info is not None:
            return {
                "type": "button",
                "text": self.plain_text_builder(plain_text=buttons.get("text")),
                "style": buttons.get("style"),
                "value": buttons.get("values"),
                "action_id": buttons.get("action_id"),
                "confirm": self.confirm_action_builder(confirm_text_info),
            }
        else:
            return {
                "type": "button",
                "text": self.plain_text_builder(plain_text=buttons.get("text")),
                "style": buttons.get("style"),
                "value": buttons.get("values"),
                "action_id": buttons.get("action_id"),
            }

    def static_select_builder(
        self,
        action_id,
        selections,
        place_holder=RequestDialogContent.DEFAULT_PLACEHOLDER,
        initial_option=None,
    ):
        static_select_schema = {
            "type": "static_select",
            "placeholder": self.plain_text_builder(place_holder),
            "options": [
                {
                    "text": self.plain_text_builder(plain_text=selection.get("text")),
                    "value": str(selection.get("value")),
                }
                for selection in selections
            ],
            "action_id": action_id,
        }

        if initial_option is not None:
            static_select_schema["initial_option"] = {
                "value": initial_option.get("value"),
                "text": self.plain_text_builder(initial_option.get("text")),
            }
        return static_select_schema

    def date_picker_builder(self, initial_date: str, place_holder, action_id):
        """
        initial_date: YYYY-MM-DD
        """
        return {
            "type": "datepicker",
            "initial_date": initial_date,
            "placeholder": self.plain_text_builder(place_holder),
            "action_id": action_id,
        }

    def checkboxes_builder(self, action_id, options, initial_option=None):
        checkbox_schema = {
            "type": "checkboxes",
            "options": [
                {
                    "text": self.mrkdwn_text_builder(mrkdwn_text=option.get("text")),
                    "description": self.mrkdwn_text_builder(
                        mrkdwn_text=option.get("description")
                    ),
                    "value": option.get("value"),
                }
                for option in options
            ],
            "action_id": action_id,
        }
        if initial_option is not None:
            checkbox_schema["initial_option"] = initial_option

        return checkbox_schema

    def plain_input_builder(
        self,
        action_id,
        label,
        place_holder=RequestDialogContent.DEFAULT_PLACEHOLDER,
        initial_value=None,
        trigger_actions_on=None,
    ):
        plain_input_schema = {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "placeholder": self.plain_text_builder(plain_text=place_holder),
                "action_id": action_id,
            },
            "label": self.plain_text_builder(plain_text=label),
        }
        if trigger_actions_on is not None:
            plain_input_schema["dispatch_action"] = True
            plain_input_schema["element"].update(
                {
                    "dispatch_action_config": {
                        "trigger_actions_on": [trigger_actions_on]
                    },
                }
            )
        if initial_value is not None:
            plain_input_schema["element"].update({"initial_value": initial_value})
        return plain_input_schema

    def header_builder(self, text):
        return {"type": "header", "text": self.plain_text_builder(plain_text=text)}

    @staticmethod
    def divider_builder():
        return {"type": "divider"}
