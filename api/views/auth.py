from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers.auth import (
    UserSerializer,
    EntrenadorProfileSerializer,
    AlumnoProfileSerializer
)
from ..services.user_management import RegistrationService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Registro de usuarios (coach o student).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password', 'role'],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, example="juan23"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, example="juan@gmail.com"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, example="12345678"),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING, example="Juan"),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING, example="Pérez"),
                "role": openapi.Schema(type=openapi.TYPE_STRING, enum=["coach", "student"], example="coach"),

                # Campos de Perfil Entrenador
                "especialidad": openapi.Schema(type=openapi.TYPE_STRING, example="Running"),
                "telefono": openapi.Schema(type=openapi.TYPE_STRING, example="+54 11 5555 0000"),
                "biografia": openapi.Schema(type=openapi.TYPE_STRING, example="Entrenador certificado AAT"),

                # Campos de Perfil Alumno
                "entrenador_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                "fecha_nacimiento": openapi.Schema(type=openapi.TYPE_STRING, example="1995-06-12"),
                "peso": openapi.Schema(type=openapi.TYPE_NUMBER, example=70),
                "altura": openapi.Schema(type=openapi.TYPE_NUMBER, example=1.75),
                "notas": openapi.Schema(type=openapi.TYPE_STRING, example="Lesión rodilla derecha"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Usuario registrado correctamente.",
                examples={
                    "coach": {
                        "user_id": 1,
                        "username": "juan23",
                        "role": "coach",
                        "message": "Registro de Entrenador exitoso. Por favor, complete el pago para activar su cuenta.",
                        "next_step": "/api/v1/payment/setup"
                    },
                    "student": {
                        "user_id": 10,
                        "username": "maria22",
                        "role": "student",
                        "message": "Registro de Alumno exitoso. ¡Bienvenido!"
                    }
                }
            ),
            400: "Datos inválidos (por ejemplo, role incorrecto).",
            500: "Error interno en el servicio de registro."
        }
    )
    def post(self, request, *args, **kwargs):
        role = request.data.get('role', None)
        if role not in ('coach', 'student'):
            return Response(
                {"role": "Debe especificar un rol válido: 'coach' o 'student'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_validated_data = user_serializer.validated_data

        if role == 'coach':
            profile_serializer = EntrenadorProfileSerializer(data=request.data)
        else:
            profile_serializer = AlumnoProfileSerializer(data=request.data)

        profile_serializer.is_valid(raise_exception=True)
        profile_validated_data = profile_serializer.validated_data

        try:
            user = RegistrationService.register_user_and_profile(
                user_validated_data,
                profile_validated_data,
                role
            )

            response_data = {
                "user_id": user.id,
                "username": user.username,
                "role": role
            }

            if role == 'coach':
                response_data["message"] = (
                    "Registro de Entrenador exitoso. Por favor, complete el pago para activar su cuenta."
                )
                response_data["next_step"] = "/api/v1/payment/setup"
            else:
                response_data["message"] = "Registro de Alumno exitoso. ¡Bienvenido!"

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": "Error en el proceso de registro.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CoachActivationWebhookView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Webhook para activar cuenta de entrenador luego del pago.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_id'],
            properties={
                "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            }
        ),
        responses={
            200: openapi.Response(
                description="Entrenador activado correctamente.",
                examples={"application/json": {"message": "Entrenador activado."}}
            ),
            404: "No se encontró el entrenador.",
            400: "Falta user_id.",
        }
    )
    def post(self, request):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"detail": "Falta el user_id."}, status=status.HTTP_400_BAD_REQUEST)

        success, message = RegistrationService.activate_coach(user_id)

        if success:
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)
