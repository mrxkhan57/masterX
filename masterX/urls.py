from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()

router.register(r'Admin', AdminCreate)
router.register(r'AboutUs', AboutUsCreate)
router.register(r'Clients', ClientCreate)
router.register(r'AdminCode', AdminCodeCreate)
router.register(r'ClientCode', ClientCodeCreate)
router.register(r'Branch', BranchCreate)
router.register(r'Category', CategoryCreate)
router.register(r'SubCategory', SubCategoryCreate)
router.register(r'Brands', BrandCreate)
router.register(r'Genders', GenderCreate)
router.register(r'Colors', ColorCreate)
router.register(r'Sizes', SizeCreate)
router.register(r'Update', UpdateCreate)
router.register(r'New', NewCreate)
router.register(r'Messages', MessageCreate)
router.register(r'Exchange', ExchangeCreate)
router.register(r'Discount', DiscountCreate)
router.register(r'Products', ProductCreate)
router.register(r'Orders', OrderCreate)

urlpatterns = [

    path('', include(router.urls)),
    path('Branch/products/<int:pk>',ProductDetail.as_view(), name='product_detail'), 
    path('Brands/products/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('Category/products/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('Category/subcategory/<int:pk>', SubCategoryDetail.as_view(), name='subcategory_detail'),
    path('SubCategory/products/<int:pk>', ProductDetail.as_view(), name='product_detail')

]