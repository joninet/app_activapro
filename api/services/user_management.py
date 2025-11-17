from django.db import transaction
from django.contrib.auth.models import User
from ..models.user_profiles import Entrenador, Alumno

class RegistrationService:
    @staticmethod
    def register_user_and_profile(user_data, profile_data, role):
        """
        Crea el usuario base y el perfil asociado en una transacción atómica.
        """
        try:
            with transaction.atomic():
                # 1. Crear el usuario base (ya validado por el serializer)
                user = User.objects.create_user(**user_data)

                # 2. Crear el perfil específico
                if role == 'coach':
                    # NOTA: is_active por defecto es False en el modelo
                    Entrenador.objects.create(user=user, **profile_data)
                
                elif role == 'student':
                    # El entrenador ya está en profile_data como objeto por el serializer
                    Alumno.objects.create(user=user, **profile_data)
                
                return user
        
        except Exception as e:
            # Re-lanza la excepción para que la vista la maneje
            raise e 

    @staticmethod
    def activate_coach(user_id):
        """
        Activa la cuenta del Entrenador después de la confirmación de pago.
        """
        try:
            entrenador = Entrenador.objects.get(user_id=user_id)
            if not entrenador.is_active:
                entrenador.is_active = True
                entrenador.save(update_fields=['is_active'])
                return True, "Entrenador activado exitosamente."
            return True, "El Entrenador ya estaba activo."
        except Entrenador.DoesNotExist:
            return False, "Error: Entrenador no encontrado."