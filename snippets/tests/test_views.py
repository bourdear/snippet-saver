import pytest
from django.test import Client
from django.urls import reverse
from snippets.models import Snippet


@pytest.mark.django_db
def test_list_page_shows_snippet_titles(client):
    Snippet.objects.create(title='Hello world', language='python', code='print("hello")')

    response = client.get(reverse('snippets:list'))

    assert response.status_code == 200
    assert 'Hello world' in response.content.decode()


@pytest.mark.django_db
def test_create_form_saves_snippet_and_redirects_to_detail(client):
    response = client.post(reverse('snippets:create'), {
        'title': 'Select one',
        'language': 'sql',
        'code': 'SELECT 1;',
    })

    snippet = Snippet.objects.get()
    assert snippet.title == 'Select one'
    assert response.status_code == 302
    assert response.url == snippet.get_absolute_url()

    detail = client.get(response.url)
    assert detail.status_code == 200
    assert 'SELECT 1;' in detail.content.decode()


@pytest.mark.django_db
def test_create_form_rejects_duplicate_title(client):
    Snippet.objects.create(title='Hello world', language='python', code='print("hello")')

    response = client.post(reverse('snippets:create'), {
        'title': 'Hello world',
        'language': 'sql',
        'code': 'SELECT 1;',
    })

    assert response.status_code == 200
    assert 'title' in response.context['form'].errors
    assert Snippet.objects.count() == 1


@pytest.mark.django_db
def test_create_form_works_with_csrf_checks_enabled():
    client = Client(enforce_csrf_checks=True)
    url = reverse('snippets:create')

    # Without a token, the request is rejected.
    response = client.post(url, {'title': 'A', 'language': 'sql', 'code': 'SELECT 1;'})
    assert response.status_code == 403

    # With the token from the rendered page, it saves.
    page = client.get(url)
    token = page.context['csrf_token']
    assert f'value="{token}"' in page.content.decode()

    response = client.post(url, {
        'title': 'A',
        'language': 'sql',
        'code': 'SELECT 1;',
        'csrfmiddlewaretoken': token,
    })
    assert response.status_code == 302


@pytest.mark.django_db
def test_missing_snippet_returns_404(client):
    response = client.get(reverse('snippets:detail', args=[999]))

    assert response.status_code == 404
