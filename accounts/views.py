from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy # this is used to reverse the URL for the login view after successful login


# Create your views here.
def register(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.is_active = False
            user.save()

            role = form.cleaned_data.get('role')

            group = Group.objects.get(name=role)

            user.groups.add(group)

            messages.success(
                request,
                'Account created successfully. Wait for admin approval.'
            )

            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):

    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.groups.filter(name='Admin').exists():
            return reverse_lazy('stock_list')

        if user.groups.filter(name='Sales Attendant').exists():
            return reverse_lazy('home')

        if user.groups.filter(name='Store Manager').exists():
            return reverse_lazy('scheme_customer_list')
        
        if user.groups.filter(name='Manager').exists():
            return reverse_lazy('stock_list')
        
        if user.groups.filter(name='Sales Manager').exists():
            return reverse_lazy('stock_list')

        return reverse_lazy('login')