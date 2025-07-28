from django.db import models
from parler.models import TranslatableModel , TranslatedFields

# Create your models here.

class ArchiveYear(TranslatableModel):
    translations = TranslatedFields(
    year = models.IntegerField(max_length=255)

    )

    def __str__(self):
        return str(self.year)

class ArchiveMonth(TranslatableModel):
    translations = TranslatedFields(
    month = models.CharField(max_length=255)

    )
    year = models.ForeignKey(ArchiveYear , on_delete=models.CASCADE , related_name='months' , null=True)

    def __str__(self):
        return self.month