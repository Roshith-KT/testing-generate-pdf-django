from django.urls import path
from . import views
app_name="pdfapp"
urlpatterns =[
    path('',views.index,name="index"),
    path('pdf_file/<int:id>',views.generate_pdf_file,name="pdf_file"),
]