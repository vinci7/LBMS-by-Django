# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.template import Context
from django import forms
from models import admin,book,record,card
import time
from itertools import chain

class UserForm(forms.Form): 
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

class find(forms.Form):
	key = forms.CharField(max_length=50)

class newcard(forms.Form):
	name = forms.CharField(max_length=50)
	unit = forms.CharField(max_length=50)
	category = forms.CharField(max_length=50)

class newbook(forms.Form):
	category = forms.CharField(max_length=50)
	name = forms.CharField(max_length=50)
	publisher = forms.CharField(max_length=50)
	year = forms.CharField(max_length=50)
	author = forms.CharField(max_length=50)
	price = forms.CharField(max_length=50)
	num = forms.IntegerField()

class newbooks(forms.Form):
	books = forms.CharField(max_length=200)

class bookreq(forms.Form):
	cardid = forms.IntegerField()
	bookid = forms.IntegerField()

class cardreq(forms.Form):
	cardid = forms.IntegerField()

def home(request):
	username = request.COOKIES.get('username','')
	if username:
		return HttpResponseRedirect('/library/index')
	else:
		context = {}
		return render(request, 'home.html', context)

def login(request):
	if request.method=="POST":
		uf = UserForm(request.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			flag = admin.objects.filter(name__exact=username,password__exact=password)
			if flag:
				response = HttpResponseRedirect('/library/index/')
				for item in flag:
					adminid = item.id
				print adminid
				response.set_cookie('username',username,3600)
				response.set_cookie('adminid',adminid,3600)
				return response
			else:
				return HttpResponseRedirect('/library/')
		else:
			return HttpResponse("登录失败")
	else:
		return HttpResponse("登录失败")

def index(request):
	username = request.COOKIES.get('username','')
	if username:
		print username
		content = Context({'user':username})
		return render(request, 'welcome.html' ,content)
	else:
		return HttpResponseRedirect('/library/')

def exit(request):
	response = HttpResponseRedirect('/library/index')
	response.delete_cookie('username')
	return response

def addbook(request):
	username = request.COOKIES.get('username','')
	if username:
		context = {}
		return render(request, 'addbook.html' ,context)
	else:
		return HttpResponseRedirect('/library/addbook')

def doaddbook(request):
	if request.method=="POST":
		uf = newbook(request.POST)
		if uf.is_valid():
			category = uf.cleaned_data['category']
			name = uf.cleaned_data['name']
			publisher = uf.cleaned_data['publisher']
			year = uf.cleaned_data['year']
			author = uf.cleaned_data['author']
			price = uf.cleaned_data['price']
			num = uf.cleaned_data['num']
			book.objects.create(category=category,name=name,publisher=publisher,year=year,author=author,price=price,num=num,stock=num)
			context = {'tip':'单本入库成功'}
			return render(request, 'tip.html' ,context)
		else:
			return HttpResponse('单本入库失败')
	else:
		return HttpResponse('入库失败')

def addbooks(request):
	username = request.COOKIES.get('username','')
	if username:
		context = {}
		return render(request, 'addbooks.html' ,context)
	else:
		return HttpResponseRedirect('/library/addbooks')
def doaddbooks(request):
	if request.method=="POST":
		uf = newbooks(request.POST)
		if uf.is_valid():
			books = uf.cleaned_data['books']
			books = books.strip()
			booklist = books.split('\n')
			for item in booklist:
				item = item.split(',')
				category = item[0]
				name = item[1]
				publisher = item[2]
				year = item[3]
				author = item[4]
				price = item[5]
				num = item[6]
				book.objects.create(category=category,name=name,publisher=publisher,year=year,author=author,price=price,num=num,stock=num)
			context = {'tip':'批量入库成功'}
			return render(request, 'tip.html' ,context)
		else:
			return HttpResponse('批量入库失败')
	else:
		return HttpResponse('入库失败')
	
def outbook(request):
	username = request.COOKIES.get('username','')
	if username:
		context = {}
		return render(request, 'outbook.html' ,context)
	else:
		return HttpResponseRedirect('/library/index')
def dooutbook(request):
	if request.method=="POST":
		uf = bookreq(request.POST)
		uff = cardreq(request.POST)
		if uf.is_valid():
			cardid = uf.cleaned_data['cardid']
			bookid = uf.cleaned_data['bookid']
			outdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
			adminid = request.COOKIES.get('adminid','')

			record.objects.create(cardid=cardid,bookid=bookid,outdate=outdate,adminid=adminid)
			outbook = book.objects.filter(id__exact=bookid)
			for item in outbook:
				stock = item.stock
			if stock>0:
				book.objects.filter(id__exact=bookid).update(stock=stock-1)
			else :
				context = {'tip':'此书余量不足'}
				return render(request, 'tip.html' ,context)
			context = {'tip':'借书成功'}
			return render(request, 'tip.html' ,context)
		elif uff.is_valid():
			cardid = uff.cleaned_data['cardid']
			records = record.objects.filter(cardid__exact=cardid,indate__exact='')
			ans = {}
			for item in records:
				nowbook = book.objects.filter(id__exact=item.bookid)
				ans = chain(ans,nowbook)
				content = Context({'booklist':ans})
			return render(request, 'dofindbook.html' ,content)
		else:
			context = {'tip':'借书操作失败'}
			return render(request, 'tip.html' ,context)
	else:
		context = {'tip':'借书失败'}
		return render(request, 'tip.html' ,context)

def inbook(request):
	username = request.COOKIES.get('username','')
	if username:
		context = {}
		return render(request, 'inbook.html' ,context)
	else:
		return HttpResponseRedirect('/library/inbook')

def doinbook(request):
	if request.method=="POST":
		uf = bookreq(request.POST)
		uff = cardreq(request.POST)
		if uf.is_valid():
			cardid = uf.cleaned_data['cardid']
			bookid = uf.cleaned_data['bookid']
			indate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
			
			flag = record.objects.filter(cardid__exact=cardid,bookid__exact=bookid,indate__exact='')
			for item in flag:
				recordid = item.id

			outbook = book.objects.filter(id__exact=bookid)
			for item in outbook:
				stock = item.stock

			if flag:
				book.objects.filter(id__exact=bookid).update(stock=stock+1)
				record.objects.filter(id__exact=recordid).update(indate=indate)
				context = {'tip':'还书成功'}
				return render(request, 'tip.html' ,context)
			else :
				context = {'tip':'没有这条记录'}
				return render(request, 'tip.html' ,context)
		elif uff.is_valid():
			cardid = uff.cleaned_data['cardid']
			records = record.objects.filter(cardid__exact=cardid,indate__exact='')
			ans = {}
			for item in records:
				nowbook = book.objects.filter(id__exact=item.bookid)
				ans = chain(ans,nowbook)
				content = Context({'booklist':ans})
			return render(request, 'dofindbook.html' ,content)
		else:
			context = {'tip':'还书操作失败'}
			return render(request, 'tip.html' ,context)
	else:
		context = {'tip':'还书失败'}
		return render(request, 'tip.html' ,context)

def findbook(request):
	username = request.COOKIES.get('username','')
	if username:
		context = {}
		return render(request, 'findbook.html' ,context)
	else:
		return HttpResponseRedirect('/library/findbook')

def dofindbook(request):
	if request.method=="POST":
		uf = find(request.POST)
		if uf.is_valid():
			key = uf.cleaned_data['key']
			booklist = book.objects.filter(name__contains=key)
			content = Context({'booklist':booklist})
			return render(request, 'dofindbook.html' ,content)
		else:
			booklist = book.objects.all()
			content = Context({'booklist':booklist})
			return render(request, 'dofindbook.html' ,content)
	else:
		return HttpResponse('查询失败')

def addcard(request):
	username = request.COOKIES.get('username','')
	if username:
		context = {}
		return render(request, 'addcard.html' ,context)
	else:
		return HttpResponseRedirect('/library/index')	
def doaddcard(request):
	if request.method=="POST":
		uf = newcard(request.POST)
		if uf.is_valid():
			name = uf.cleaned_data['name']
			unit = uf.cleaned_data['unit']
			category = uf.cleaned_data['category']
			card.objects.create(name=name,unit=unit,category=category)
			context = {'tip':'添加借书证成功'}
			return render(request, 'tip.html' ,context)
		else:
			return HttpResponse('添加借书证失败')
	else:
		return HttpResponse('添加失败')

def showcard(request):
	username = request.COOKIES.get('username','')
	if username:
		cardlist = card.objects.all()
		content = Context({'cardlist':cardlist})
		return render(request, 'card.html' ,content)
	else:
		return HttpResponseRedirect('/library/card')

def deletecard(request):
	if request.method=="POST":
		uf = cardreq(request.POST)
		if uf.is_valid():
			print 'hello'
			cardid = uf.cleaned_data['cardid']
			card.objects.get(id__exact=cardid).delete()
			context = {'tip':'删除借书证成功'}
			return render(request, 'tip.html' ,context)
		else:
			return HttpResponse('删除借书证失败')
	else:
		return HttpResponse('删除失败')







