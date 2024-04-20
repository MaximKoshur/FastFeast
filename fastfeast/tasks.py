from celery import Celery
import time
from .models import Order
app = Celery('fastfeast', broker='redis://redis:6379/0')


@app.task
def change_status(order_id):
    order = Order.objects.get(id=order_id)
    time.sleep(10)
    order.status = 'ONTHEWAY'
    order.save()
    time.sleep(10)
    order.status = 'DELIVERED'
    order.save()

