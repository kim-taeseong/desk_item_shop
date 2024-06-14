from django.db import models
from users.models import Customer, Store

class UserFavoriteStore(models.Model):
    customer = models.ForeignKey(Customer, related_name='favorites', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'store')
