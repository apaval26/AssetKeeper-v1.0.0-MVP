from base64 import urlsafe_b64encode
from datetime import date
import datetime
import random
import string
from types import MemberDescriptorType
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Equipment, Reservation, EquipmentReturn
from django.db.models import Q

from django.contrib.auth import logout
import csv

from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse 
from django.utils.http import urlsafe_base64_encode 
from django.utils.encoding import force_bytes 
from django.contrib.auth.models import User 
from django.core.mail import send_mail 
from django.conf import settings 
from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.db.models import Q

User = get_user_model()


from .models import Equipment, EquipmentReturn, Reservation

# Create your views here.

testdata = [
    {'id':1, 'name': 'Item 1 of list'},
    {'id':2, 'name': 'Item 2 of list'},
    {'id':3, 'name': 'Item 3 of list'},
    {'id':4, 'name': 'Item 4 of list'},
    {'id':5, 'name': 'Item 5 of list'},
    {'id':6, 'name': 'Item 6 of list'},
]

def home(request):
    return render(request, 'AppOneSDG/home.html', {'testdata':testdata})

def blist(request):
    return render(request, 'AppOneSDG/blist.html')

def navbar(request):
    return render(request, 'navbar.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home.html')
        else:
            return render(request, 'login.html', {'message': 'Invalid email or password'})
    else:
        return render(request, 'login.html')

"""
    
def forgot_password(request):
    message = ''
    form = PasswordResetForm()

    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            try:
                user = User.objects.get(email=email)

                form = PasswordResetForm({'email': email})

                if form.is_valid():
                    form.save(
                        request=request,
                        use_https=False,
                        from_email=None,
                        email_template_name='registration/password_reset_email.html',
                    )
                    return redirect('password_reset_done')
                else:
                    message = 'Please provide a valid email address.'

            except User.DoesNotExist:
                message = "No User Found With that Email Address."

        else:
            message = 'Please provide an email address.'

    return render(request,'forgot_password.html',{'form': form,'message': message})
    
    """
    

def user_admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home.html')
        else:
            return render(request, 'admin_login.html', {'message': 'Invalid email or password'})
    else:
        return render(request, 'admin_login.html')
    
    


def user_sign_up(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        contactNumber = request.POST.get('contactNumber')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        agree = request.POST.get('agree')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'sign_up.html', {'message': 'Passwords do not match'})

        if not agree:
            messages.error(request,"You must agree to the terms.")
            return render(request, 'sign_up.html', {'message': 'You must agree to the terms and conditions'})
        
        if User.objects.filter(username = email).exists():
            messages.error(request,"Email already registered.")
            return render(request, 'sign_up.html', {'message': 'Email already registered'})
        
        new_user = User.objects.create_user( username=email, email=email, password=password, firstName=firstName, lastName=lastName, contactNumber=contactNumber)
        new_user.full_name = full_name 
        new_user.save()
        messages.success(request, "Account created successfully.")

        #if User.objects.filter(email=email).exists():
            #return render(request, 'sign_up.html', {'message': 'Email already exists'})

        #user = User.objects.create_user(username=email, email=email, password=password)
        #user.first_name = full_name
        #user.save()

        return redirect('/')
    else:
        return render(request, 'sign_up.html')
    
"""
    
def export_equipments_csv(request):
    category = request.GET.get("category")
    location = request.GET.get("location")
    search = request.GET.get("search")

    equipments = Equipment.objects.all()

    # MULTI-CATEGORY FILTER (case-insensitive, supports messy DB values)
    if category:
        categories = [c.strip() for c in category.split(",")]

        q = Q()
        for c in categories:
            q |= Q(equipType__icontains=c)   # <— THIS is the key

        equipments = equipments.filter(q)

    # LOCATION FILTER
    if location:
        equipments = equipments.filter(equipLocation=location)

    # SEARCH FILTER
    if search:
        equipments = equipments.filter(
            Q(equipName__icontains=search)
            | Q(equipComments__icontains=search)
            | Q(equipType__icontains=search)
        )

    # CSV EXPORT
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="equipments.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "equipId",
        "equipName",
        "equipComments",
        "equipType",
        "equipQuantity",
    ])

    for equipment in equipments:
        writer.writerow([
            equipment.equipId,
            equipment.equipName,
            equipment.equipComments,
            equipment.equipType,
            equipment.equipQuantity,
        ])

    return response
"""

def export_equipments_csv(request):
    ids = request.GET.get("ids")

    if ids:
        id_list = ids.split(",")
        equipments = Equipment.objects.filter(equipId__in=id_list)
    else:
        equipments = Equipment.objects.all()

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="equipments.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "equipId",
        "equipName",
        "equipComments",
        "equipType",
        "equipQuantity",
        "equipStatus",
        "equipLocation",
    ])

    for equipment in equipments:
        writer.writerow([
            equipment.equipId,
            equipment.equipName,
            equipment.equipComments,
            equipment.equipType,
            equipment.equipQuantity,
            equipment.equipStatus,
            equipment.equipLocation,
        ])

    return response



def export_bookings_csv(request):
    search = request.GET.get("search")

    reservations = Reservation.objects.exclude(
        reservationStatus="Complete"
    ).select_related("equipId", "userId")

    if search:
        search = search.strip()
        reservations = reservations.filter(
            Q(userId__username__icontains=search) |
            Q(reservationId__icontains=search) |
            Q(equipId__equipName__icontains=search) |
            Q(equipId__equipType__icontains=search) |
            Q(reservationNotes__icontains=search)
        )

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="bookings.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "User ID",
        "Reservation ID",
        "Status",
        "Quantity",
        "Equipment Borrowed",
        "Notes",
        "Return Date"
    ])

    for r in reservations:
        equipment_display = f"[equipId: {r.equipId.equipId} -- {r.equipId.equipName}]"
        writer.writerow([
            r.userId.username,
            r.reservationId,
            r.reservationStatus,
            r.quantityBorrowed,
            equipment_display,
            r.reservationNotes,
            r.returnDate.strftime("%b. %d, %Y"),
        ])

    return response



 
@login_required
def devicesInventory(request): 
    equipments = Equipment.objects.all() 
    total_count = 0 
    category_counts = { 'VR_Headset': 0, 'VR_Controller': 0, 'PC_Laptop': 0, 'Phone_Tablets': 0, 'Furniture': 0, 'Presentation Tools': 0, 'Other': 0, } 
    category_map = { 'VR Headset': 'VR_Headset', 'VR Controller': 'VR_Controller', 'Laptop': 'PC_Laptop', 'Non Portable PC': 'PC_Laptop', 'Mobile Device': 'Phone_Tablets', 'Furniture': 'Furniture', 'PC Peripherals': 'Other', 'Camera/Sensors': 'Other', 'Presentation Tools:': 'Other', 'Other': 'Other', } 
    for item in equipments: 
        quantity = item.equipQuantity or 0 
        total_count += quantity
        category = category_map.get(item.equipType, 'Other') 
        category_counts[category] += quantity 
    
    context = { 'equipments': equipments, 'total_count': total_count, 'vr_headset': category_counts['VR_Headset'], 'vr_controller': category_counts['VR_Controller'], 'pc_laptop': category_counts['PC_Laptop'], 'phone_tablets': category_counts['Phone_Tablets'], 'furniture': category_counts['Furniture'],'Presentation Tools': category_counts['Presentation Tools'],  'other': category_counts['Other'] }
        
        
    return render(request, "devices_admin.html", context)

def borrowEquipmentUser(request):
    equipments = Equipment.objects.all()
    if request.method == "POST":
        equip_id = request.POST.get("equipId")

        try:
            quantity = int(request.POST.get("quantityBorrowed", 1))
        except (TypeError, ValueError):
            quantity = 1

        return_date = request.POST.get("endDate")
        notes = request.POST.get("notes")

        try:
            equipment = Equipment.objects.get(equipId=equip_id)

            # Check stock
            if equipment.equipQuantity < quantity:
                messages.error(
                    request,
                    "Not enough quantity available."
                )
                return redirect("devicesInventoryUser")

            # Update inventory (subtract borrowed quantity)
            equipment.equipQuantity = max(equipment.equipQuantity - quantity,0)
            equipment.save()

            if equipment.is_low_stock():
                 send_low_stock_email(equipment)


            # Create reservation log
            Reservation.objects.create(
                reservationStatus="Active",
                reservationDate=date.today(),
                returnDate=return_date,
                reservationNotes=notes,
                quantityBorrowed=quantity,
                equipId=equipment,
                userId=request.user,
            )

            messages.success(
                request,
                "Equipment borrowed successfully."
            )

            # Send email notification
            send_mail(
                subject="Equipment Borrowing Confirmation",
                message=f"""
Hi {request.user.username},

Your equipment borrowing has been recorded successfully.

Details:
- Equipment: {equipment.equipName}
- Quantity Borrowed: {quantity}
- Borrow Date: {date.today()}
- Expected Return Date: {return_date}
- Notes: {notes}
- Remaining Stock: {equipment.equipQuantity}

Make sure you return it by the assigned date.

Regards,
IT Department
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    "andreirobertpaval26@gmail.com",
                    request.user.email,
                ],
                fail_silently=False,
            )

        except Equipment.DoesNotExist:
            messages.error(
                request,
                "Equipment not found."
            )
        

        return redirect("devicesInventoryUser")
       

    return render(
        request,
        "borrow_equipment.html",
        {"equipments":equipments}
    )


def borrow_equipment(request):
    equipments = Equipment.objects.all()

    if request.method == "POST":
        equip_id = request.POST.get("equipId")

        try:
            quantity = int(request.POST.get("quantityBorrowed", 1))
        except (TypeError, ValueError):
            quantity = 1

        return_date = request.POST.get("endDate")
        notes = request.POST.get("notes")

        try:
            equipment = Equipment.objects.get(equipId=equip_id)

            if equipment.equipQuantity < quantity:
                messages.error(request, "Not enough quantity available.")
                return redirect("devicesInventory")

            # Update inventory
            equipment.equipQuantity = max(
                equipment.equipQuantity - quantity,
                0
            )
            equipment.save()
            
            if equipment.is_low_stock():
                 send_low_stock_email(equipment)

            # Create reservation
            Reservation.objects.create(
                reservationStatus="Active",
                reservationDate=date.today(),
                returnDate=return_date,
                reservationNotes=notes,
                quantityBorrowed=quantity,
                equipId=equipment,
                userId=request.user,
            )

            messages.success(request, "Equipment borrowed successfully.")

            # Send confirmation email
            send_mail(
                subject="Equipment Borrowing Confirmation",
                message=f"""
Hi {request.user.username},

Your equipment borrowing has been recorded successfully.

Details:
- Equipment: {equipment.equipName}
- Quantity Borrowed: {quantity}
- Borrow Date: {date.today()}
- Expected Return Date: {return_date}
- Notes: {notes}
- Remaining Stock: {equipment.equipQuantity}

Make sure you return it by the assigned date.

Regards,
IT Department
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    "andreirobertpaval26@gmail.com",
                    request.user.email,
                ],
                fail_silently=False,
            )

        except Equipment.DoesNotExist:
            messages.error(request, "Equipment not found.")

        return redirect("devicesInventory")

    return render(
        request,
        "borrow_equipment_admin.html",
        {
            "equipments": equipments,  # ← correctly passed to template
        }
    )

    
def returnEquipment(request):
    if request.method == "POST":
        reservation_id = request.POST.get("reservationId")

        try:
            quantity = int(request.POST.get("quantityBorrowed", 1))
        except (TypeError, ValueError):
            quantity = 1

        date_returned = request.POST.get("dateReturned")
        notes = request.POST.get("notes")

        try:
            # Get the reservation directly
            reservation = Reservation.objects.get(
                reservationId=reservation_id,
                userId=request.user,
                reservationStatus__in=["Active","Overdue"]
            )

            equipment = reservation.equipId
            
            if quantity > reservation.quantityBorrowed:
                messages.error(request, f"You cannot return more than you borrowed ({reservation.quantityBorrowed}).")
               

            # Update inventory
            equipment.equipQuantity += quantity
            equipment.save()

            # Mark reservation as complete
            reservation.reservationStatus = "Complete"
            reservation.save()
            
            if equipment.is_low_stock(): 
                send_low_stock_email(equipment)

            # Log the return
            EquipmentReturn.objects.create(
                equipId=equipment,
                quantityReturned=quantity,
                dateReturned=date_returned,
                notes=notes,
                userId=request.user,
            )

            messages.success(request, "Equipment returned successfully.")

            # Send email
            send_mail(
                subject="Equipment Return Confirmation",
                message=f"""
Hi {request.user.username},

Your equipment return has been recorded successfully.

Details:
- Equipment: {equipment.equipName}
- Quantity Returned: {quantity}
- Date Returned: {date_returned}
- Notes: {notes}
- Updated Stock: {equipment.equipQuantity}

Regards,
IT Department
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    "andreirobertpaval26@gmail.com",
                    request.user.email,
                ],
                fail_silently=False,
            )

        except Reservation.DoesNotExist:
            messages.error(request, "Reservation not found or already completed.")

        return redirect("devicesInventory")

    # GET request → show dropdown
    active_reservations = Reservation.objects.filter(
        userId=request.user,
        reservationStatus__in=["Active","Overdue"]
    ).select_related("equipId")

    return render(
        request,
        "return_equipment_admin.html",
        {"reservations": active_reservations}
    )



def returnEquipmentUser(request):
    if request.method == "POST":
        reservation_id = request.POST.get("reservationId")

        try:
            quantity = int(request.POST.get("quantityBorrowed", 1))
        except (TypeError, ValueError):
            quantity = 1

        date_returned = request.POST.get("dateReturned")
        notes = request.POST.get("notes")

        try:
            # Get the reservation directly
            reservation = Reservation.objects.get(
                reservationId=reservation_id,
                userId=request.user,
                reservationStatus__in=["Active","Overdue"]
            )

            equipment = reservation.equipId
            
            if quantity > reservation.quantityBorrowed:
                messages.error(request, f"You cannot return more than you borrowed ({reservation.quantityBorrowed}).")
               

            # Update inventory
            equipment.equipQuantity += quantity
            equipment.save()

            # Mark reservation as complete
            reservation.reservationStatus = "Complete"
            reservation.save()
            
            if equipment.is_low_stock():
                 send_low_stock_email(equipment)

            # Log the return
            EquipmentReturn.objects.create(
                equipId=equipment,
                quantityReturned=quantity,
                dateReturned=date_returned,
                notes=notes,
                userId=request.user,
            )

            messages.success(request, "Equipment returned successfully.")

            # Send email
            send_mail(
                subject="Equipment Return Confirmation",
                message=f"""
Hi {request.user.username},

Your equipment return has been recorded successfully.

Details:
- Equipment: {equipment.equipName}
- Quantity Returned: {quantity}
- Date Returned: {date_returned}
- Notes: {notes}
- Updated Stock: {equipment.equipQuantity}

Regards,
IT Department
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    "andreirobertpaval26@gmail.com",
                    request.user.email,
                ],
                fail_silently=False,
            )

        except Reservation.DoesNotExist:
            messages.error(request, "Reservation not found or already completed.")

        return redirect("devicesInventoryUser")

    # GET request → show dropdown
    active_reservations = Reservation.objects.filter(
        userId=request.user,
        reservationStatus__in=["Active","Overdue"]
    ).select_related("equipId")

    return render(
        request,
        "return_equipment_user.html",
        {"reservations": active_reservations}
    )

    


    
"""def forgot_password(request):
    message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
    
        if email:
          try:
           user = User.objects.get(email=email) 
           uid = urlsafe_b64encode(force_bytes(user.pk)) 
           token = default_token_generator.make_token(user)
           reset_path = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
           reset_link = request.build_absolute_uri(reset_path)
           #reset_link = f"http://127.0.0.1:8000/reset/{uid}/{token}/"
            #send_mail(
                #'Password Reset',
                #f'Click the link to reset your password: {reset_link}',
                #settings.EMAIL_HOST_USER,
                #[email],
                #fail_silently=False,
            #)
            
           send_mail( 'Password Reset', f'Click the link to reset your password: {reset_link}', settings.EMAIL_HOST_USER, [email], fail_silently=False, )
           message = 'An email has been sent to reset your password'
           
          except User.DoesNotExist:
              message = "No User Found With that Email Address."
        else:
            message = 'Please provide an email address.'
    return render(request, 'forgot_password.html', {'message': message})
    
"""
def forgot_password(request):
    message = ''
    form = PasswordResetForm()

    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            try:
                user = User.objects.get(email=email)

                form = PasswordResetForm({'email': email})

                if form.is_valid():
                    form.save(
                        request=request,
                        use_https=False,
                        from_email=None,
                        email_template_name='registration/password_reset_email.html',
                    )
                    return redirect('password_reset_done')
                else:
                    message = 'Please provide a valid email address.'

            except User.DoesNotExist:
                message = "No User Found With that Email Address."

        else:
            message = 'Please provide an email address.'

    return render(request,'forgot_password.html',{'form': form,'message': message})

def logout_view(request): 
    logout(request) 
    return render(request, 'sign_up.html')

def login_unauthorized(request):
    return render(request,'login_unauthorized.html')

@login_required
def contact_us(request):
    return render(request,"contactus.html")

def sitemap(request):
    return render(request,"sitemap.html")


def currentBookings(request):
    reservations = (
        Reservation.objects
        .filter(
            userId=request.user,
            reservationStatus__in=["Active", "Overdue", "Critical Overdue"]  # or whatever status you use
        )
        .select_related("equipId")
        .order_by("returnDate")
    )

    return render(
        request,
        "currentBookings.html",
        {
            "reservations": reservations,
        }
    )

def bookingsHistory(request):
    reservations = (
        Reservation.objects
        .filter(userId=request.user)
        .select_related("equipId")
        .order_by("-reservationDate")
    )

    return render(
        request,
        "bookingsHistory.html",
        {
            "reservations": reservations,
        }
    )


def updateAccountInformation(request):
    return render(request,"updateAccountInformation.html")


#def devices(request):
    #return render(request,"bookingsHistory.html")


def manageBookings(request):
    reservationsToApprove = Reservation.objects.exclude(
        reservationStatus="Complete"
    )

    context = {'reservationsToApprove': reservationsToApprove}
    return render(request, "manageBookings.html", context)

def completedBookingsAdmin(request):
    completed_reservations = Reservation.objects.filter(
        reservationStatus="Complete"
    ).select_related("equipId", "userId").order_by("-returnDate")

    context = {
        "completed_reservations": completed_reservations
    }

    return render(request, "completedBookingsAdmin.html", context)

def completedBookingsUser(request):
    completed_reservations = Reservation.objects.filter(
        userId=request.user,
        reservationStatus="Complete"
    ).select_related("equipId", "userId").order_by("-returnDate")

    context = {
        "completed_reservations": completed_reservations
    }

    return render(request, "completedBookingsUser.html", context)

def manageUsers(request):
    
    return render(request,"manageUsers.html")


def main_admin(request):
    return render(request,"main_admin.html")

def main_user(request):
    return render(request,"main_user.html")


#@login_required
def devices(request):
    equipments = Equipment.objects.all()
    context = {'equipments' : equipments}
    return render(request, "devices.html", context)

def devicesInventoryUser(request):
    equipments = Equipment.objects.all()
    context = {'equipments' : equipments}
    total_items = equipments.count(),
    total_quantity =  sum(equipment.equipQuantity for equipment in equipments )
    
    # ✅ Sum only for PC peripherals 
    
    pc_peripherals_quantity = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "PC Peripherals" )
    
    #Sum only for VR Headset
    
    vr_headset_quantity = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "VR Headset" )
    
    return render(request, "devices.html", { 'equipments': equipments, 'total_items': total_items, 'total_quantity': total_quantity, 'pc_peripherals_quantity': pc_peripherals_quantity, 'vr_headset_quantity' : vr_headset_quantity })


def devicesInventory(request):
    equipments = Equipment.objects.all()
    context = {'equipments' : equipments}
    total_items = equipments.count(),
    total_quantity =  sum(equipment.equipQuantity for equipment in equipments )
    
    # ✅ Sum only for PC peripherals 
    
    pc_peripherals_quantity = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "PC Peripherals" )
    
    #Sum only for VR Headsets
    
    vr_headset_quantity = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "VR Headset" )
    
    pc_laptop = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "Laptop" )
    
    furniture = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "Furniture" )
    
    mobile_devices = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "Mobile Device" )
    
    other = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "Other" )
    
    accessories = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "Accessories" )
    
    presentation_tools = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "Presentation Tools" )
    
    stationary = sum( equipment.equipQuantity for equipment in equipments if equipment.equipType == "Stationary" )
    
    return render(request, "devices_admin.html", { 'equipments': equipments, 'total_items': total_items, 'total_quantity': total_quantity, 'pc_peripherals_quantity': pc_peripherals_quantity, 'vr_headset_quantity' : vr_headset_quantity, 'pc_laptop': pc_laptop, 'furniture' : furniture , 'mobile_devices': mobile_devices,"accessories": accessories, "presentation_tools": presentation_tools, "stationary": stationary, 'other': other})
    
def equipment_list_sorted(request): 
    equipments = Equipment.objects.all().order_by('equipName') # A → Z 
    total_items = equipments.count() 
    total_quantity = sum(e.equipQuantity for e in equipments) 
    return render(request, "devices_admin.html", { 'equipments': equipments, 'total_items': total_items, 'total_quantity': total_quantity, })

def equipment_list_sorted_desc(request): 
    equipments = Equipment.objects.all().order_by('-equipName') # Z -> A 
    total_items = equipments.count() 
    total_quantity = sum(e.equipQuantity for e in equipments) 
    return render(request, "devices_admin.html", { 'equipments': equipments, 'total_items': total_items, 'total_quantity': total_quantity, })

def equipment_list_sorted_user(request): 
    equipments = Equipment.objects.all().order_by('equipName') # A → Z 
    total_items = equipments.count() 
    total_quantity = sum(e.equipQuantity for e in equipments) 
    return render(request, "devices.html", { 'equipments': equipments, 'total_items': total_items, 'total_quantity': total_quantity, })

def equipment_list_sorted_user_desc(request): 
    equipments = Equipment.objects.all().order_by('-equipName') # Z -> A 
    total_items = equipments.count() 
    total_quantity = sum(e.equipQuantity for e in equipments) 
    return render(request, "devices.html", { 'equipments': equipments, 'total_items': total_items, 'total_quantity': total_quantity, })

def reservation_list_sorted(request):
    reservationsToApprove = Reservation.objects.all().order_by("userId")

    return render(
        request,
        "manageBookings.html",
        {
            "reservationsToApprove": reservationsToApprove,
        }
    )


def reservation_list_sorted_desc(request):
    reservationsToApprove = Reservation.objects.all().order_by("-userId")

    return render(
        request,
        "manageBookings.html",
        {
            "reservationsToApprove": reservationsToApprove,
        }
    )

import random
import string
from datetime import datetime
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import redirect

def generate_ticket_id():
    #date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"#{random_part}"

def contact_submit(request):
    if request.method == "POST":
        ticket_id = generate_ticket_id()

        first = request.POST.get("firstName", "").strip()
        last = request.POST.get("lastName", "").strip()
        email = request.POST.get("emailAddress", "").strip()
        phone = request.POST.get("telephoneNumber", "").strip()
        issue_type = request.POST.get("issueType", "").strip()
        message = request.POST.get("message", "").strip()
        evidence_file = request.FILES.get("evidenceFile")

        full_message = f"""
New Contact Form Submission

Ticket ID: {ticket_id}

Name: {first} {last}
Email: {email}
Phone: {phone}
Issue Type: {issue_type}

Message:
{message}
"""

        email_msg = EmailMessage(
            subject=f"New Service Desk Request — {ticket_id}",
            body=full_message,
            from_email="yourgmail@gmail.com",
            to=[
                "w1907294@my.westminster.ac.uk",
                "andreirobertpaval26@gmail.com"
            ],
        )

        if evidence_file:
            email_msg.attach(
                evidence_file.name,
                evidence_file.read(),
                evidence_file.content_type
            )

        email_msg.send()

        messages.success(request, f"Your message has been sent successfully. Your ticket ID is {ticket_id}.")
        return redirect("contact_page")

    return redirect("contact_page")




    
def addProduct(request):
    return render(request,"addProduct.html")


def updateProduct(request):
    return render(request,"updateProduct.html")

def productOverview(request):
    return render(request,"productOverview.html")

def productOverview2(request):
    return render(request,"productOverview2.html")

def productOverview3(request):
    return render(request,"productOverview3.html")

def equipment_list(request):
    equipments = Equipment.objects.all()

    return render(
        request,
        'device_admin.html',
        {
            'equipments': equipments,
            'total_items': equipments.count(),
            'total_quantity': sum(e.equipQuantity for e in equipments),
        }
    )
    
def export_completed_bookings_admin(request):
    ids = request.GET.get("ids")

    if ids:
        id_list = ids.split(",")
        reservations = Reservation.objects.filter(
            reservationId__in=id_list,
            reservationStatus="Complete"
        ).select_related("equipId", "userId")
    else:
        reservations = Reservation.objects.filter(
            reservationStatus="Complete"
        ).select_related("equipId", "userId")

    # If no results → return empty CSV with headers only
    if not reservations.exists():
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="completed_bookings.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "User",
            "Reservation ID",
            "Equipment",
            "Equipment Type",
            "Quantity",
            "Reservation Status",
            "Return Date",
            "Notes",
        ])
        return response

    # Normal export
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="completed_bookings.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "User",
        "Reservation ID",
        "Equipment",
        "Equipment Type",
        "Quantity",
        "Reservation Status",
        "Return Date",
        "Notes",
    ])

    for r in reservations:
        writer.writerow([
            r.userId.username,
            r.reservationId,
            r.equipId.equipName,
            r.equipId.equipType,
            r.quantityBorrowed,
            r.reservationStatus,
            r.returnDate,
            r.reservationNotes,
        ])

    return response


"""
def export_bookings_csv(request):
    category = request.GET.get("category")
    search = request.GET.get("search")

    # Match the admin table: exclude completed reservations
    reservations = Reservation.objects.exclude(
        reservationStatus="Complete"
    ).select_related("equipId", "userId")

    # Filter by category (equipment type)
    if category:
        categories = [c.strip() for c in category.split(",")]
        q = Q()
        for c in categories:
            q |= Q(equipId__equipType__icontains=c)
        reservations = reservations.filter(q)

    # Filter by search term
    if search:
        search = search.strip()
        reservations = reservations.filter(
            Q(userId__username__icontains=search) |
            Q(reservationId__icontains=search) |
            Q(equipId__equipName__icontains=search) |
            Q(equipId__equipType__icontains=search) |
            Q(reservationNotes__icontains=search)
        )

    # CSV export
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="bookings.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "User",
        "Reservation ID",
        "Status",
        "Quantity",
        "Equipment",
        "Equipment Type",
        "Notes",
        "Return Date",
    ])

    for r in reservations:
        writer.writerow([
            r.userId.username,
            r.reservationId,
            r.reservationStatus,
            r.quantityBorrowed,
            r.equipId.equipName,
            r.equipId.equipType,
            r.reservationNotes,
            r.returnDate,
        ])

    return response
"""
def export_bookings_csv(request):
    ids = request.GET.get("ids")

    if ids:
        id_list = ids.split(",")
        reservations = Reservation.objects.filter(reservationId__in=id_list)
    else:
        reservations = Reservation.objects.exclude(reservationStatus="Complete")

    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="bookings.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "User ID",
        "Reservation ID",
        "Status",
        "Quantity",
        "Equipment Borrowed",
        "Notes",
        "Return Date"
    ])

    for r in reservations:
        equipment_display = f"[equipId: {r.equipId.equipId} -- {r.equipId.equipName}]"
        writer.writerow([
            r.userId.username,
            r.reservationId,
            r.reservationStatus,
            r.quantityBorrowed,
            equipment_display,
            r.reservationNotes,
            r.returnDate.strftime("%b. %d, %Y"),
        ])

    return response



def export_completed_bookings_user(request):
    ids = request.GET.get("ids")

    if ids:
        id_list = ids.split(",")
        reservations = Reservation.objects.filter(
            reservationId__in=id_list,
            reservationStatus="Complete"
        ).select_related("equipId", "userId")
    else:
        reservations = Reservation.objects.filter(
            reservationStatus="Complete"
        ).select_related("equipId", "userId")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="completed_bookings.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "User",
        "Reservation ID",
        "Equipment",
        "Equipment Type",
        "Quantity",
        "Reservation Status",
        "Return Date",
        "Notes",
    ])

    for r in reservations:
        writer.writerow([
            r.userId.username,
            r.reservationId,
            r.equipId.equipName,
            r.equipId.equipType,
            r.quantityBorrowed,
            r.reservationStatus,
            r.returnDate,
            r.reservationNotes,
        ])

    return response

def completed_bookings_sorted_admin(request):
    completed_reservations = Reservation.objects.filter(
        reservationStatus="Complete"
    ).select_related("equipId", "userId").order_by("equipId__equipName")  # A → Z

    context = {
        "completed_reservations": completed_reservations
    }

    return render(request, "completedBookingsAdmin.html", context)


def completed_bookings_sorted_desc_admin(request):
    completed_reservations = Reservation.objects.filter(
        reservationStatus="Complete"
    ).select_related("equipId", "userId").order_by("-equipId__equipName")  # Z → A

    context = {
        "completed_reservations": completed_reservations
    }

    return render(request, "completedBookingsAdmin.html", context)


def completed_bookings_sorted_user(request):
    completed_reservations = Reservation.objects.filter(
        reservationStatus="Complete"
    ).select_related("equipId", "userId").order_by("equipId__equipName")  # A → Z

    context = {
        "completed_reservations": completed_reservations
    }

    return render(request, "completedBookingsUser.html", context)


def completed_bookings_sorted_desc_user(request):
    completed_reservations = Reservation.objects.filter(
        reservationStatus="Complete"
    ).select_related("equipId", "userId").order_by("-equipId__equipName")  # Z → A

    context = {
        "completed_reservations": completed_reservations
    }

    return render(request, "completedBookingsUser.html", context)



def export_booking_history_user(request):
    ids = request.GET.get("ids")

    if ids:
        id_list = ids.split(",")
        reservations = Reservation.objects.filter(
            reservationId__in=id_list,
            userId=request.user
        ).select_related("equipId", "userId").order_by("-reservationDate")
    else:
        reservations = Reservation.objects.filter(
            userId=request.user
        ).select_related("equipId", "userId").order_by("-reservationDate")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="booking_history.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Reservation ID",
        "Equipment ID",
        "Device Name",
        "Device Type",
        "Quantity",
        "Status",
        "Reserved On",
        "Return Date",
    ])

    for r in reservations:
        writer.writerow([
            r.reservationId,
            r.equipId.equipId,
            r.equipId.equipName,
            r.equipId.equipType,
            r.quantityBorrowed,
            r.reservationStatus,
            r.reservationDate,
            r.returnDate,
        ])

    return response



def export_current_bookings_user(request):
    ids = request.GET.get("ids")

    if ids:
        id_list = ids.split(",")
        reservations = Reservation.objects.filter(
            reservationId__in=id_list,
            userId=request.user,
            reservationStatus__in=["Active", "Overdue", "Pending"]
        ).select_related("equipId", "userId")
    else:
        reservations = Reservation.objects.filter(
            userId=request.user,
            reservationStatus__in=["Active", "Overdue", "Pending"]
        ).select_related("equipId", "userId")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="current_bookings.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Device ID",
        "Device Name",
        "Device Type",
        "Reservation ID",
        "Location",
        "Status",
        "Quantity",
        "Return Date",
    ])

    for r in reservations:
        writer.writerow([
            r.equipId.equipId,
            r.equipId.equipName,
            r.equipId.equipType,
            r.reservationId,
            r.equipId.equipLocation,
            r.reservationStatus,
            r.quantityBorrowed,
            r.returnDate,
        ])

    return response


def send_low_stock_email(equipment):
    subject = f"Low Stock Alert: {equipment.equipName}"

    message = (
        f"Attention,\n\n"
        f"The stock level for the following equipment is low:\n\n"
        f"Name: {equipment.equipName}\n"
        f"ID: {equipment.equipId}\n"
        f"Current Quantity: {equipment.equipQuantity}\n"
        f"Threshold: {equipment.low_stock_threshold}\n\n"
        f"Please consider reordering soon.\n"
    )

    send_mail(
        subject,
        message,
        None,  # uses DEFAULT_FROM_EMAIL
        ["andreirobertpaval26@gmail.com"],  # change to real admin email
        fail_silently=False,
    )







