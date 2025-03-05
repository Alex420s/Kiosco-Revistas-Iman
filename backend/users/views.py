from ninja import Router, Form
from ninja.security import HttpBearer
from django.contrib.auth import authenticate
from .schemas import UserIn, UserOut, VerificationIn, TokenOut, MessageOut
from .models import CustomUser
from django.conf import settings
import jwt
from datetime import datetime, timedelta

router = Router()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  # Decodifica el token JWT usando la SECRET_KEY
            user = CustomUser.objects.get(id=payload['user_id'])    # Busca el usuario en la base de datos
            return user
        except:
            return None

auth = AuthBearer() 

def create_token(user_id: int) -> dict:
    # Crea el token de acceso (dura 1 día)
    access_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'type': 'access'
    }
    # Crea el token de actualización (dura 7 días)
    refresh_payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7),
        'type': 'refresh'
    }
     # Codifica los tokens usando JWT
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

@router.post('/register', response={201: UserOut, 400: MessageOut})
def register(request, data: UserIn):
    """
    Registra un usuario {
    "username": "john_doe",
    "phone_number": "+1234567890",
    "password": "secreto123"}
"""
    try:
        user = CustomUser.objects.create_user(
            username=data.username,
            phone_number= '+52' + data.phone_number,
            password=data.password
        )
        user.send_verification_sms()
         # Devuelve los datos del usuario creado
        return 201, UserOut.from_orm(user)
    except Exception as e:
        return 400, {'message': str(e)}

@router.post('/verify/{user_id}', response={200: MessageOut, 400: MessageOut})
def verify_phone(request, user_id: int, data: VerificationIn):
    try:
        user = CustomUser.objects.get(id=user_id)
        # Verifica si el código coincide
        if user.verification_code == data.code:
            user.is_phone_verified = True
            user.verification_code = None
            user.save()
            return 200, {'message': 'Teléfono verificado exitosamente'}
        return 400, {'message': 'Código inválido'}
    except CustomUser.DoesNotExist:
        return 400, {'message': 'Usuario no encontrado'}

@router.post('/login', response={200: TokenOut, 400: MessageOut})
def login(request, username: str = Form(...), password: str = Form(...)):
    user = authenticate(username=username, password=password)
    if user is None:
        return 400, {'message': 'Credenciales inválidas'}
    if not user.is_phone_verified:
        return 400, {'message': 'Teléfono no verificado'}
    
    return 200, create_token(user.id)

