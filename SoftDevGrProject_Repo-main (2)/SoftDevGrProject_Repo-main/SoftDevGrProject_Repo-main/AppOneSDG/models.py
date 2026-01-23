from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.



# Here is a model manager, made specifically for our custom User model below. It allows us to build queries or override functions that commonly get used
class MyUserManager(BaseUserManager):
    # This is an overridden function, for creating a new user
    def create_user(self, firstName, lastName, email, contactNumber, username, password=None):
        if not firstName:
            raise ValueError("Users must have a first name.")
        if not lastName:
            raise ValueError("Users must have a last name.")
        if not email:
            raise ValueError("Users must have an email address.")
        if not contactNumber:
            raise ValueError("Users must have a contact number.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            firstName=firstName,
            lastName=lastName,
            email=self.normalize_email(email),
            contactNumber=contactNumber,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # This is another function which we override, to create a new superuser
    def create_superuser(self, firstName, lastName, email, contactNumber, username, password):
        user = self.create_user(
            firstName=firstName,
            lastName=lastName,
            email=self.normalize_email(email),
            contactNumber=contactNumber,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



# Here is a custom model for the User entity/table
class User(AbstractBaseUser):
    # These fields are based on the attributes for a user, from our Logical ERD
    userId              = models.AutoField(verbose_name="User ID", primary_key=True)
    firstName           = models.CharField(verbose_name="First name", max_length=100)
    lastName            = models.CharField(verbose_name="Last name", max_length=100)
    username            = models.CharField(verbose_name="Username", max_length=100, unique=True)
    email               = models.EmailField(verbose_name="Email address", max_length=100, unique=True)
    contactNumber       = models.CharField(verbose_name="Contact number", max_length=100)
    emergencyContact    = models.CharField(verbose_name="Emergency contact", max_length=100)

    # These fields are included in the AbstractBaseUser class, so we need to override these to extend a user model
    date_joined         = models.DateTimeField(verbose_name='Date joined', auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name='Last login', auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)

    # This parameter is set to allow us to log in with the email, as opposed to the username (which django by default does)
    USERNAME_FIELD = 'email'

    # This parameter is set so that, alongside the new USERNAME_FIELD, we can also make any other fields required to create a user account
    REQUIRED_FIELDS = ['firstName', 'lastName', 'contactNumber', 'username']

    # We need to set the above custom user manager to our model - it's how we tie the User to the MyUserManager
    objects = MyUserManager()

    # This method/function will determine what's going to be returned, when you access the object (i.e. model) but you don't access any individual field
    def __str__(self):
        return self.username
    
    # This is a default function that we override. It sets whether a user has permission to do an admin-like thing (i.e. if they are an admin, then yes)
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # This is another permission function. It also has to be overridden
    def has_module_perms(self, app_label):
        return True



#Equipment
class Equipment(models.Model):
    
    EQUIPMENT_CATEGORY = [ ("PC Peripherals", "PC Peripherals"), ("Non Portable PC", "Non Portable PC"), ("Laptop", "Laptop"), ("Mobile Device", "Mobile Device"), ("VR Headset", "VR Headset"), ("VR Controller", "VR Controller"), ("Camera/Sensors", "Camera/Sensors"), ("Furniture", "Furniture"), ("Presentation Tools", "Presentation Tools"), ("Stationary", "Stationary"), ("Furniture", "Furniture"), ("Accessories", "Accessories"),("Other", "Other") ]
    
    equipId             = models.AutoField(verbose_name="Equipment ID", primary_key=True)
    equipName           = models.CharField(verbose_name="Equipment name", max_length=100)
    equipType           = models.CharField(verbose_name="Equipment type", choices=EQUIPMENT_CATEGORY, max_length=100)
    equipQuantity       = models.IntegerField(verbose_name="Quantity for equipment", default=0)
    equipAudit          = models.DateField(verbose_name="Last audit for equipment")
    #equipLocation       = models.CharField(verbose_name="Location of equipment", max_length=100, choices=[ ("Available", "Available"), ("Borrowed", "Borrowed"), ("Lost", "Lost"), ("Written Off", "Written Off"), ], default = "Available")
    equipLocation         = models.CharField(verbose_name="Location of equipment", max_length=100, blank=True)
    equipStatus       = models.CharField(verbose_name="Status of equipment", max_length=100, default = "Available")
    equipComments       = models.TextField(verbose_name="Comments on equipment", blank=True)
    isOnsite            = models.BooleanField(default=False)
    low_stock_threshold = models.IntegerField(default=5) # Optional but recommended
    
    def is_low_stock(self): 
        return self.equipQuantity <= self.low_stock_threshold
    
    def save(self, *args, **kwargs):

    # Do not override special statuses
      if self.equipStatus in ["Lost", "Repairing", "Written Off"]:
        super().save(*args, **kwargs)
        return

    # Quantity is zero → Borrowed
      if self.equipQuantity == 0:
        self.equipStatus = "Out Of Stock"

    # Low stock (but not zero)
      elif self.equipQuantity <= self.low_stock_threshold:
        self.equipStatus = "Low Stock"

    # Otherwise available
      else:
        self.equipStatus = "Available"

      super().save(*args, **kwargs)


    
    
    def __str__(self):
        return f"[equipId: {self.equipId}  --  {self.equipName}]"



#Device_Serial_Number
class Device_Serial_Number(models.Model):
    equipId             = models.OneToOneField(Equipment, on_delete=models.CASCADE, primary_key=True, verbose_name="Corresponding equipment ID", related_name='equipments_with_extra_details')
    deviceSerialNo      = models.CharField(verbose_name="Device serial number", max_length=100)
    deviceCPU           = models.CharField(verbose_name="Device CPU", max_length=100, blank=True)
    deviceGPU           = models.CharField(verbose_name="Device GPU", max_length=100, blank=True)
    deviceRAM           = models.CharField(verbose_name="Device RAM", max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.equipId}"



#Admin
class Admin(models.Model):
    userId              = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Corresponding user username", related_name='users_who_are_admins')

    def __str__(self):
        return f"[admin with username -- {self.userId}]"



#Reservation
class Reservation(models.Model):
    reservationId       = models.AutoField(verbose_name='Reservation ID', primary_key=True)
    reservationStatus   = models.CharField(verbose_name='Status of reservation', max_length=100, choices=[ ("Pending", "Pending"), ("Approved", "Approved"), ("Overdue", "Overdue"), ("Critical Overdue", "Critical Overdue"), ("Active", "Active"), ("Complete", "Complete"), ("Written Off", "Written Off"), ], default = "Active")
    reservationDate     = models.DateField(verbose_name='Date of reservation')
    returnDate          = models.DateField(verbose_name='Return date for reservation')
    reservationNotes    = models.TextField(verbose_name='Notes about reservation', blank=True)
    userId              = models.ForeignKey(User, related_name='users_who_place_reservations', on_delete=models.CASCADE, null=False, verbose_name='Corresponding user ID')
    adminUserId         = models.ForeignKey(Admin, related_name='admins_who_approve_reservations', on_delete=models.CASCADE, null=True, verbose_name='Corresponding admin ID')
    equipId             = models.ForeignKey(Equipment, related_name='equipments_that_are_reserved', on_delete=models.CASCADE, null=False, verbose_name='Corresponding equipment ID')
    quantityBorrowed = models.IntegerField(verbose_name="Quantity borrowed", default=0)
    def __str__(self):
        return f"[reservationId: {self.reservationId}]"



    
#Return for admin

class EquipmentReturn(models.Model):
    equipId = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE
    )
    quantityReturned = models.IntegerField()
    dateReturned = models.DateField()
    notes = models.TextField(
        blank=True,
        null=True
    )
    userId = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )




#Admin_User_Manage
class Admin_User_Manage(models.Model):
    modifyId            = models.AutoField(verbose_name='ID of this management', primary_key=True)
    userId              = models.ForeignKey(User, related_name='users_who_admins_manage', on_delete=models.CASCADE, null=False, verbose_name='Corresponding user ID')
    adminUserId         = models.ForeignKey(Admin, related_name='admins_who_manage_users', on_delete=models.CASCADE, null=False, verbose_name='Corresponding admin ID')
    modifyDateTime      = models.DateTimeField(verbose_name='Time/Date of management', auto_now_add=True)
    
    def __str__(self):
        return f"[manageId: {self.modifyId}]"



#Admin_Equip_Manage
class Admin_Equip_Manage(models.Model):
    updateId            = models.AutoField(verbose_name='ID of this management', primary_key=True)
    equipId             = models.ForeignKey(Equipment, related_name='equipments_that_admins_manage', on_delete=models.CASCADE, null=False, verbose_name='Corresponding equipment ID')
    adminUserId         = models.ForeignKey(Admin, related_name='admins_who_manage_equipments', on_delete=models.CASCADE, null=False, verbose_name='Corresponding admin ID')
    updateDateTime      = models.DateTimeField(verbose_name='Time/Date of management', auto_now_add=True)
    
    def __str__(self):
        return f"[manageId: {self.updateId}]"