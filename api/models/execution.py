from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .base import TimeStampedModel
from .plan_assignment import DiaAsignado

class EjecucionEntrenamiento(TimeStampedModel):
    """
    Registro de la ejecución del entrenamiento por parte del alumno
    """
    dia_asignado = models.ForeignKey(
        DiaAsignado,
        on_delete=models.CASCADE,
        related_name='ejecuciones',
        verbose_name='Día Asignado'
    )
    fecha_hora_ejecucion = models.DateTimeField(
        verbose_name='Fecha y Hora de Ejecución'
    )
    comentarios = models.TextField(
        blank=True,
        verbose_name='Comentarios'
    )
    
    # Métricas de rendimiento
    ritmo = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Ritmo',
        help_text='Ej: 5:30/km'
    )
    pulsaciones_promedio = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Pulsaciones Promedio',
        validators=[MinValueValidator(30), MaxValueValidator(250)]
    )
    pulsaciones_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Pulsaciones Máximas',
        validators=[MinValueValidator(30), MaxValueValidator(250)]
    )
    distancia_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Distancia (km)'
    )
    duracion_minutos = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Duración (minutos)',
        validators=[MinValueValidator(0)]
    )
    calificacion = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Calificación',
        help_text='1-5 estrellas',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        db_table = 'ejecucion_entrenamiento'
        verbose_name = 'Ejecución de Entrenamiento'
        verbose_name_plural = 'Ejecuciones de Entrenamiento'
        ordering = ['-fecha_hora_ejecucion']
        indexes = [
            models.Index(fields=['dia_asignado', 'fecha_hora_ejecucion']),
        ]

    def __str__(self):
        return f"Ejecución - {self.dia_asignado.asignacion_plan.alumno.nombre_completo} - {self.fecha_hora_ejecucion}"

    def save(self, *args, **kwargs):
        """Al guardar, marca el día como completado"""
        super().save(*args, **kwargs)
        if not self.dia_asignado.completado:
            self.dia_asignado.completado = True
            self.dia_asignado.save()

    @property
    def ritmo_promedio_calculo(self):
        """Calcula el ritmo promedio si hay distancia y duración"""
        if self.distancia_km and self.duracion_minutos and self.distancia_km > 0:
            minutos_por_km = float(self.duracion_minutos) / float(self.distancia_km)
            minutos = int(minutos_por_km)
            segundos = int((minutos_por_km - minutos) * 60)
            return f"{minutos}:{segundos:02d}/km"
        return None


class ImagenEjecucion(models.Model):
    """
    Imágenes de la ejecución (capturas de reloj, pulsaciones, mapa de ruta, etc.)
    """
    ejecucion = models.ForeignKey(
        EjecucionEntrenamiento,
        on_delete=models.CASCADE,
        related_name='imagenes',
        verbose_name='Ejecución'
    )
    imagen = models.ImageField(
        upload_to='ejecuciones/%Y/%m/%d/',
        verbose_name='Imagen'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Carga'
    )

    class Meta:
        db_table = 'imagen_ejecucion'
        verbose_name = 'Imagen de Ejecución'
        verbose_name_plural = 'Imágenes de Ejecución'
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Imagen - {self.ejecucion}"