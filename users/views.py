from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
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
class LoginView(View):
    template_name = "users/login.html"

    def get(self, request):
        # Renderowanie formularza logowania
        return render(request, self.template_name)

    def post(self, request):
        # Pobranie danych logowania z formularza
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Sprawdzanie, czy użytkownik istnieje
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Jeśli dane są poprawne, logujemy użytkownika
            login(request, user)
            messages.success(request, "Zalogowano pomyślnie.")
            return HttpResponseRedirect(reverse_lazy('home'))  # Zmień na odpowiedni URL strony głównej
        else:
            # Jeśli dane logowania są niepoprawne
            messages.error(request, "Błędne dane logowania.")
            return render(request, self.template_name)  # Ponowne wyświetlenie formularza logowania
