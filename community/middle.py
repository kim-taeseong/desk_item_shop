from django.utils.deprecation import MiddlewareMixin

class SaveBodyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST':
            # 본문 데이터를 읽어서 속성에 저장
            request._body_saved = request.body