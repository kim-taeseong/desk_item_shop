from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # 기본 요구 사항 검사
        if len(password) < 8 or len(password) > 12:
            raise ValidationError(_('비밀번호는 8자 이상 12자 이하여야 합니다.'))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('비밀번호는 적어도 하나의 숫자를 포함해야 합니다.'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('비밀번호는 적어도 하나의 대문자를 포함해야 합니다.'))
        if not any(char.islower() for char in password):
            raise ValidationError(_('비밀번호는 적어도 하나의 소문자를 포함해야 합니다.'))

        # 연속되는 숫자 검사
        for i in range(len(password) - 2):
            if password[i].isdigit() and password[i+1].isdigit() and password[i+2].isdigit():
                if int(password[i+1]) == int(password[i]) + 1 and int(password[i+2]) == int(password[i]) + 2:
                    raise ValidationError(_('비밀번호는 연속되는 숫자를 포함할 수 없습니다.'))

    def get_help_text(self):
        return _('비밀번호는 8자 이상 12자 이하이며, 대문자, 소문자, 숫자를 각각 적어도 하나씩 포함해야 하며, 연속되는 숫자를 포함할 수 없습니다.')
