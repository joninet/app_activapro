from django.db import models
from django.core.exceptions import ValidationError
from .base import TimeStampedModel
from .user_profiles import Alumno
from .training_plan import PlanEntrenamiento, DiaPlantilla

class AsignacionPlan(TimeStampedModel):
    """
    Asignación de un plan de entrenamiento a un alumno específico
    """
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    plan = models.ForeignKey(
        PlanEntrenamiento,
        on_delete=models.PROTECT,
        related_name='asignaciones',
        verbose_name='Plan'
    )
    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.CASCADE,
        related_name='planes_asignados',
        verbose_name='Alumno'
    )
    fecha_inicio = models.DateField(
        verbose_name='Fecha de Inicio'
    )
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Fin'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activo',
        verbose_name='Estado'
    )

    class Meta:
        db_table = 'asignacion_plan'
        verbose_name = 'Asignación de Plan'
        verbose_name_plural = 'Asignaciones de Planes'
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['alumno', 'estado']),
            models.Index(fields=['fecha_inicio', 'fecha_fin']),
        ]

    def __str__(self):
        return f"{self.plan.nombre} → {self.alumno.nombre_completo} ({self.estado})"

    def clean(self):
        """Validaciones personalizadas"""
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')

    @property
    def dias_totales(self):
        """Calcula el total de días del plan"""
        if self.fecha_fin:
            return (self.fecha_fin - self.fecha_inicio).days + 1
        return None

    @property
    def esta_activo(self):
        return self.estado == 'activo'


class DiaAsignado(TimeStampedModel):
    """
    Días específicos asignados con fechas concretas
    Se generan automáticamente cuando se asigna un plan a un alumno
    """
    asignacion_plan = models.ForeignKey(
        AsignacionPlan,
        on_delete=models.CASCADE,
        related_name='dias_asignados',
        verbose_name='Asignación de Plan'
    )
    dia_plantilla = models.ForeignKey(
        DiaPlantilla,
        on_delete=models.PROTECT,
        related_name='dias_asignados',
        verbose_name='Día Plantilla'
    )
    fecha_especifica = models.DateField(
        verbose_name='Fecha Específica'
    )
    dia_semana = models.CharField(
        max_length=10,
        verbose_name='Día de la Semana'
    )
    completado = models.BooleanField(
        default=False,
        verbose_name='Completado'
    )

    class Meta:
        db_table = 'dia_asignado'
        verbose_name = 'Día Asignado'
        verbose_name_plural = 'Días Asignados'
        ordering = ['fecha_especifica']
        unique_together = [['asignacion_plan', 'fecha_especifica']]
        indexes = [
            models.Index(fields=['asignacion_plan', 'fecha_especifica']),
            models.Index(fields=['completado']),
        ]

    def __str__(self):
        return f"{self.asignacion_plan.alumno.nombre_completo} - {self.fecha_especifica}"

    @property
    def rutina(self):
        """Retorna la rutina asociada al día plantilla"""
        return self.dia_plantilla.rutina