from .exception_message_builder import slack_exception_message_builder


class ExceptionHandler:
    def __init__(self, error="", exception_engine=None):
        self.error = error
        self.exception_engine = exception_engine
        self.error_exception_blocks = slack_exception_message_builder(error)

    def default_exception_when_creating_request(
        self,
        profile_id=None,
        from_date=None,
        from_time=None,
        temp_leave_request_id=None,
    ):
        if temp_leave_request_id is not None:
            return (
                self.exception_engine.send_exception_blocks(self.error_exception_blocks)
                .call_delete_temp_request_by_id_service(temp_leave_request_id)
                .return_http_no_retires_response(self.error)
            )
        else:
            return (
                self.exception_engine.send_exception_blocks(self.error_exception_blocks)
                .call_delete_temp_request_by_profile_id_and_from_datetime_service(
                    profile_id=profile_id,
                    from_date=from_date,
                    from_time=from_time,
                )
                .return_http_no_retires_response(str(self.error))
            )

    def line_manager_action_exception(self):
        return self.exception_engine.send_exception_blocks(
            self.error_exception_blocks
        ).return_http_no_retires_response(str(self.error))

    def exception_when_sending_slack_notification(self):
        self.exception_engine.send_message(self.error_exception_blocks)

    def exception_when_call_canceling_request(self):
        return self.exception_engine.send_exception_blocks(
            self.error_exception_blocks
        ).return_http_no_retires_response(self.error)
