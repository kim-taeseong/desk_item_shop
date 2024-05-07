from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
from django.apps import apps

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        User = apps.get_model('users', 'User')  # User 모델

        # 비활성화된 시점으로부터 지정한 시간 후에 계정을 삭제하는 함수
        def delete_inactive_users():
            delete_time = timezone.now() - timedelta(minutes=10) # 시간 지정
            # 비활성화한 시간이 지정한 시간보다 오래된 계정을 삭제
            User.objects.filter(is_active=False, deactivetime__lte=delete_time).delete()

        if not hasattr(self, 'scheduler'):
            self.scheduler = BackgroundScheduler()
            self.scheduler.add_job(delete_inactive_users, 'interval', hours=24)  # 매일 실행
            self.scheduler.start()
