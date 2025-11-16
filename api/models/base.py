from django.db import models

class TimeStampedModel(models.Model):
    """
    Modelo abstracto base con campos de auditoría
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModel(models.Model):
    """
    Modelo abstracto para eliminación lógica
    """
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_active = False
        self.save()

    def restore(self):
        self.is_active = True
        self.save()