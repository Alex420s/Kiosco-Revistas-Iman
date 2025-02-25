from ninja import NinjaAPI

# Una única instancia de API
api = NinjaAPI()

# Importa las rutas de cada app
from users.views import router as user_router
from inventory.views import router as inventory_router

# Registra los routers
api.add_router('/auth/', user_router)
api.add_router('/inventory/', inventory_router)