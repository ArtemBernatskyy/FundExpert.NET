from django.db import models


class ManagementCompany(models.Model):
    name = models.CharField(max_length=320)
    slug = models.SlugField(unique=True, max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Management companies"
