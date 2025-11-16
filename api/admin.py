from django.contrib import admin
from .models import (
    Entrenador, Alumno,
    TipoActividad, TipoRutina,
    Rutina,
    PlanEntrenamiento, Semana, DiaPlantilla,
    AsignacionPlan, DiaAsignado,
    EjecucionEntrenamiento, ImagenEjecucion
)

@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ['user', 'especialidad', 'telefono', 'created_at']
    search_fields = ['user__username', 'user__email', 'especialidad']
    list_filter = ['especialidad', 'created_at']

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['user', 'entrenador', 'edad', 'peso', 'altura', 'imc']
    search_fields = ['user__username', 'user__email', 'entrenador__user__username']
    list_filter = ['entrenador', 'created_at']

@admin.register(TipoActividad)
class TipoActividadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'entrenador', 'es_global']
    list_filter = ['entrenador']
    search_fields = ['nombre']

@admin.register(TipoRutina)
class TipoRutinaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'entrenador', 'es_global']
    list_filter = ['entrenador']
    search_fields = ['nombre']

@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'entrenador', 'tipo_actividad', 'tipo_rutina', 'created_at']
    list_filter = ['tipo_actividad', 'tipo_rutina', 'created_at']
    search_fields = ['nombre', 'descripcion']

class SemanaInline(admin.TabularInline):
    model = Semana
    extra = 1

@admin.register(PlanEntrenamiento)
class PlanEntrenamientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'entrenador', 'tipo_actividad', 'duracion_semanas', 'is_template']
    list_filter = ['is_template', 'tipo_actividad', 'created_at']
    search_fields = ['nombre', 'descripcion']
    inlines = [SemanaInline]

class DiaPlantillaInline(admin.TabularInline):
    model = DiaPlantilla
    extra = 7

@admin.register(Semana)
class SemanaAdmin(admin.ModelAdmin):
    list_display = ['plan', 'numero_semana', 'nombre']
    list_filter = ['plan']
    inlines = [DiaPlantillaInline]

@admin.register(DiaPlantilla)
class DiaPlantillaAdmin(admin.ModelAdmin):
    list_display = ['semana', 'dia_semana', 'rutina', 'orden', 'es_descanso']
    list_filter = ['dia_semana', 'semana__plan']

@admin.register(AsignacionPlan)
class AsignacionPlanAdmin(admin.ModelAdmin):
    list_display = ['plan', 'alumno', 'fecha_inicio', 'fecha_fin', 'estado', 'esta_activo']
    list_filter = ['estado', 'fecha_inicio']
    search_fields = ['alumno__user__username', 'plan__nombre']

@admin.register(DiaAsignado)
class DiaAsignadoAdmin(admin.ModelAdmin):
    list_display = ['asignacion_plan', 'fecha_especifica', 'dia_semana', 'completado']
    list_filter = ['completado', 'dia_semana', 'fecha_especifica']

class ImagenEjecucionInline(admin.TabularInline):
    model = ImagenEjecucion
    extra = 1

@admin.register(EjecucionEntrenamiento)
class EjecucionEntrenamientoAdmin(admin.ModelAdmin):
    list_display = [
        'dia_asignado', 'fecha_hora_ejecucion', 'distancia_km', 
        'duracion_minutos', 'ritmo', 'calificacion'
    ]
    list_filter = ['fecha_hora_ejecucion', 'calificacion']
    inlines = [ImagenEjecucionInline]

class ImagenEjecucionAdmin(admin.ModelAdmin):
    list_display = ['ejecucion', 'imagen', 'descripcion', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['descripcion', 'ejecucion__dia_asignado__asignacion_plan__alumno__user__username']