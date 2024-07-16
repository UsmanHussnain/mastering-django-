from django.contrib.auth import login , logout , get_user_model
from django.shortcuts import render, redirect , get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import User 
from .forms import SignupForm, CustomAuthenticationForm
from .forms import ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm 
User = get_user_model()

@login_required(login_url='login')
def index_view(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html' )



def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                login(request, user)
                messages.success(request, f'Welcome, {user.first_name +" "+ user.last_name}!')
                return redirect('dashboard') 
            else:
                messages.error(request, 'You must verify your email address before logging in.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']

            # if User.objects.filter(email=email).exists():
            #     messages.error(request, 'Email Already Exist')
            #     return render(request, 'signup.html', {'form': form})

            # if User.objects.filter(username=username).exists():
            #     messages.error(request, 'Username Already Exist')
            #     return render(request, 'signup.html', {'form': form})
            try:
                existing_email_user = User.objects.get(email=email)
                messages.error(request, 'Email Already Exist')
                return render(request, 'signup.html', {'form': form})

            except User.DoesNotExist:
                pass 
            try:
                existing_username_user = User.objects.get(username=username)
                messages.error(request, 'Username Already Exist')
                return render(request, 'signup.html', {'form': form})

            except User.DoesNotExist:
                pass  

            user = form.save(commit=False)
            user.is_verified = False  
            user.save()

            send_email_verification(user)
            messages.success(request, 'Account created successfully! Please verify your email address.')
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def send_email_verification(user):
    subject = 'Verify Your Email Address'
    token = user.generate_verification_token()
    message = f'Hi {user.first_name},\n\nPlease click the link below to verify your email address:\n\n' \
              f'{settings.BASE_URL}/verify-email/{token}/\n\nThank you!'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

def verify_email(request, token):
    user = get_object_or_404(User, verification_token=token)

    if not user.is_verified:
        user.is_verified = True
        user.save()
        messages.success(request, 'Your email has been verified successfully. You can now log in.')
    else:
        messages.info(request, 'Your email is already verified.')

    return redirect('login')



@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile_detail(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile_detail.html', context)



@login_required(login_url='login')
def editProfile(request):
    user = request.user  

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update session with new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile-detail')  # Replace with the name of your profile detail URL
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})