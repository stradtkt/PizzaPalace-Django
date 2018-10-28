# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect
import cart
from .models import *
import bcrypt



def index(request):
    return render(request, 'palace/index.html')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    if len(user) > 0:
        is_pass = bcrypt.checkpw(password.encode('utf-8'), user[0].password.encode('utf-8'))
        if is_pass:
            request.session['id'] = user[0].id
            return redirect('/')
        else:
            messages.error(request, "Incorrect email and/or password")
            return redirect('/')
    else:
        messages.error(request, "User does not exist")
    return redirect('/')

def register(request):
    errors = User.objects.validate_user(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_pw)
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def register_page(request):
    return render(request, 'palace/register-page.html')

def login_page(request):
    return render(request, 'palace/login-page.html')

def order_now(request):
    return render(request, 'palace/order-now.html')

def process_temp_address(request):
    errors = DeliveryTempAddress.objects.validate_temp_address(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/')
    else:
        street_address = request.POST['street_address']
        apt_ste_floor = request.POST['apt_ste_floor']
        number = request.POST['number']
        zip_code = request.POST['zip_code']
        DeliveryTempAddress.objects.create(street_address=street_address, apt_ste_floor=apt_ste_floor, number=number, zip_code=zip_code)
        return redirect('/menu')


#  Cart Commands

def add_to_cart(request, item_id, quantity):
    item = Item.objects.get(id=item_id)
    cart = Cart(request)
    cart.add(item, item.price, quantity)

def remove_from_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    cart = Cart(request)
    cart.remove(item)