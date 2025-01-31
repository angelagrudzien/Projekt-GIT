from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CustomUser


# Widok rejestracji użytkownika
class RegisterView(View):
    def get(self, request):
        return render(request, "users/register.html")

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Hasła muszą się zgadzać.")
            return render(request, "users/register.html")

        if CustomUser.objects.filter(password=password).exists():
            messages.error(request, "Podane hasło już istnieje.")
            return render(request, "users/register.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Użytkownik o takiej nazwie już istnieje.")
            return render(request, "users/register.html")

        user = CustomUser.objects.create_user(username=username,
                                              email=email,
                                              first_name=first_name,
                                              last_name=last_name,
                                              phone_number=phone_number,
                                              address=address,
                                              password=password
                                              )
        login(request, user)
        messages.success(request, "Rejestracja zakończona sukcesem.")
        return HttpResponseRedirect(reverse_lazy('home'))  # Zmień na odpowiedni URL


# Widok logowania użytkownika
class LoginView(AuthLoginView):
    template_name = "users/login.html"

    def form_invalid(self, form):
        messages.error(self.request, "Błędne dane logowania.")
        return super().form_invalid(form)
