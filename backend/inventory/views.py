
from ninja import Router
from typing import List
from .schemas import ProductIn, ProductOut
from .models import Product
from users.views import auth

router = Router(
    
)
@router.get('/products', response=List[ProductOut], auth=auth)
def list_products(request):
    return Product.objects.all()

@router.post('/products', response=ProductOut, auth=auth)
def create_product(request, data: ProductIn):
    product = Product.objects.create(**data.dict())
    return product

@router.get('/products/{product_id}', response=ProductOut, auth=auth)
def get_product(request, product_id: int):
    return Product.objects.get(id=product_id)

@router.put('/products/{product_id}', response=ProductOut, auth=auth)
def update_product(request, product_id: int, data: ProductIn):
    product = Product.objects.get(id=product_id)
    for field, value in data.dict().items():
        setattr(product, field, value)
    product.save()
    return product

@router.delete('/products/{product_id}', auth=auth)
def delete_product(request, product_id: int):
    Product.objects.get(id=product_id).delete()
    return {'success': True}
