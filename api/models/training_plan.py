from django.db import models
from django.core.validators import MinValueValidator
from .base import TimeStampedModel
from .user_profiles import Entrenador
from .activity_types import TipoActividad
from .routine import Rutina

class PlanEntrenamiento(TimeStampedModel):
    """
    Plan de Entrenamiento (plantilla general)
    Puede ser una plantilla reutilizable o un plan específico
    """
    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.CASCADE,
        related_name='planes_entrenamiento',
        verbose_name='Entrenador'
    )
    tipo_actividad = models.ForeignKey(
        TipoActividad,
        on_delete=models.PROTECT,
        related_name='planes_entrenamiento',
        verbose_name='Tipo de Actividad'
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    duracion_semanas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Duración (semanas)'
    )
    is_template = models.BooleanField(
        default=False,
        verbose_name='Es Plantilla',
        help_text='Marca si este plan es una plantilla reutilizable'
    )

    class Meta:
        db_table = 'plan_entrenamiento'
        verbose_name = 'Plan de Entrenamiento'
        verbose_name_plural = 'Planes de Entrenamiento'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entrenador', 'is_template']),
            models.Index(fields=['tipo_actividad']),
        ]

    def __str__(self):
        tipo = "Plantilla" if self.is_template else "Plan"
        return f"{tipo}: {self.nombre} ({self.duracion_semanas} semanas)"


class Semana(models.Model):
    """
    Semanas del plan de entrenamiento
    """
    plan = models.ForeignKey(
        PlanEntrenamiento,
        on_delete=models.CASCADE,
        related_name='semanas',
        verbose_name='Plan'
    )
    numero_semana = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Número de Semana'
    )
    nombre = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Nombre',
        help_text='Ej: Semana de adaptación, Semana de carga'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )

    class Meta:
        db_table = 'semana'
        verbose_name = 'Semana'
        verbose_name_plural = 'Semanas'
        ordering = ['plan', 'numero_semana']
        unique_together = [['plan', 'numero_semana']]
        indexes = [
            models.Index(fields=['plan', 'numero_semana']),
        ]

    def __str__(self):
        return f"{self.plan.nombre} - Semana {self.numero_semana}"


class DiaPlantilla(models.Model):
    """
    Días plantilla (días de la semana con rutinas asignadas)
    """
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    semana = models.ForeignKey(
        Semana,
        on_delete=models.CASCADE,
        related_name='dias_plantilla',
        verbose_name='Semana'
    )
    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dias_plantilla',
        verbose_name='Rutina',
        help_text='Puede ser NULL para días de descanso'
    )
    dia_semana = models.CharField(
        max_length=10,
        choices=DIAS_SEMANA,
        verbose_name='Día de la Semana'
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden dentro de la semana (0-6)'
    )
    notas = models.TextField(
        blank=True,
        verbose_name='Notas'
    )

    class Meta:
        db_table = 'dia_plantilla'
        verbose_name = 'Día Plantilla'
        verbose_name_plural = 'Días Plantilla'
        ordering = ['semana', 'orden']
        indexes = [
            models.Index(fields=['semana', 'orden']),
            models.Index(fields=['dia_semana']),
        ]

    def __str__(self):
        rutina_nombre = self.rutina.nombre if self.rutina else 'Descanso'
        return f"{self.semana} - {self.get_dia_semana_display()}: {rutina_nombre}"

    @property
    def es_descanso(self):
        return self.rutina is None