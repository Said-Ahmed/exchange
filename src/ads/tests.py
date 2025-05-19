import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from ads.models import Ad


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )


@pytest.fixture
def test_ad(user):
    return Ad.objects.create(
        title='Test Ad',
        description='Test Description',
        category='electronics',
        condition='new',
        user=user
    )


@pytest.fixture(autouse=True)
def patch_image_url(monkeypatch):
    def mock_url(self):
        return None

    monkeypatch.setattr('django.db.models.fields.files.FieldFile.url', mock_url)


@pytest.mark.django_db
def test_ad_list_view(client, test_ad):
    url = reverse('ad_list')
    response = client.get(url)

    assert response.status_code == 200
    assert 'page_obj' in response.context
    assert test_ad in response.context['page_obj']
    assert 'Test Ad' in response.content.decode()


@pytest.mark.django_db
def test_search_works(client, test_ad):
    url = reverse('ad_list') + '?search=Test'
    response = client.get(url)

    assert response.status_code == 200
    assert test_ad in response.context['page_obj']
    assert 'Test Ad' in response.content.decode()


@pytest.mark.django_db
def test_ad_create_view_post(client, user):
    client.force_login(user)
    response = client.post(reverse('ad_create'), {
        'title': 'New Post',
        'description': 'Desc',
        'category': 'electronics',
        'condition': 'new'
    })
    messages = list(get_messages(response.wsgi_request))

    assert response.status_code == 302
    assert response.url == reverse('ad_list')
    assert len(messages) == 1
    assert str(messages[0]) == 'Объявление успешно создано!'
    assert Ad.objects.filter(title='New Post').exists()


@pytest.mark.django_db
def test_ad_update_view_owner(client, user, test_ad):
    client.force_login(user)
    url = reverse('ad_update', kwargs={'pk': test_ad.pk})
    response = client.post(url, {
        'title': 'Updated',
        'description': 'Updated',
        'category': 'electronics',
        'condition': 'used'
    })
    test_ad.refresh_from_db()

    assert response.status_code == 302
    assert test_ad.title == 'Updated'