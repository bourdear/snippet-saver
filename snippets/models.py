from django.db import models


class Snippet(models.Model):
    class Language(models.TextChoices):
        PYTHON = 'python', 'Python'
        JAVASCRIPT = 'javascript', 'JavaScript'
        HTML = 'html', 'HTML'
        CSS = 'css', 'CSS'
        SQL = 'sql', 'SQL'
        BASH = 'bash', 'Bash'
        OTHER = 'other', 'Other'

    title = models.CharField(max_length=200)
    language = models.CharField(max_length=20, choices=Language.choices)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
