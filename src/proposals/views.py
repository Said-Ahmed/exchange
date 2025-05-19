from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import ExchangeProposal
from .forms import ExchangeProposalForm


def all_proposals(request):
    proposals = ExchangeProposal.objects.all().order_by('-created_at')

    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    status = request.GET.get('status')

    if sender:
        proposals = proposals.filter(ad_sender__user__username__icontains=sender)
    if receiver:
        proposals = proposals.filter(ad_receiver__user__username__icontains=receiver)
    if status:
        proposals = proposals.filter(status=status)

    paginator = Paginator(proposals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'proposals/all_proposals.html', {
        'proposals': page_obj,
        'status_choices': ExchangeProposal.STATUS_CHOICES,
        'current_status': status or '',
        'current_sender': sender or '',
        'current_receiver': receiver or ''
    })

@login_required
def create_exchange_proposal(request):
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Предложение обмена успешно создано!")
            return redirect('proposals:all_proposals')
    else:
        form = ExchangeProposalForm()

    return render(request, 'proposals/create_proposal.html', {'form': form})


@login_required
def update_proposal_status(request, pk, new_status):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)

    if request.user != proposal.ad_receiver.user:
        return render(request, 'proposals/error.html', {
            'error': 'Вы не менять статус чужих предложений'
        }, status=403)

    if proposal.status in ('accepted', 'rejected'):
        return render(request, 'proposals/error.html', {
            'error': 'Действие недоступно'
        }, status=403)

    proposal.status = new_status
    proposal.save()

    return redirect('proposals:all_proposals')
