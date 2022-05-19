from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *  
from django.http import HttpResponse
import xlwt
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django_filters import rest_framework as filters




class AdsCreate(viewsets.ModelViewSet):
    serializer_class = AdsSerializer
    queryset = Ads.objects.all().order_by('-pk')

class AboutUsCreate(viewsets.ModelViewSet):
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all().order_by('pk')

class ClientCreate(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all().order_by('pk')

class ClientCodeCreate(viewsets.ModelViewSet):
    serializer_class = ClientCodeSerializer
    queryset = ClientCodeGen.objects.all().order_by('pk')

class ClientIPView(generics.ListCreateAPIView):
    queryset = ClientIPLogList.objects.all()
    serializer_class = LoglistSerializer

    def perform_create(self, serializer):
        serializer.save()

class ClientIPDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClientIPLogList.objects.all()
    serializer_class = LoglistSerializer

class VendorCreate(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all().order_by('pk')

class SuperCreate(viewsets.ModelViewSet):
    serializer_class = SuperSerializer
    queryset = SuperCategory.objects.all().order_by('pk')

class CategoryCreate(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('pk')
    filter_fields = ('ai', 'name')

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('pk')

class SubCategoryCreate(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all().order_by('pk')

class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all().order_by('pk')
    
class BrandCreate(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all().order_by('pk')

class GenderCreate(viewsets.ModelViewSet):
    serializer_class = GenderSerializer
    queryset = Gender.objects.all().order_by('pk')
    
class ColorCreate(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all().order_by('pk')

class SizeCreate(viewsets.ModelViewSet):
    serializer_class = SizeSerializer
    queryset = Size.objects.all().order_by('pk')

class UpdateCreate(viewsets.ModelViewSet):
    serializer_class = UpdateSerializer
    queryset = Update.objects.all().order_by('pk')

class VisitCreate(viewsets.ModelViewSet):
    serializer_class = VisitedSerializer
    queryset = Visited.objects.all()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.visit = obj.visit + 1
        obj.save(update_fields=("visit", ))
        return super().retrieve(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     for obj in queryset:
    #         obj.visit = obj.visit + 1
    #         obj.save(update_fields=("visit", ))
    #     return super().list(request, *args, **kwargs)

class LocationCreate(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all().order_by('pk')

class MessageCreate(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all().order_by('pk')
    filter_fields = ('question_text', 'answer_text', 'user_phone', 'user_email')

class ExchangeCreate(viewsets.ModelViewSet):
    serializer_class = ExchangeSerializer
    queryset = Exchange.objects.all().order_by('pk')

class DiscountCreate(viewsets.ModelViewSet):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all().order_by('pk')

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ('product_id','name','description','vendor_name','supercategory','category','subcategory', 
        'brand','location','gender','barcode','size','color','date','new','in_dollar','exchange','price', 
        'discount','discounted_price','new_price','calc_dollar','calc_discount')

class ProductCreate(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-pk')
    filterset_class = ProductFilter

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.visited = obj.visited + 1
        obj.save(update_fields=("visited", ))
        return super().retrieve(request, *args, **kwargs)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('pk')

class ProductIPView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save()

class ProductIPDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderCreate(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('pk')
    filter_fields = ('order_id', 'name_order', 'vendor_name','adress', 'user_name', 
                    'user_email', 'user_phone', 
                    'completed', 'in_process',
                    'color', 'size', 'price_order', 'quantity', 'result')

    #def retrieve(self, request, *args, **kwargs, instance):
    #    obj = self.get_object()
    #    obj.order_id = generate_order_id()
    #    obj.save(update_fields=("order_id", ))
    #
    #    return super().retrieve(request, *args, **kwargs)

def index(request):   
    return render(request,"index.html")

def export_orders(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="order.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Order')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ID','Date and Time','Address','Vendor name','User name', 'User email', 'User phone',
                'Name order', 'Order_ID','Price', 'Quantity', 'Result of Order']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Order.objects.all().values_list('pk','date','adress','vendor_name','user_name', 'user_email',
                         'user_phone', 'name_order', 'order_id','price_order', 'quantity', 'result')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def view_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)
    orders = Order.objects.all()
    lines = []
    for ord in orders:
        lines.append("Date ==> " + ord.date)
        lines.append("Order_ID ==>" + ord.order_id)
        lines.append("Adress ==> " + ord.adress)
        lines.append("Vendor_name ==> " + ord.vendor_name)
        lines.append("Client_name ==> " + ord.user_name)
        lines.append("Client_phone_number ==> " + ord.user_phone)
        lines.append("Name of Order ==> " + ord.name_order)
        lines.append("Price of Order ==> " + str(ord.price_order))
        lines.append("Quantity of Order ==> " + str(ord.quantity))
        lines.append("Result ====> " + str(ord.result))
        lines.append("")
        lines.append("Alyjy_Goly___________________")
        lines.append(">=============< Mr.X >==============<")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Orders_PDF.pdf')
