from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import random
from django.conf import settings
from twilio.rest import Client

class CustomUserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        if not phone_number:
            raise ValueError('El número de teléfono es obligatorio')
        
        user = self.model(
            username=username,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(username, phone_number, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), blank=True)  # Hacemos email opcional
    phone_number = models.CharField(max_length=15, unique=True)
    is_phone_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']
    
    def generate_verification_code(self):
        code = str(random.randint(100000, 999999))
        self.verification_code = code
        self.save()
        return code
    
    def send_verification_sms(self):
        if not self.verification_code:
            self.generate_verification_code()
            
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'Tu código de verificación es: {self.verification_code}',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=self.phone_number
        )
        return message.sid
    
    def verify_phone(self, code):
        if self.verification_code == code:
            self.is_phone_verified = True
            self.verification_code = None
            self.save()
            return True
        return False