# -*- coding: utf-8 -*-
from django.db import models

class book(models.Model):
	category = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	publisher = models.CharField(max_length=50)
	year = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	price = models.CharField(max_length=50)
	num = models.IntegerField()
	stock = models.IntegerField()

class card(models.Model):
	name = models.CharField(max_length=50)
	unit = models.CharField(max_length=50)
	category = models.CharField(max_length=50)

class admin(models.Model):
	password = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	tel = models.CharField(max_length=50)

class record(models.Model):
	cardid = models.IntegerField()
	bookid = models.IntegerField()
	outdate = models.CharField(max_length=50)
	indate = models.CharField(max_length=50)
	adminid = models.IntegerField()
	
