# account/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import RegistrationForm
import random

User = get_user_model()


class RegisterView(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'html/account/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Сделаем пользователя неактивным до подтверждения
            user.save()
            confirmation_code = random.randint(1000, 9999)
            request.session['confirmation_code'] = confirmation_code
            request.session['user_id'] = user.id
            print(f"Confirmation code sent: {confirmation_code}")  # Здесь будет ваша логика отправки кода
            return redirect('confirm')  # Перенаправление на страницу подтверждения кода
        return render(request, 'html/account/register.html', {'form': form})


class ConfirmView(View):
    def get(self, request):
        return render(request, 'html/account/confirm.html')

    def post(self, request):
        code = request.POST.get('code')
        if code == str(request.session.get('confirmation_code')):
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            del request.session['confirmation_code']
            del request.session['user_id']
            messages.success(request, 'Ваш аккаунт успешно подтвержден.')
            return redirect('login')  # Перенаправление на страницу входа после успешного подтверждения
        messages.error(request, 'Неверный код подтверждения.')
        return redirect('confirm')
