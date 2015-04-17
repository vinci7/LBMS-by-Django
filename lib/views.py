# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect
def home(request):
    return HttpResponseRedirect('/library/index')