from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View

class TopView(View):
    def get(self, request):
        return render()