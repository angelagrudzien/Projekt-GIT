from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.urls import reverse_lazy


# Widok rejestracji
class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')  # Zmień na swoją stronę główną

    def form_valid(self, form):
        user = form.save()  # Zapisz użytkownika
        login(self.request, user)  # Zaloguj użytkownika po rejestracji
        messages.success(self.request, "Rejestracja zakończona sukcesem!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Błąd podczas rejestracji. Popraw dane.")
        return super().form_invalid(form)


# Widok logowania
class LoginView(AuthLoginView):
    template_name = 'users/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Błędne dane logowania.")
        return super().form_invalid(form)
