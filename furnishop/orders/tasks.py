from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from orders.models import Order

"""
send_order_confirmation_email task უგზავნის ელფოსტას მომხმარებელს მას შემდეგ, რაც შეკვეთა შეიქმნება. 
ამას აკეთებს კონკრეტული შეკვეთის ID-ის მიხედვით
@shared_task-ით Celery-ს ვეუბნებით, რომ ეს ფუნქცია შეიძლება ასინქრონულად გაეშვას
"""


@shared_task
def send_order_confirmation_email(order_id):
    """
    Sends an order confirmation email to the user after the order is created.
    """
    try:
        order = Order.objects.get(id=order_id)  # ვეძებთ იმ შეკვეთას, რომელიც შეიქმნა
        user = order.user  # ამ შეკვეთიდან ვიღებთ მომხმარებელს (რომელმაც შეავსო)

        subject = f"Order Confirmation #{order.order_number}"  # ელფოსტის სათაური
        """
        message არის ელფოსტის ძირითადი ტექსტი, მასში ვწერ შეკვეთის ინფორმაციას: 
        მომხმარებლის სახელი, შეკვეთის ნომერი, თანხა, მისამართი და ა.შ.
        """
        message = (
            f"Hello {user.first_name} {user.last_name},\n\n"
            f"Your order has been successfully received and is being processed.\n\n"
            f"Order Number: {order.order_number}\n"
            f"Total Amount: {order.total_amount} ₾\n"
            f"Shipping Address: {order.shipping_address}\n\n"
            f"Thank you for shopping with FurniShop!"
        )

        """
        send_mail უშუალოდ აგზავნის ელფოსტას. settings.DEFAULT_FROM_EMAIL — გამგზავნის ელფოსტა
        [user.email] — მომხმარებელის ელფოსტა
        fail_silently=False — თუ შეცდომაა, შეცდომა გამოისროლოს
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        # თუ ყველაფერი წარმატებით გაიარა, ვაბრუნებ ტექსტს, რომელიც ჩაწერილი იქნება Celery-ის worker-ის ლოგში
        return f"Order confirmation email sent to {user.email}"

    # თუ ასეთი შეკვეთა საერთოდ არ არსებობს, უბრალოდ ვაბრუნებ შეცდომის მესიჯს
    except Order.DoesNotExist:
        return f"Order with id={order_id} not found"

# მომხმარებლის მიერ შეკვეთის გაკეთებიდან 1 წუთში შეკვეთის სტატუსი ავტომატურად გახდება Processing.
# ეს ტასკი განსაზღვრავს, რომელი ორდერები უნდა განახლდეს
@shared_task
def update_order_status():
    """
    Automatically changes the order status from Pending → Processing after 1 minute.
    """
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    pending_orders = Order.objects.filter(status=1, created_at__lte=one_minute_ago)

    updated_count = pending_orders.update(status=2)  # 2 = Processing (choices მიხედვით 2-ია)

    return f"Updated {updated_count} pending orders to 'Processing' (after 1 minute)"

