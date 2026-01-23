from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from datetime import timedelta, date
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .models import Reservation, Equipment
from django.db import models


# ---------------------------------------------------------
# 1. CHECK OVERDUE RESERVATIONS
# ---------------------------------------------------------
def check_overdue_reservations():
    today = date.today()

    overdue_items = Reservation.objects.filter(
        returnDate__lt=today,
        reservationStatus__in=["Pending", "Approved"]
    )

    for reservation in overdue_items:
        user = reservation.userId
        equipment = reservation.equipId

        send_mail(
            subject="Overdue Equipment Notice",
            message=f"""
Hi {user.username},

This is a reminder that the following equipment is now overdue:

- Equipment: {equipment.equipName}
- Reservation ID: {reservation.reservationId}
- Quantity: {reservation.quantityBorrowed}
- Expected Return Date: {reservation.returnDate}
- Remaining Stock: {equipment.equipQuantity}

Please return it as soon as possible.

Regards,
IT Department
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email, "andreirobertpaval26@gmail.com"],
            fail_silently=False,
        )

        reservation.reservationStatus = "Overdue"
        reservation.save()


# ---------------------------------------------------------
# 2. UPCOMING RETURN REMINDERS
# ---------------------------------------------------------
def send_upcoming_return_reminders():
    today = timezone.now().date()

    reminder_schedule = {
        2: "2 days left",
        3: "3 days left",
        7: "1 week left",
    }

    for days, label in reminder_schedule.items():
        reminder_date = today + timedelta(days=days)

        reservations = Reservation.objects.filter(
            returnDate=reminder_date,
            reservationStatus="Active"
        )

        for reservation in reservations:
            user = reservation.userId
            equipment = reservation.equipId

            send_mail(
                subject=f"Equipment Return Reminder ({label})",
                message=f"""
Hi {user.username},

This is a reminder that your equipment reservation is due in {days} day(s).

Details:
- Equipment: {equipment.equipName}
- Reservation ID: {reservation.reservationId}
- Quantity: {reservation.quantityBorrowed}
- Return Date: {reservation.returnDate}

Please ensure it is returned on time.

Thanks,
IT Department
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )


# ---------------------------------------------------------
# 3. ESCALATE OVERDUE ITEMS (5 days, 10 days)
# ---------------------------------------------------------
def escalate_overdue_items():
    today = date.today()

    # Stage 1: 5 days overdue
    five_days_overdue = today - timedelta(days=5)

    overdue_5 = Reservation.objects.filter(
        returnDate__lte=five_days_overdue,
        reservationStatus="Overdue"
    )

    for reservation in overdue_5:
        user = reservation.userId
        equipment = reservation.equipId

        send_mail(
            subject="Escalation: Equipment 5 Days Overdue",
            message=f"""
Hi Admin,

The following equipment is now 5 days overdue:

User: {user.username} ({user.email})
Reservation ID: {reservation.reservationId}
Equipment: {equipment.equipName}
Quantity: {reservation.quantityBorrowed}
Original Return Date: {reservation.returnDate}

Please follow up with the user.

Regards,
Asset Management System
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["andreirobertpaval26@gmail.com"],
            fail_silently=False,
        )

    # Stage 2: 10 days overdue
    ten_days_overdue = today - timedelta(days=10)

    overdue_10 = Reservation.objects.filter(
        returnDate__lte=ten_days_overdue,
        reservationStatus="Overdue"
    )

    for reservation in overdue_10:
        user = reservation.userId
        equipment = reservation.equipId

        send_mail(
            subject="CRITICAL: Equipment 10 Days Overdue",
            message=f"""
Hi Admin,

The following equipment is now 10 days overdue and requires immediate action:

User: {user.username} ({user.email})
Equipment: {equipment.equipName}
Quantity: {reservation.quantityBorrowed}
Original Return Date: {reservation.returnDate}

This reservation has been marked as CRITICAL OVERDUE.

Regards,
Asset Management System
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["andreirobertpaval26@gmail.com"],
            fail_silently=False,
        )

        reservation.reservationStatus = "Critical Overdue"
        reservation.save()


# ---------------------------------------------------------
# 4. WRITE OFF ASSETS (30 days overdue)
# ---------------------------------------------------------
def write_off_assets():
    today = date.today()
    thirty_days_overdue = today - timedelta(days=30)

    reservations = Reservation.objects.filter(
        returnDate__lte=thirty_days_overdue,
        reservationStatus__in=["Overdue", "Critical Overdue"]
    )

    for reservation in reservations:
        user = reservation.userId
        equipment = reservation.equipId

        send_mail(
            subject="ASSET WRITE-OFF: Equipment 30 Days Overdue",
            message=f"""
Hi Admin,

The following equipment is now over 30 days overdue and has been marked as WRITTEN OFF:

User: {user.username} ({user.email})
Reservation ID: {reservation.reservationId}
Equipment: {equipment.equipName}
Quantity: {reservation.quantityBorrowed}
Original Return Date: {reservation.returnDate}

This item is now considered lost and should be replaced or removed from inventory.

Regards,
Asset Management System
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["andreirobertpaval26@gmail.com"],
            fail_silently=False,
        )

        reservation.reservationStatus = "Written Off"
        reservation.save()


# ---------------------------------------------------------
# 5. LOW STOCK CHECK (NEW)
# ---------------------------------------------------------
def check_low_stock():
    low_stock_items = Equipment.objects.filter(
        equipQuantity__lte=models.F("low_stock_threshold")
    )

    for item in low_stock_items:
        send_mail(
            subject=f"Low Stock Alert: {item.equipName}",
            message=f"""
Hi Admin,

The following equipment is low on stock:

- Equipment: {item.equipName}
- ID: {item.equipId}
- Current Quantity: {item.equipQuantity}
- Threshold: {item.low_stock_threshold}

Please consider reordering soon.

Regards,
Asset Management System
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["andreirobertpaval26@gmail.com"],
            fail_silently=False,
        )


# ---------------------------------------------------------
# 6. START SCHEDULER
# ---------------------------------------------------------
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        check_overdue_reservations,
        trigger="cron",
        hour=13,
        minute=26,
        id="check_overdue_reservations",
        replace_existing=True,
    )

    scheduler.add_job(
        send_upcoming_return_reminders,
        trigger="cron",
        hour=13,
        minute=25,
        id="send_upcoming_return_reminders",
        replace_existing=True,
    )

    scheduler.add_job(
        escalate_overdue_items,
        trigger="cron",
        hour=13,
        minute=25,
        id="escalate_overdue_items",
        replace_existing=True,
    )

    scheduler.add_job(
        write_off_assets,
        trigger="cron",
        hour=13,
        minute=25,
        id="write_off_assets",
        replace_existing=True,
    )

    # NEW: Low stock check every morning at 09:00
    scheduler.add_job(
        check_low_stock,
        trigger="cron",
        hour=13,
        minute=25,
        id="check_low_stock",
        replace_existing=True,
    )

    scheduler.start()
