from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from HRCS.models import EmpTable


class PasswordBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            user = EmpTable.objects.get(emp_no=username)
        except EmpTable.DoesNotExist:
            raise Exception("使用者名稱錯誤")
        if check_password(password, user.user_pwd):
            return user
        raise Exception("密碼錯誤")

    def get_user(self, user_id):
        try:
            return EmpTable.objects.get(pk=user_id)
        except EmpTable.DoesNotExist:
            return None
