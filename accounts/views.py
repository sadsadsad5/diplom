from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.urls import reverse


def register(request):
  if request.method == 'POST':
    # Получаем параметр next из GET-запроса
    next_url = request.GET.get('next', '')

    # Получаем значения формы
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Проверка паролей
    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.error(request, 'Это имя пользователя уже занято')
        return redirect(f"{reverse('register')}?next={next_url}")
      elif User.objects.filter(email=email).exists():
        messages.error(request, 'Этот email уже используется')
        return redirect(f"{reverse('register')}?next={next_url}")
      else:
        # Создаем пользователя
        user = User.objects.create_user(
          username=username,
          password=password,
          email=email,
          first_name=first_name,
          last_name=last_name
        )
        user.save()
        messages.success(request, 'Вы успешно зарегистрированы и можете войти')

        # Автоматический вход после регистрации (раскомментируйте при необходимости)
        # auth.login(request, user)
        # if next_url:
        #     return redirect(next_url)
        # return redirect('index')

        return redirect(f"{reverse('login')}?next={next_url}")
    else:
      messages.error(request, 'Пароли не совпадают')
      return redirect(f"{reverse('register')}?next={next_url}")
  else:
    # Для GET-запроса передаем next в контекст
    return render(request, 'accounts/register.html', {
      'next': request.GET.get('next', '')
    })


def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    next_url = request.POST.get('next', '')  # Получаем next из скрытого поля формы

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'Вы успешно вошли в систему')
      return redirect(next_url if next_url else 'dashboard')
    else:
      messages.error(request, 'Неверные учетные данные')
      return redirect(f"{reverse('login')}?next={next_url}")
  else:
    # Передаем next в шаблон
    return render(request, 'accounts/login.html', {
      'next': request.GET.get('next', '')
    })

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('index')

def dashboard(request):
  user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

  context = {
    'contacts': user_contacts
  }
  return render(request, 'accounts/dashboard.html', context)
