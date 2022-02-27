from rest_framework import routers
from django.urls import path, include
from .views import *
from . import views

router = routers.DefaultRouter()

router.register(r'ADS', AdsCreate)
router.register(r'AboutUs', AboutUsCreate)
router.register(r'Brands', BrandCreate)
router.register(r'Category', CategoryCreate)
router.register(r'Clients', ClientCreate)
router.register(r'ClientCode', ClientCodeCreate)
router.register(r'Colors', ColorCreate)
router.register(r'Discount', DiscountCreate)
router.register(r'Exchange', ExchangeCreate)
router.register(r'Genders', GenderCreate)
router.register(r'Location', LocationCreate)
router.register(r'Messages', MessageCreate)
router.register(r'Orders', OrderCreate)
router.register(r'Products', ProductCreate)
router.register(r'Sizes', SizeCreate)
router.register(r'SuperCategory', SuperCreate)
router.register(r'SubCategory', SubCategoryCreate)
router.register(r'Update', UpdateCreate)
router.register(r'Vendor', VendorCreate)
router.register(r'Visited', VisitCreate)

urlpatterns = [

    path('', include(router.urls)),
    path('Vendor/products/<int:pk>',ProductDetail.as_view(), name='product_detail'), 
    path('Brand/products/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('SuperCategory/category/<int:pk>', CategoryDetail.as_view(), name='category_detail'),
    path('SuperCategory/products/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('Category/products/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('Category/subcategory/<int:pk>', SubCategoryDetail.as_view(), name='subcategory_detail'),
    path('SubCategory/products/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('ClientDATA/', views.ClientIPView.as_view(), name='ClientDATA'),
]