from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Service,Subscription
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import ServiceForm,SubscriptionForm,signin
import random
from django.views import View
from django.http import HttpResponse
import razorpay
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .backends import LoginModelBackend
from .decorators import custom_login_required
from .models import login


# Create your views here.

@custom_login_required
def home(request):
    services = Service.objects.filter(active=True)
    return render(request, 'home.html',{'services':services})



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Generate OTP
            otp = random.randint(1000, 9999)
            
            # Save user data in session
            request.session['username'] = username
            request.session['email'] = email
            request.session['password'] = password
            request.session['otp'] = otp

            # Send OTP via email
            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                return render(request, 'register.html', {'form': form, 'error': f'Error sending email: {e}'})

            return redirect('otp_verification')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.make_password(form.cleaned_data['password'])
#             user.is_active = False
#             user.save()

#             otp = random.randint(100000, 999999)
#             # request.session['otp'] = otp
#             # request.session['user_id'] = user.id
#             request.session['username'] = username
#             request.session['email'] = email
#             request.session['password'] = password
#             request.session['otp'] = otp

#             send_mail(
#                 'Your OTP Code',
#                 f'Your OTP code is {otp}',
#                 'your_email@gmail.com',
#                 [user.email],
#                 fail_silently=False,
#             )
#             return redirect('otp_verification')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'register.html', {'form': form})

# def otp_verification(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         if otp == str(request.session['otp']):
#             user_id = request.session['user_id']
#             user = login.objects.get(id=user_id)
#             user.is_active = True
#             user.save()
#             del request.session['otp']
#             del request.session['user_id']
#             return redirect('login')
#     return render(request, 'otp_verification.html')

# def otp_verification(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
        
#         # Check OTP
#         if otp == str(request.session.get('otp')):
#             username = request.session.get('username')
#             email = request.session.get('email')
#             password = request.session.get('password')

#             if username and email and password:
#                 try:
#                     # Create or update the user
#                     user, created = login.objects.get_or_create(
#                         username=username,
#                         defaults={
#                             'email': email,
#                             'password': make_password(password),
#                         }
#                     )
                    
#                     # If user was created, set is_active to True
#                     if created:
#                         user.is_active = True
#                         user.save()
                    
#                     # Clean up session data
#                     del request.session['otp']
#                     del request.session['username']
#                     del request.session['email']
#                     del request.session['password']

#                     return redirect('login')  # Redirect to the login page or dashboard
#                 except Exception as e:
#                     return render(request, 'otp_verification.html', {'error': f'Error creating or updating user: {e}'})
#             else:
#                 return render(request, 'otp_verification.html', {'error': 'Session data missing.'})
#         else:
#             return render(request, 'otp_verification.html', {'error': 'Invalid OTP.'})

#     return render(request, 'otp_verification.html')


def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        
        # Check OTP
        if otp == str(request.session.get('otp')):
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')

            if username and email and password:
                try:
                    # Create or update the user
                    user, created = login.objects.get_or_create(
                        username=username,email=email,password=password
                    )
                    
                    # If user was created, set is_active to True
                    if created:
                        user.is_active = True
                        user.save()
                    
                    # Clean up session data
                    del request.session['otp']
                    del request.session['username']
                    del request.session['email']
                    del request.session['password']

                    return redirect('login')  # Redirect to the login page or dashboard
                except Exception as e:
                    return render(request, 'otp_verification.html', {'error': f'Error creating or updating user: {e}'})
            else:
                return render(request, 'otp_verification.html', {'error': 'Session data missing.'})
        else:
            return render(request, 'otp_verification.html', {'error': 'Invalid OTP.'})

    return render(request, 'otp_verification.html')




class log(View):
    
    def get(self,request):
        form = signin()
        ctx={
             'form': form
        }
        return render(request,'login.html',ctx)
    
    def post(self, request):
        form = signin(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            backend = LoginModelBackend()
            user = backend.authenticate(request, username=username, password=password)
            if user is not None:
                request.session['user_id'] = user.id  
                request.session['username'] = user.username
                return redirect('home')
            else:
                return HttpResponse('Invalid login credentials')
        return render(request, 'login.html', {'form': form})
    
    # def post(self,request):
    #     form = signin(request.POST)
    #     if form.is_valid():
    #         return redirect('home')
    #     else:
    #         return HttpResponse('Invalid Details')

def user_logout(request):
    logout(request)
    return redirect('login')


@custom_login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service_detail.html', {'service': service})


@custom_login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'service_form.html', {'form': form})

@custom_login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'service_form.html', {'form': form})

@custom_login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'service_confirm_delete.html', {'service': service})



# @custom_login_required
# def subscription_create(request):
#     if request.method == "POST":
#         form = SubscriptionForm(request.POST)
#         if form.is_valid():
#             subscription = form.save(commit=False)
#             subscription.payment_status = 'Pending'
#             subscription.save()

#             print("RAZORPAY_API_KEY:", settings.RAZORPAY_API_KEY)
#             print("RAZORPAY_API_SECRET:", settings.RAZORPAY_API_SECRET)

#             # Initialize Razorpay client
#             client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

#             # Amount is in paisa (hence * 100)
#             amount = int(subscription.service.price * 100)
#             currency = 'INR'

#             # Create an order in Razorpay
#             order = client.order.create({'amount': amount, 'currency': currency, 'payment_capture': 1})

#             # Save the order ID in the subscription model
#             subscription.payment_id = order['id']
#             subscription.save()

#             # Render payment page
#             context = {
#                 'order': order,
#                 'razorpay_key': settings.RAZORPAY_API_KEY,
#                 'subscription': subscription,
#             }
#             return render(request, 'razorpay_payment.html', context)
#     else:
#         form = SubscriptionForm()
#     return render(request, 'subscription_form.html', {'form': form})



# @custom_login_required
# def subscription_create(request):
#     if request.method == "POST":
#         form = SubscriptionForm(request.POST)
#         if form.is_valid():
#             subscription = form.save(commit=False)
#             subscription.payment_status = 'Pending'
#             subscription.save()

#             try:
#                 # Print Razorpay API credentials for debugging purposes
#                 print("RAZORPAY_API_KEY:", settings.RAZORPAY_API_KEY)
#                 print("RAZORPAY_API_SECRET:", settings.RAZORPAY_API_SECRET)

#                 # Initialize Razorpay client
#                 client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

#                 # Amount is in paisa (hence * 100)
#                 amount = int(subscription.service.price * 100)
#                 currency = 'INR'

#                 # Create an order in Razorpay
#                 order = client.order.create({'amount': amount, 'currency': currency, 'payment_capture': 1})

#                 # Save the order ID in the subscription model
#                 subscription.payment_id = order['id']
#                 subscription.save()

#                 # Render payment page
#                 context = {
#                     'order': order,
#                     'razorpay_key': settings.RAZORPAY_API_KEY,
#                     'subscription': subscription,
#                 }
#                 return render(request, 'razorpay_payment.html', context)

#             except razorpay.errors.BadRequestError as e:
#                 # Handle authentication error or other bad requests
#                 print(f"Razorpay BadRequestError: {e}")
#                 return HttpResponse("There was an issue with your payment request. Please try again later.", status=500)

#             except Exception as e:
#                 # Handle any other exceptions
#                 print(f"An unexpected error occurred: {e}")
#                 return HttpResponse("An unexpected error occurred. Please try again later.", status=500)
#         else:
#             return HttpResponse("Invalid form data", status=400)

#     else:
#         form = SubscriptionForm()
#     return render(request, 'subscription_form.html', {'form': form})

@custom_login_required
def subscription_create(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.payment_status = 'Pending'
            subscription.save()

            print("RAZORPAY_API_KEY:", settings.RAZORPAY_API_KEY)
            print("RAZORPAY_API_SECRET:", settings.RAZORPAY_API_SECRET)

            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

            # Amount is in paisa (hence * 100)
            amount = int(subscription.service.price * 100)
            charges = int(subscription.service.tax / 100 * amount)
            Total = amount+charges
            currency = 'INR'

            # Create an order in Razorpay
            order = client.order.create({'amount': Total, 'currency': currency, 'payment_capture': 1})

            # Save the order ID in the subscription model
            subscription.payment_id = order['id']
            subscription.save()

            # Render payment page
            context = {
                'order': order,
                'razorpay_key': settings.RAZORPAY_API_KEY,
                'subscription': subscription,
            }
            return render(request, 'razorpay_payment.html', context)
    else:
        form = SubscriptionForm()
    return render(request, 'subscription_form.html', {'form': form})

# def subscription_create(request):
#     service = Service.objects.filter(active = True)
#     if request.method == 'POST':
#         form = SubscriptionForm(request.POST)
#         if form.is_valid():
#             subscription = form.save(commit=False)
#             subscription.user = request.user
#             subscription.Service = service
#             subscription.amount = service.price + (service.price * service.tax / 100)
#             subscription.save()

#             client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#             payment = client.order.create({'amount': int(subscription.amount * 100), 'currency': 'INR', 'payment_capture': '1'})

#             subscription.transaction_id = payment['id']
#             subscription.save()

#             return render(request, 'subscription_confirm.html', {'subscription': subscription, 'payment': payment, 'razorpay_key': settings.RAZORPAY_KEY_ID})
#     else:
#         form = SubscriptionForm()
#     return render(request, 'subscription_form.html', {'form': form, 'service': service})

@csrf_exempt
@custom_login_required
def subscription_callback(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        subscription = get_object_or_404(Subscription, transaction_id=request.POST.get('razorpay_order_id'))

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.payment.fetch(payment_id)

        if payment['status'] == 'captured':
            subscription.payment_status = 'Success'
        else:
            subscription.payment_status = 'Failed'
        subscription.save()

        return redirect('home')

