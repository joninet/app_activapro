from django.db import models
from .base import TimeStampedModel
from .user_profiles import Entrenador

class TipoActividad(models.Model):
    """
    Tipos de Actividad (Running, Ciclismo, Natación, etc.)
    NULL en entrenador = global, con valor = personalizado por entrenador
    """
    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tipos_actividad_personalizados',
        verbose_name='Entrenador',
        help_text='NULL = tipo global, con valor = personalizado'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )

    class Meta:
        db_table = 'tipo_actividad'
        verbose_name = 'Tipo de Actividad'
        verbose_name_plural = 'Tipos de Actividad'
        unique_together = [['nombre', 'entrenador']]
        indexes = [
            models.Index(fields=['entrenador', 'nombre']),
        ]

    def __str__(self):
        if self.entrenador:
            return f"{self.nombre} (personalizado por {self.entrenador.nombre_completo})"
        return f"{self.nombre} (global)"

    @property
    def es_global(self):
        return self.entrenador is None


class TipoRutina(models.Model):
    """
    Tipos de Rutina (Series, Fuerza, Resistencia, Intervalos, etc.)
    NULL en entrenador = global, con valor = personalizado por entrenador
    """
    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tipos_rutina_personalizados',
        verbose_name='Entrenador',
        help_text='NULL = tipo global, con valor = personalizado'
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )

    class Meta:
        db_table = 'tipo_rutina'
        verbose_name = 'Tipo de Rutina'
        verbose_name_plural = 'Tipos de Rutina'
        unique_together = [['nombre', 'entrenador']]
        indexes = [
            models.Index(fields=['entrenador', 'nombre']),
        ]

    def __str__(self):
        if self.entrenador:
            return f"{self.nombre} (personalizado por {self.entrenador.nombre_completo})"
        return f"{self.nombre} (global)"

    @property
    def es_global(self):
        return self.entrenador is None