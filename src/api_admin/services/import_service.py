import re
from datetime import datetime

import pandas
from api_base.services import BaseService
from api_user.models import User
from common.constants.workday_constants import Workday
from rest_framework.exceptions import ValidationError


class ExcelImportService(BaseService):
    """
    CHECK IMPORT METHOD
    """

    def __init__(self):
        self.rows = []
        self.valid_email = []
        self.invalid_email = []
        self.current_row = None
        self.status = []
        self.email = None
        self.name = None
        self.phone = None
        self.join_date = None
        self.remain_leave = None

    def check_import(self, df):
        email_regex = r"^[a-z][a-z0-9_\\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}$"
        email_col = "email"
        name_col = "name"
        phone_col = "phone"
        join_date_col = "join date"
        remain_leave_col = "remain leave"

        for i in df.index:
            self.phone = str(int(df[phone_col][i]))
            self.current_row = str(i + 2)
            self.email = str(df[email_col][i])
            self.name = str(df[name_col][i])
            self.join_date = '{:%Y-%m-%d}'.format(datetime.strptime(str(df[join_date_col][i]), '%Y-%m-%d %H:%M:%S'))
            self.remain_leave = str(df[remain_leave_col][i])

            if re.search("^\\d{9,11}$", str(int(df[phone_col][i]))):
                self.phone = self.reformat_phone(str(int(df[phone_col][i])))

            if not self.check_name(self.name):
                self.status.append("Invalid name")
                self.append_status(email_list=self.invalid_email, success=False)
                continue
            self.name = self.name.strip()

            if not self.check_join_date(self.join_date):
                self.status.append("Join date should be '%y-%m-%d'")
                self.append_status(email_list=self.invalid_email, success=False)
                continue

            if not self.check_remain_leave(self.remain_leave):
                self.status.append("Invalid remain leave")
                self.append_status(email_list=self.invalid_email, success=False)
                continue

            if not (re.search(email_regex, self.email)):
                self.status.append("Invalid email format")
                self.append_status(email_list=self.invalid_email, success=False)
                continue
            existed = User.objects.filter(email=self.email).count()
            if existed:
                self.status.append("Already existed")
                self.append_status(email_list=self.invalid_email, success=False)
                continue
            if self.email in self.valid_email:
                self.status.append("Duplicate in file")
                self.append_status(email_list=self.invalid_email, success=False)
                continue

            if not re.search("^\\d{9,11}$", str(int(df[phone_col][i]))):
                self.status.append("Invalid phone format")
                self.append_status(email_list=self.invalid_email, success=False)
                continue

            self.status.append("Valid email")
            self.append_status(email_list=self.valid_email, success=True)

        return {
            "rows": self.rows,
            "valid": self.valid_email,
            "invalid": self.invalid_email,
        }

    def append_status(self, email_list, success):
        email_list.append(self.email)
        self.rows.append(
            {
                "row": self.current_row,
                "email": self.email,
                "name": self.name,
                "phone": self.phone,
                "status": self.status,
                "join_date": self.join_date,
                "remain_leave": self.remain_leave,
                "success": success,
            }
        )
        self.status = []

    @staticmethod
    def read_excel(file):
        try:
            return pandas.read_excel(file, engine="openpyxl")
        except Exception:
            raise ValidationError("Input file is not valid")

    @classmethod
    def check_join_date(cls, join_date_str: str):
        try:
            return bool(datetime.strptime(join_date_str, '%Y-%m-%d'))
        except ValueError:
            return False

    @classmethod
    def check_remain_leave(cls, remain_leave: str):
        try:
            remain_leave = float(remain_leave)
            return Workday.MAX_REMAIN_DAY > remain_leave >= 0 and remain_leave % 0.5 == 0
        except ValueError:
            return False

    @classmethod
    def reformat_phone(cls, phone: str):
        return '0' + phone if not re.search(r"(84|0)+([0-9]{9})\b", phone) else phone

    @classmethod
    def check_name(cls, name: str) -> bool:
        return isinstance(name, str) and name.strip() != ""
