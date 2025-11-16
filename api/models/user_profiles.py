from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .base import TimeStampedModel

class Entrenador(TimeStampedModel):
    """
    Perfil de Entrenador - Extiende el modelo User de Django
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='entrenador',
        verbose_name='Usuario'
    )
    especialidad = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Especialidad'
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Teléfono'
    )
    biografia = models.TextField(
        blank=True,
        verbose_name='Biografía'
    )

    class Meta:
        db_table = 'entrenador'
        verbose_name = 'Entrenador'
        verbose_name_plural = 'Entrenadores'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.especialidad}"

    @property
    def nombre_completo(self):
        return self.user.get_full_name()


class Alumno(TimeStampedModel):
    """
    Perfil de Alumno - Extiende el modelo User de Django
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='alumno',
        verbose_name='Usuario'
    )
    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.PROTECT,
        related_name='alumnos',
        verbose_name='Entrenador'
    )
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Nacimiento'
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Teléfono'
    )
    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Peso (kg)',
        help_text='Peso en kilogramos'
    )
    altura = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Altura (m)',
        help_text='Altura en metros'
    )
    notas = models.TextField(
        blank=True,
        verbose_name='Notas'
    )

    class Meta:
        db_table = 'alumno'
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        indexes = [
            models.Index(fields=['entrenador', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.entrenador.user.get_full_name()}"

    @property
    def nombre_completo(self):
        return self.user.get_full_name()

    @property
    def edad(self):
        """Calcula la edad del alumno"""
        if self.fecha_nacimiento:
            from datetime import date
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None

    @property
    def imc(self):
        """Calcula el índice de masa corporal"""
        if self.peso and self.altura and self.altura > 0:
            return round(float(self.peso) / (float(self.altura) ** 2), 2)
        return None