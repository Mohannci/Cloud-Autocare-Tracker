from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .dynamodb import create_user, get_user, create_vehicle, get_vehicles, update_vehicle, delete_vehicle, create_maintenance_record, get_maintenance_records
from decimal import Decimal
import boto3
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

s3 = boto3.client('s3',
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                  aws_session_token=settings.AWS_SESSION_TOKEN)

sns = boto3.client('sns',
                   region_name=settings.AWS_REGION,
                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                   aws_session_token=settings.AWS_SESSION_TOKEN)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = make_password(form.cleaned_data['password1'])
            create_user(username, password)
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_data = get_user(username)
            if user_data and check_password(password, user_data['password_hash']):
                user = form.get_user()
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    vehicles = get_vehicles(request.user.username)
    return render(request, 'home.html', {'vehicles': vehicles})

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        vehicle_name = request.POST['vehicle_name']
        model = request.POST['model']
        year = request.POST['year']
        image = request.FILES.get('image')
        
        image_url = None
        if image:
            s3.upload_fileobj(image, settings.AWS_S3_BUCKET, image.name)
            image_url = f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{image.name}"
        
        vehicle_id = create_vehicle(request.user.username, vehicle_name, model, year)
        sns.publish(TopicArn=settings.AWS_SNS_TOPIC_ARN, Message=f"Vehicle {vehicle_name} {model} added.")
        return redirect('home')
    return render(request, 'add_vehicle.html')

@login_required
def edit_vehicle(request, vehicle_id):
    if request.method == 'POST':
        vehicle_name = request.POST['vehicle_name']
        model = request.POST['model']
        year = request.POST['year']
        update_vehicle(vehicle_id, request.user.username, vehicle_name, model, year)
        return redirect('home')
    vehicles = get_vehicles(request.user.username)
    vehicle = next((v for v in vehicles if v['vehicle_id'] == vehicle_id), None)
    if vehicle is None:
        return redirect('home')
    return render(request, 'edit_vehicle.html', {'vehicle': vehicle})

@login_required
def delete_vehicle_view(request, vehicle_id):
    if request.method == 'POST':
        delete_vehicle(vehicle_id, request.user.username)
        return redirect('home')
    return render(request, 'delete_vehicle.html', {'vehicle_id': vehicle_id})

@login_required
def maintenance(request):
    if request.method == 'POST':
        vehicle_id = request.POST['vehicle_id']
        service_date = request.POST['service_date']
        description = request.POST['description']
        cost = Decimal(request.POST['cost'])
        create_maintenance_record(vehicle_id, service_date, description, cost)
        return redirect('maintenance')
    vehicles = get_vehicles(request.user.username)
    vehicle_id = request.GET.get('vehicle_id', vehicles[0]['vehicle_id'] if vehicles else None)
    maintenance_records = get_maintenance_records(vehicle_id) if vehicle_id else []
    return render(request, 'maintenance.html', {'vehicles': vehicles, 'maintenance_records': maintenance_records, 'selected_vehicle_id': vehicle_id})

@login_required
@login_required
def service_history(request):
    vehicles = get_vehicles(request.user.username)
    # Fetch all maintenance records and filter in the template
    all_maintenance_records = []
    for vehicle in vehicles:
        records = get_maintenance_records(vehicle['vehicle_id'])
        all_maintenance_records.extend(records)
    return render(request, 'service_history.html', {'vehicles': vehicles, 'maintenance_records': all_maintenance_records})
@login_required
def appointments(request):
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        vehicle_name = request.POST['vehicle_name']
        # Send email notification via SNS
        subject = f'New Appointment Booking - {request.user.username}'
        message = f'Appointment booked on {date} at {time} for vehicle: {vehicle_name} by {request.user.username}.'
        sns.publish(TopicArn=settings.AWS_SNS_TOPIC_ARN, Message=message, Subject=subject)
        return redirect('appointments')
    return render(request, 'appointments.html')

@login_required
def contact(request):
    return render(request, 'contact.html')