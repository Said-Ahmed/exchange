from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AdForm, AdSearchForm

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Ad


def ad_list(request):
    ads = Ad.objects.all().order_by('-created_at')
    search_form = AdSearchForm(request.GET or None)

    if search_form.is_valid():
        search_data = search_form.cleaned_data

        search_query = search_data.get('search')
        if search_query:
            ads = ads.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        category = search_data.get('category')
        if category:
            ads = ads.filter(category=category)

        condition = search_data.get('condition')
        if condition:
            ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {
        'page_obj': page_obj,
        'search_form': search_form
    })

@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, files=request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('ad_list')
    else:
        form = AdForm()

    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def ad_update(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.user != request.user:
        messages.error(request, 'Вы не можете редактировать это объявление!')
        return redirect('ad_list')

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)

    if ad.user != request.user:
        return render(request, 'ads/error.html', {
            'error': 'Вы не являетесь автором этого объявления'
        }, status=403)

    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')

    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})