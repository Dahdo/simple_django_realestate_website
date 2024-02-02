from .helpers import get_common_data
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def estate(request):
    # Fetch distinct values for filters
    common_data = get_common_data()
    properties = Property.objects.all()
    context = {'properties': properties,
               **common_data}
    return render(request, 'estate/estate.html', context=context)


def for_sale(request):
    properties_for_sale = Property.objects.filter(status='for_sale')
    context = {'properties': properties_for_sale}
    return render(request, 'estate/for_sale.html', context=context)


def for_rent(request):
    properties_for_sale = Property.objects.filter(status='for_rent')
    context = {'properties': properties_for_sale}
    return render(request, 'estate/for_rent.html', context=context)


def submit_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            # Save the property and location
            property = form.save(commit=False)
            property.location.save()

            # Associate the property with the user
            user_profile = UserProfile.objects.get(user=request.user)
            property.user_profile = user_profile
            property.save()

            # Associate it with a new order
            new_order = Order.objects.create(user_profile=user_profile, completed=True, orderItem=property)
            new_order.save()

            messages.success(request, 'Property submitted successfully', extra_tags='success')
            return redirect('property_detail', pk=property.pk)
        return render(request, 'estate/submit_property.html', {'form': form})  # In case the form is invalid
    else:
        form = PropertyForm()
        return render(request, 'estate/submit_property.html', {'form': form})


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    user_profile = property.user_profile
    custom_user = user_profile.user
    data = {'property': property, 'user_profile': user_profile, 'custom_user': custom_user}
    return render(request, 'estate/property_detail.html', context=data)


def about(request):
    return render(request, 'estate/about.html')


def contact(request):
    return render(request, 'estate/contact.html')


def login_request(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.", extra_tags='success')
                return redirect(reverse_lazy('estate'))
            else:
                messages.error(request, "Invalid username or password.", extra_tags='invalid-form')
        else:
            messages.error(request, "Invalid username or password. - invalid form", extra_tags='invalid-form')
    form = CustomAuthenticationForm(request)
    return render(request, 'estate/registration/login.html', {'login_form': form})


def register_request(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Check if bio and profile_pic are provided in the form
            bio = form.cleaned_data.get('bio')
            profile_pic = form.cleaned_data.get('profile_pic')

            # If provided, save them to UserProfile
            if bio or profile_pic:
                user_profile = UserProfile.objects.get(user=user)
                user_profile.bio = bio
                user_profile.profile_pic = profile_pic
                user_profile.save()

            messages.success(request, 'Registration successful!', extra_tags='success')
            return redirect(reverse_lazy('estate'))
        messages.error(request, "Unsuccessful registration. Invalid information.", extra_tags='invalid-form')
        # In case it is invalid, repopulate the form
        return render(request, 'estate/registration/register.html', context={'registration_form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'estate/registration/register.html', context={'registration_form': form})


def logout_request(request):
    logout(request)
    messages.success(request, 'You have been logged out.', extra_tags='success')
    return redirect(reverse_lazy('estate'))


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    context = {'profile': profile}
    return render(request, 'estate/registration/profile.html', context=context)


@login_required
def profile_edit(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

            # Check if bio and profile_pic are provided in the form
            bio = form.cleaned_data.get('bio')
            profile_pic = form.cleaned_data.get('profile_pic')

            # If provided, save them to UserProfile
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.bio = bio
            user_profile.profile_pic = profile_pic
            user_profile.save()

            messages.success(request, 'Changes saved!', extra_tags='success')
            return redirect('profile')
        messages.error(request, "Not saved. Invalid information.", extra_tags='invalid-form')
        # Repopulate the form in case it is invalid
        return render(request, 'estate/registration/profile_edit.html', {'profile_form': form})
    else:
        if user_profile:
            # Pre-populate the form with existing values
            form = CustomUserChangeForm(instance=request.user,
                                    initial={'bio': user_profile.bio,
                                                    'profile_pic': user_profile.profile_pic_url})
        else:
            form = CustomUserChangeForm(instance=request.user)

    return render(request, 'estate/registration/profile_edit.html', {'profile_form': form})


def search_and_filter(request):
    properties = Property.objects.all()

    # distinct values for filters
    states = Location.objects.values_list('state', flat=True).distinct()
    cities = Location.objects.values_list('city', flat=True).distinct()
    categories = Property.PROPERTY_CATEGORIES
    statuses = Property.PROPERTY_STATUS

    # form submission
    if request.method == 'GET':
        state = request.GET.get('state')
        city = request.GET.get('city')
        category = request.GET.get('category')
        status = request.GET.get('status')
        min_price = request.GET.get('min-price')
        max_price = request.GET.get('max-price')

        # Apply filters
        if state and state != 'all-states':
            properties = properties.filter(location__state=state)
        if city and city != 'all-cities':
            properties = properties.filter(location__city=city)
        if category and category != 'all-categories':
            properties = properties.filter(category=category)
        if status and status != 'all-status':
            properties = properties.filter(status=status)
        if min_price and min_price != 'any-min-price':
            properties = properties.filter(price__gte=min_price)
        if max_price and max_price != 'any-max-price':
            properties = properties.filter(price__lte=max_price)

    context = {
        'properties': properties,
        'states': states,
        'cities': cities,
        'categories': categories,
        'statuses': statuses,
    }
    return render(request, 'estate/search_and_filter.html', context)
