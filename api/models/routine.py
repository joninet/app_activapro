from django.db import models
from .base import TimeStampedModel
from .user_profiles import Entrenador
from .activity_types import TipoActividad, TipoRutina

class Rutina(TimeStampedModel):
    """
    Rutinas reutilizables creadas por entrenadores
    Ejemplo: "5x800m + 3x500m", "10km ritmo suave", etc.
    """
    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.CASCADE,
        related_name='rutinas',
        verbose_name='Entrenador'
    )
    tipo_actividad = models.ForeignKey(
        TipoActividad,
        on_delete=models.PROTECT,
        related_name='rutinas',
        verbose_name='Tipo de Actividad'
    )
    tipo_rutina = models.ForeignKey(
        TipoRutina,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rutinas',
        verbose_name='Tipo de Rutina'
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    detalles = models.TextField(
        blank=True,
        verbose_name='Detalles',
        help_text='Ejemplo: 5x800m + 3x500m, recuperación 2min'
    )

    class Meta:
        db_table = 'rutina'
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entrenador', 'tipo_actividad']),
            models.Index(fields=['tipo_rutina']),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.tipo_actividad.nombre}"