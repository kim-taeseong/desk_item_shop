from django.db import models
from uuid import uuid4
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
import logging
from order.models import Order
import requests

User = get_user_model()
logger = logging.getLogger("toss_payment")

class Payment(models.Model):
    uid = models.UUIDField(default=uuid4, editable=False)

    @property
    def merchant_uid(self):
        return self.uid

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    
    STATUS_CHOICES = (
        ("ready", "미결제"),
        ("paid", "결제 완료"),
        ("cancelled", "결제 취소"),
        ("failed", "결제 실패"),
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="ready", db_index=True
    )
    
    def get_status_display(self):
        status_display = {
            "ready": "미결제",
            "paid": "결제 완료",
            "cancelled": "결제 취소",
            "failed": "결제 실패"
        }
        return status_display.get(self.status)
    
    is_paid = models.BooleanField(default=False, db_index=True)
    
    def verify(self, commit=True):
        # Toss Payments API를 사용하여 결제 정보를 확인하는 로직
        url = f"https://api.tosspayments.com/v1/payments/{self.merchant_uid}"
        headers = {
            "Authorization": f"Basic {settings.TOSS_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response_data = response.json()
            
            if response.status_code != 200:
                raise ValueError(response_data.get('message', 'Unknown error'))
            
            self.status = response_data['status']
            self.is_paid = response_data['status'] == 'paid' and response_data['amount'] == self.amount
            if commit:
                self.save()
        except Exception as e:
            logger.error(str(e), exc_info=e)
            raise Http404(str(e))

    created_at = models.DateTimeField(auto_now_add=True)

