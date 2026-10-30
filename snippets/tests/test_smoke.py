import pytest


@pytest.mark.django_db
def test_admin_login_page_loads(client):
    # Placeholder so CI has something to run; also proves the app boots and
    # the test database can be created.
    response = client.get('/admin/login/')

    assert response.status_code == 200
