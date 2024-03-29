from rest_framework import serializers
from .models import *

class AdsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ads
        fields = ['pk', 'name', 'description', 'spcategory','photo', 'url']

    def to_representation(self, instance):
        rep = super(AdsSerializer, self).to_representation(instance)
        rep['spcategory'] = instance.spcategory.name
        return rep

class AboutUsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['pk', 'website', 'email', 'phone1', 'phone2', 'phone3', 'file','url']
        
class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['pk', 'name', 'address', 'number', 'url']

class ClientCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientCodeGen
        fields = ['pk', 'phone_number', 'code', 'url']

class LoglistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientIPLogList
        fields = ('pk', 'date', 'client_ip')
        read_only_fields = ('date', 'client_ip')

    def create(self, validated_data):
        validated_data['client_ip'] = self.context.get('request').META.get('HTTP_X_FORWARDED_FOR')
        if validated_data['client_ip']:
            validated_data['client_ip'] = validated_data['client_ip'].split(',')[0]
        else:
            validated_data['client_ip'] = self.context.get('request').META.get('REMOTE_ADDR')
        #validated_data['client_ip'] = self.context.get('request').META.get('REMOTE_ADDR')
        #validated_data['client_ip'] = self.context.get('request').META.get('HTTP_X_FORWARDED_FOR', self.context.get('request').META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        return ClientIPLogList.objects.create(**validated_data)

class VendorSerializer(serializers.HyperlinkedModelSerializer):
    supercategory = serializers.HyperlinkedRelatedField(many = True, read_only = True,view_name='supcategory_detail')
    
    class Meta:
        model = Vendor
        fields = ['pk','vendor_name','admin_name','username','passwd','phone_number',
                    'address','photo','supercategory','url']

#class DynamicFieldsSuperCategorySerializer(serializers.ModelSerializer):
#    def __init__(self, *args, **kwargs):
#        # Don't pass the 'fields' arg up to the superclass
#        fields = kwargs.pop('fields', None)
#
#        # Instantiate the superclass normally
#        super().__init__(*args, **kwargs)
#
#        if fields is not None:
#            # Drop any fields that are not specified in the `fields` argument.
#            allowed = set(fields)
#            existing = set(self.fields)
#            for field_name in existing - allowed:
#                self.fields.pop(field_name)

class SuperSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many = True, read_only = True,
                                                        view_name='product_detail')
    category = serializers.HyperlinkedRelatedField(many = True, read_only = True,
                                                        view_name='category_detail')
    #vendors =  VendorSerializer(many=True)                                                                                     
    class Meta:
        model = SuperCategory
        fields = ['pk','ai','name','photo','category','products','url']

    #def create(self, validated_data):
    #    vendors_data = validated_data.pop('vendors')
    #    vendor = SuperCategory.objects.create(**validated_data)
    #    for vendor_data in vendors_data:
    #        Vendor.objects.create(vendor=vendor, **vendor_data)
    #    return vendor

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many = True, read_only = True,
                                                        view_name='product_detail')
    subcategory = serializers.HyperlinkedRelatedField(many = True, read_only = True, 
                                                        view_name='subcategory_detail')
    
    class Meta:
        model = Category
        fields = ['pk', 'ai', 'name', 'super','photo', 'url', 'subcategory', 'products']

    def to_representation(self, instance):
        rep = super(CategorySerializer, self).to_representation(instance)
        rep['super'] = instance.super.name
        return rep

class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many = True, read_only = True,
                                                        view_name='product_detail')

    class Meta:
        model = SubCategory
        fields = ['pk','category','name','photo','url','products']

    def to_representation(self, instance):
        rep = super(SubCategorySerializer, self).to_representation(instance)
        rep['category'] = instance.category.name
        return rep

class BrandSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many = True, read_only = True,
                                                        view_name='product_detail')
    
    class Meta:
        model = Brand
        fields = ['pk', 'name', 'photo', 'url', 'products']

class GenderSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many = True, read_only = True,
                                                        view_name='product_detail')

    class Meta:
        model = Gender
        fields = ['pk', 'name', 'url', 'products']

class ColorSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many = True, read_only = True,
                                                        view_name='product_detail')
    class Meta:
        model = Color
        fields = ['pk', 'name', 'url', 'products']

class SizeSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(many = True, read_only = True,
                                                        view_name='product_detail')
    class Meta:
        model = Size
        fields = ['pk', 'name', 'url', 'products']

class UpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Update
        fields = ['pk', 'url', 'update_product']

class VisitedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visited
        fields = ['visit', 'url']

    #def to_representation(self, instance):
    #    rep = super(VisitedSerializer, self).to_representation(instance)
    #    rep['visit'] = str(rep['visit']).rjust(5, '0')
    #    return rep
class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ['pk', 'name', 'url']

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['pk', 'question_text', 'answer_text', 'date', 'user_phone', 'user_email','url']

class ExchangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exchange
        fields = ['pk', 'exchange', 'url']

class DiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Discount
        fields = ['pk', 'discount', 'url']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['pk','supercategory','category','subcategory','brand','vendor_name','location','product_id',
                'date','name','description','barcode','stock_number','visited','in_dollar','exchange', 
                'price', 'discount','discounted_price','new_price','calc_dollar','calc_discount','color',
                'size','gender','new','free_delivery','photo1','photo2','photo3','photo4','ip_pro','url']
        read_only_fields = ('ip_pro','discounted_price','new_price','date','visited')

    def to_representation(self, instance):
        rep = super(ProductSerializer, self).to_representation(instance)
        rep['vendor_name'] = instance.vendor_name.vendor_name
        rep['supercategory'] = instance.supercategory.name
        rep['category'] = instance.category.name
        rep['subcategory'] = instance.subcategory.name
        rep['brand'] = instance.brand.name
        rep['color'] = instance.color.name
        rep['size'] = instance.size.name
        rep['gender'] = instance.gender.name
        rep['exchange'] = instance.exchange.exchange
        rep['discount'] = instance.discount.discount
        rep['location'] = instance.location.name
        return rep

    def create(self, validated_data):
        validated_data['ip_pro'] = self.context.get('request').META.get('HTTP_X_FORWARDED_FOR')
        if validated_data['ip_pro']:
            validated_data['ip_pro'] = validated_data['ip_pro'].split(',')[0]
        else:
            validated_data['ip_pro'] = self.context.get('request').META.get('REMOTE_ADDR')
        return Product.objects.create(**validated_data)

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['pk','order_id','name_order','vendor_name','adress', 'user_name', 'user_email', 
                        'user_phone', 'order_note','completed', 'in_process', 'cancelled',
                'color', 'size', 'date', 'price_order', 'quantity', 'result', 'photo', 'url']
        read_only_fields = ['date', 'order_id']
    
    #def to_representation(self, instance):
    #    rep = super(OrderSerializer, self).to_representation(instance)
    #    rep['order_id'] = str(rep['order_id']).rjust(10, '0')
    #    return rep