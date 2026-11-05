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


@pytest.mark.django_db
def test_edit_form_updates_snippet_and_redirects_to_detail(client):
    snippet = Snippet.objects.create(title='Old title', language='python', code='print("old")')
    created_at = snippet.created_at

    response = client.post(reverse('snippets:update', args=[snippet.pk]), {
        'title': 'New title',
        'language': 'sql',
        'code': 'SELECT 1;',
    })

    assert response.status_code == 302
    assert response.url == snippet.get_absolute_url()

    snippet.refresh_from_db()
    assert snippet.title == 'New title'
    assert snippet.language == 'sql'
    assert snippet.code == 'SELECT 1;'
    assert snippet.created_at == created_at
    assert Snippet.objects.count() == 1


@pytest.mark.django_db
def test_edit_form_shows_current_values(client):
    snippet = Snippet.objects.create(title='Hello world', language='python', code='print("hello")')

    response = client.get(reverse('snippets:update', args=[snippet.pk]))

    assert response.status_code == 200
    assert 'Edit Snippet' in response.content.decode()
    assert response.context['form'].initial['title'] == 'Hello world'


@pytest.mark.django_db
def test_edit_form_allows_keeping_the_same_title(client):
    snippet = Snippet.objects.create(title='Hello world', language='python', code='print("hello")')

    response = client.post(reverse('snippets:update', args=[snippet.pk]), {
        'title': 'Hello world',
        'language': 'python',
        'code': 'print("changed")',
    })

    assert response.status_code == 302
    snippet.refresh_from_db()
    assert snippet.code == 'print("changed")'


@pytest.mark.django_db
def test_edit_form_rejects_title_of_another_snippet(client):
    Snippet.objects.create(title='Taken', language='python', code='print("taken")')
    snippet = Snippet.objects.create(title='Mine', language='python', code='print("mine")')

    response = client.post(reverse('snippets:update', args=[snippet.pk]), {
        'title': 'Taken',
        'language': 'python',
        'code': 'print("mine")',
    })

    assert response.status_code == 200
    assert 'title' in response.context['form'].errors
    snippet.refresh_from_db()
    assert snippet.title == 'Mine'


@pytest.mark.django_db
def test_delete_page_asks_first_and_does_not_delete(client):
    snippet = Snippet.objects.create(title='Hello world', language='python', code='print("hello")')

    response = client.get(reverse('snippets:delete', args=[snippet.pk]))

    assert response.status_code == 200
    assert 'Hello world' in response.content.decode()
    assert Snippet.objects.filter(pk=snippet.pk).exists()


@pytest.mark.django_db
def test_delete_removes_only_that_snippet_and_redirects_to_list(client):
    snippet = Snippet.objects.create(title='Delete me', language='python', code='print("bye")')
    other = Snippet.objects.create(title='Keep me', language='python', code='print("stay")')

    response = client.post(reverse('snippets:delete', args=[snippet.pk]))

    assert response.status_code == 302
    assert response.url == reverse('snippets:list')
    assert not Snippet.objects.filter(pk=snippet.pk).exists()
    assert Snippet.objects.filter(pk=other.pk).exists()


@pytest.mark.django_db
def test_delete_requires_csrf_token():
    client = Client(enforce_csrf_checks=True)
    snippet = Snippet.objects.create(title='Hello world', language='python', code='print("hello")')

    response = client.post(reverse('snippets:delete', args=[snippet.pk]))

    assert response.status_code == 403
    assert Snippet.objects.filter(pk=snippet.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize('url_name', ['snippets:update', 'snippets:delete'])
def test_edit_and_delete_return_404_for_missing_snippet(client, url_name):
    response = client.get(reverse(url_name, args=[999]))

    assert response.status_code == 404
