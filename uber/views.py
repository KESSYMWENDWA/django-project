from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Ride, Payment, CustomUser
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import models

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')  # Stay on the sign-up page if passwords don't match
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'signup.html')  # Stay on the sign-up page if username is taken
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            return render(request, 'signup.html')  # Stay on the sign-up page if email is taken

        # If all validations pass, create and save the user
        user = CustomUser(username=username, email=email, password=make_password(password))
        user.save()
        messages.success(request, 'Account created successfully! Please sign in.')
        return redirect('signin')  # Redirect to the sign-in page after successful sign-up
    
    return render(request, 'signup.html')  # Render the sign-up page on GET request

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in and redirect to the order page
            login(request, user)
            return redirect('booking')  # Redirect to the order page or any other page you have
        else:
            # Display an error message and reload the sign-in page
            messages.error(request, 'Invalid username or password.')
            return render(request, 'signin.html')

    return render(request, 'signin.html')

def booking(request):
    if request.method == 'POST':
        current_location = request.POST['current_location']
        destination = request.POST['destination']
        ride_type = request.POST['ride_type']
        
        # Calculate price based on ride type
        price = 0
        if ride_type == 'Economy Car':
            price = 15.00
        elif ride_type == 'Motorcycle':
            price = 10.00
        elif ride_type == 'Luxury Car':
            price = 25.00
        elif ride_type == 'Ride Car':
            price = 20.00
        elif ride_type == 'Blue Car':
            price = 35.00
        elif ride_type == 'Womenonly Car':
            price = 30.00
        
        # Save the booking to the database
        user = request.user
        ride = Ride(
            user=user,
            current_location=current_location,
            destination=destination,
            ride_type=ride_type,
            price=price,
        )
        ride.save()
        
        # Redirect to payment page with ride_id
        return redirect('payment', ride_id=ride.id)
    
    return render(request, 'booking.html')

def payment_view(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    if request.method == 'POST':
        mpesa_code = request.POST.get('mpesa_code')
        amount = ride.price  # Assuming amount is based on ride price

        # Create and save the Payment object
        payment = Payment(
            user=request.user,
            ride=ride,
            mpesa_code=mpesa_code,
            amount=amount
        )
        payment.save()

        return redirect('receipt', payment_id=payment.id)  # Redirect to a success page or another appropriate view

    return render(request, 'payment.html', {'ride': ride})

def receipt_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'receipt.html', {'payment': payment})