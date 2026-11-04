import pytest
from snippets.models import Snippet


@pytest.mark.django_db
def test_creating_a_snippet_saves_its_fields():
    snippet = Snippet.objects.create(
        title='Hello world',
        language=Snippet.Language.PYTHON,
        code='print("hello")',
    )

    saved = Snippet.objects.get(pk=snippet.pk)

    assert saved.title == 'Hello world'
    assert saved.language == 'python'
    assert saved.code == 'print("hello")'
    assert saved.created_at is not None
    assert str(saved) == 'Hello world'
