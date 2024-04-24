from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from logistics.models import Category, Product

#--- ListView
class CategoryLV(ListView):
    model = Category
    template_name = ''

class ProductLV(ListView):
    model = Product
    template_name = ''

#--- DetailView
class CategoryDV(DetailView):
    model = Category

class ProductDV(DetailView):
    model = Product
