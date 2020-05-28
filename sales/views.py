from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def list_orders(request):
    return HttpResponse("订单列表")


