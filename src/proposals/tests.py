import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from proposals.models import ExchangeProposal
from proposals.forms import ExchangeProposalForm
from ads.models import Ad


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def another_user():
    return User.objects.create_user(
        username='anotheruser',
        password='testpass123'
    )


@pytest.fixture
def sender_ad(user):
    return Ad.objects.create(
        title='Sender Ad',
        description='Test',
        category='electronics',
        condition='new',
        user=user
    )


@pytest.fixture
def receiver_ad(another_user):
    return Ad.objects.create(
        title='Receiver Ad',
        description='Test',
        category='books',
        condition='used',
        user=another_user
    )


@pytest.fixture
def test_proposal(sender_ad, receiver_ad):
    return ExchangeProposal.objects.create(
        ad_sender=sender_ad,
        ad_receiver=receiver_ad,
        comment='Test proposal'
    )


@pytest.mark.django_db
def test_proposal_form_valid(sender_ad, receiver_ad):
    form_data = {
        'ad_sender': sender_ad.id,
        'ad_receiver': receiver_ad.id,
        'comment': 'Test comment'
    }
    form = ExchangeProposalForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_all_proposals_view(client, test_proposal):
    url = reverse('proposals:all_proposals')
    response = client.get(url)

    assert response.status_code == 200
    assert test_proposal in response.context['proposals']


@pytest.mark.django_db
def test_create_proposal_authenticated(client, user, sender_ad, receiver_ad):
    client.force_login(user)
    response = client.post(reverse('proposals:create_proposal'), {
        'ad_sender': sender_ad.id,
        'ad_receiver': receiver_ad.id,
        'comment': 'New proposal'
    })
    messages = list(get_messages(response.wsgi_request))

    assert response.status_code == 302
    assert response.url == reverse('proposals:all_proposals')
    assert len(messages) == 1
    assert str(messages[0]) == "Предложение обмена успешно создано!"
    assert ExchangeProposal.objects.filter(comment='New proposal').exists()


@pytest.mark.django_db
def test_update_proposal_status(client, another_user, test_proposal):
    client.force_login(another_user)
    url = reverse('proposals:update_status', kwargs={
        'pk': test_proposal.pk,
        'new_status': 'accepted'
    })
    response = client.post(url)
    test_proposal.refresh_from_db()

    assert response.status_code == 302
    assert test_proposal.status == 'accepted'


@pytest.mark.django_db
def test_cannot_update_own_proposal(client, user, test_proposal):
    client.force_login(user)
    url = reverse('proposals:update_status', kwargs={
        'pk': test_proposal.pk,
        'new_status': 'accepted'
    })
    response = client.post(url)

    assert response.status_code == 403
    assert test_proposal.status == 'pending'


@pytest.mark.django_db
def test_proposal_filters(client, test_proposal):
    url = reverse('proposals:all_proposals') + f'?sender={test_proposal.ad_sender.user.username}'
    response = client.get(url)
    assert test_proposal in response.context['proposals']

    url = reverse('proposals:all_proposals') + '?status=pending'
    response = client.get(url)
    assert test_proposal in response.context['proposals']

