from dataclasses import fields
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


class AdminCreate(viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    queryset = Admin.objects.all().order_by('pk')

class AboutUsCreate(viewsets.ModelViewSet):
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all().order_by('pk')

class ClientCreate(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all().order_by('pk')

class AdminCodeCreate(viewsets.ModelViewSet):
    serializer_class = AdminCodeSerializer
    queryset = AdminCodeGen.objects.all().order_by('pk')

class ClientCodeCreate(viewsets.ModelViewSet):
    serializer_class = ClientCodeSerializer
    queryset = ClientCodeGen.objects.all().order_by('pk')

class BranchCreate(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.all().order_by('pk')

class CategoryCreate(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('pk')
    filter_fields = ('ai', 'name')

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

class NewCreate(viewsets.ModelViewSet):
    serializer_class = NewSerializer
    queryset = New.objects.all().order_by('pk')

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
        fields = ('ai', 'name', 'description', 'branch_name', 'category', 'subcategory', 
        'brand', 'gender', 'size', 'color', 'date', 'new', 'in_dollar','exchange', 'price', 
        'discount', 'discounted_price', 'new_price', 'calc_dollar', 'calc_discount')

class ProductCreate(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('pk')
    filterset_class = ProductFilter

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('pk')

class OrderCreate(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('pk')
    filter_fields = ('ai', 'name_order', 'adress', 'user_name', 'user_email', 'user_phone', 
                    'completed', 'in_process',
                    'color', 'size', 'price_order', 'quantity', 'result')

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

    columns = ['Date and Time','Address','User name', 'User email', 'User phone',
                'Name order', 'Price', 'Quantity', 'Result of Order']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Order.objects.all().values_list('date','adress','user_name', 'user_email',
                         'user_phone', 'name_order', 'price_order', 'quantity', 'result')
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
        lines.append("Adress ==> " + ord.adress)
        lines.append("Client_name ==> " + ord.user_name)
        lines.append("Client_phone_number ==> " + ord.user_phone)
        lines.append("Name of Order ==> " + ord.name_order)
        lines.append("Price of Order ==> " + str(ord.price_order))
        lines.append("Quantity of Order ==> " + str(ord.quantity))
        lines.append("Result ====> " + str(ord.result))
        lines.append(">=============Mr.X==============<")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Orders_PDF.pdf')
