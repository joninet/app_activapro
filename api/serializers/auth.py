from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ..models.user_profiles import Entrenador, Alumno # Ajusta la ruta si es necesario


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    role = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8, 'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def create(self, validated_data):
        # Crear User y hashear password
        user = User.objects.create_user(**validated_data)
        return user
    
    def get_role(self, obj):
        # Intentar determinar el rol después de la creación/consulta
        if hasattr(obj, 'entrenador') and obj.entrenador:
            return 'coach'
        if hasattr(obj, 'alumno') and obj.alumno:
            return 'student'
        return None

# --- 2. Serializer de Perfil de Entrenador ---
class EntrenadorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrenador
        fields = ('especialidad', 'telefono', 'biografia', 'is_active')
        read_only_fields = ('is_active',) # is_active se gestiona internamente
        
# --- 3. Serializer de Perfil de Alumno ---
class AlumnoProfileSerializer(serializers.ModelSerializer):
    # Necesitas un ID válido de Entrenador
    entrenador_id = serializers.PrimaryKeyRelatedField(
        queryset=Entrenador.objects.filter(is_active=True), # Solo entrenadores activos
        source='entrenador',
        required=True,
        label="ID del Entrenador"
    )
    
    class Meta:
        model = Alumno
        # Se reemplaza 'entrenador' por 'entrenador_id' para el input
        fields = (
            'entrenador_id', 'fecha_nacimiento', 'telefono', 'peso', 'altura', 'notas'
        )