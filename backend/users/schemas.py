from ninja import Schema


class UserIn(Schema):
    username: str
    phone_number: str
    password: str

class UserOut(Schema):
    id: int
    username: str
    phone_number: str
    is_phone_verified: bool

class VerificationIn(Schema):
    code: str

class TokenOut(Schema):
    access_token: str
    refresh_token: str

class MessageOut(Schema):
    message: str

"""Al usar estos schemas:

-Validan automáticamente los datos de entrada
-Documentan claramente la estructura de datos esperada
-Proporcionan autocompletado en IDEs
-Generan automáticamente la documentación OpenAPI/Swagger
-Convierten automáticamente entre Python y JSON

"""