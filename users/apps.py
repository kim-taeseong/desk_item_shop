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

        # 비활성화된 시점으로부터 7일 후에 계정을 삭제
        def delete_inactive_users():
            delete_time = timezone.now() - timedelta(minutes=5) # 원래 7일이지만 현재 테스트를 위해서 5분 후 계정을 삭제
            
            # deactivetime이 지정한 시간보다 오래된 계정을 삭제
            User.objects.filter(is_active=False, deactivetime__lte=delete_time).delete()

        # 스케줄러 생성
        if not hasattr(self, 'scheduler'):
            self.scheduler = BackgroundScheduler() # APScheduler 라이브러리에서 제공하는 스케줄러 클래스
            self.scheduler.add_job(delete_inactive_users, 'interval', minutes=1)  # 현재 테스트를 위해서 1분간격으로 실행
            self.scheduler.start() # 스케줄러 시작