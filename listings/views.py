from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncMonth
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from .models import Listing
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from realtors.models import Realtor
from django.contrib.auth.decorators import login_required
from .forms import ListingForm
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Listing



def index(request):
  # Получаем параметр сортировки из URL
  sort_param = request.GET.get('sort', '-list_date')  # По умолчанию: новые сначала

  # Начинаем с базового QuerySet
  listings = Listing.objects.filter(is_published=True)

  # Применяем сортировку
  if sort_param == 'price':
    listings = listings.order_by('price')  # Дешевые сначала
  elif sort_param == '-price':
    listings = listings.order_by('-price')  # Дорогие сначала
  else:
    listings = listings.order_by('-list_date')  # По умолчанию: новые сначала

  # Пагинация
  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings,
    'sort_param': sort_param  # Передаем в шаблон для отладки
  }

  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': listing
  }

  return render(request, 'listings/listing.html', context)


def search(request):
  # Получаем параметр сортировки (по умолчанию - по новизне)
  sort_param = request.GET.get('sort', '-list_date')

  # Начинаем с базового QuerySet
  queryset_list = Listing.objects.filter(is_published=True)

  # Применяем сортировку
  if sort_param == 'price':
    queryset_list = queryset_list.order_by('price')
  elif sort_param == '-price':
    queryset_list = queryset_list.order_by('-price')
  else:
    queryset_list = queryset_list.order_by('-list_date')

  # Фильтрация по параметрам поиска
  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # State
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      queryset_list = queryset_list.filter(state__iexact=state)

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET,
    'sort_param': sort_param  # Добавляем для отображения текущей сортировки
  }

  return render(request, 'listings/search.html', context)

# listings/views.py
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('dashboard')
    else:
        form = ListingForm()
    return render(request, 'listings/create_listing.html', {'form': form})

@login_required
def user_listings(request):
    listings = Listing.objects.filter(user=request.user).order_by('-list_date')
    context = {
      'listings': listings
    }
    return render(request, 'listings/user_listings.html', context)

from django.shortcuts import get_object_or_404, render, redirect
from .models import Listing
from .forms import ListingForm

def update_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('user_listings')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'listings/update_listing.html', {'form': form})

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, user=request.user)
    if request.method == 'POST':
        listing.delete()
        return redirect('dashboard')  # Теперь этот name существует
    return redirect('user_listings')


def statistics_view(request):
    # Основные метрики
    total_listings = Listing.objects.filter(is_published=True).count()

    # Средняя цена (исключаем нулевые цены)
    avg_price = Listing.objects.filter(
        is_published=True,
        price__gt=0
    ).aggregate(avg_price=Avg('price'))['avg_price'] or 0

    # Активные клиенты (за последние 30 дней)
    active_clients = Listing.objects.filter(
        is_published=True,
        list_date__gte=timezone.now() - timedelta(days=30)
    ).values('user').distinct().count()

    # Сделки за месяц
    monthly_deals = Listing.objects.filter(
        is_published=True,
        list_date__month=timezone.now().month,
        list_date__year=timezone.now().year
    ).count()

    # Статистика по регионам
    regions = Listing.objects.filter(is_published=True).values('state').annotate(
        count=Count('id'),
        avg_price=Avg('price')
    ).order_by('-count')[:5]

    # Данные для графика динамики цен (последние 12 месяцев)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)

    monthly_stats = Listing.objects.filter(
        is_published=True,
        price__gt=0,
        list_date__range=[start_date, end_date]
    ).annotate(
        month=TruncMonth('list_date')
    ).values('month').annotate(
        avg_price=Avg('price'),
        count=Count('id')
    ).order_by('month')

    # Подготовка данных для графика цен
    months = []
    avg_prices = []

    current_month = timezone.now().replace(day=1)
    for i in range(12):
        month = current_month - timedelta(days=30 * i)
        month_str = month.strftime('%b %Y')

        stat = next((s for s in monthly_stats if
                    s['month'].month == month.month and
                    s['month'].year == month.year), None)

        months.insert(0, month_str)
        avg_prices.insert(0, float(stat['avg_price']) if stat else 0)

    # Статистика по количеству спален
    bedroom_stats = Listing.objects.filter(
        is_published=True
    ).values('bedrooms').annotate(
        count=Count('id')
    ).order_by('bedrooms')

    # Подготовка данных для диаграммы спален
    bedroom_labels = []
    bedroom_data = []
    bedroom_colors = ['#0d6efd', '#198754', '#fd7e14', '#6f42c1', '#20c997', '#dc3545']

    for stat in bedroom_stats:
        label = "Студия" if stat['bedrooms'] == 0 else f"Кол-во комнат: {stat['bedrooms']}"
        bedroom_labels.append(label)
        bedroom_data.append(stat['count'])

    # Собираем все данные в один контекст
    context = {
        'total_listings': total_listings,
        'avg_price': avg_price,
        'active_clients': active_clients,
        'monthly_deals': monthly_deals,
        'regions': regions,
        'months': json.dumps(months, cls=DjangoJSONEncoder),
        'avg_prices': json.dumps(avg_prices),
        'bedroom_labels': json.dumps(bedroom_labels, cls=DjangoJSONEncoder),
        'bedroom_data': json.dumps(bedroom_data),
        'bedroom_colors': json.dumps(bedroom_colors[:len(bedroom_labels)]),

    }

    return render(request, 'statistics/statistics.html', context)