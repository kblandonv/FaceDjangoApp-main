from rest_framework import serializers
from .models import Solicitud_amistad, Mensaje
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q


class SolicitudSerializer(serializers.Serializer):
    """
    Serializer for creating a Solicitud_amistad object.

    This serializer validates and creates a Solicitud_amistad object based on the provided data.
    It checks if the user_sender and user_receptor are valid users and if a request or friendship already exists between them.
    """

    user_sender = serializers.CharField()
    user_receptor = serializers.CharField()

    def create(self, validated_data):
        validacion = self.validar_solicitud(validated_data)

        solicitud = Solicitud_amistad()
        solicitud.user_sender = validacion[0]
        solicitud.user_receptor = validacion[1]
        solicitud.save()
        return solicitud
    
    def validar_solicitud(self, data):
        user_sender = data.get('user_sender')
        user_receptor = data.get('user_receptor')

        try:
            user_sender = User.objects.get(id=user_sender)
            user_receptor = User.objects.get(id=user_receptor)
        except:
            raise serializers.ValidationError({'error': 'Usuario/s invalido'})

        solicitudes_usaurios = Solicitud_amistad.objects.filter(Q(user_sender=user_sender.id, user_receptor=user_receptor.id) 
                                                                | Q(user_sender=user_receptor.id, user_receptor=user_sender.id))   
        if list(solicitudes_usaurios) != []:
            raise serializers.ValidationError({'error': 'Ya existe una solicitud o amistad entre los usuarios'})
        
        if user_sender == user_receptor:
            raise serializers.ValidationError({'error': 'Invalido, no se puede enviar la solicitud a si mismo'})
        
        return (user_sender, user_receptor)


class SolicitudInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solicitud_amistad
        fields = '__all__'
        

class MensajesSerializer(serializers.Serializer):
    """
    Serializer for the Mensajes model.
    """

    amistad = serializers.CharField()
    enviado_por = serializers.CharField()
    mensaje = serializers.CharField()

    def create(self, validated_data):
        """
        Create and save a new Mensaje instance.

        Args:
            validated_data (dict): Validated data for creating the Mensaje instance.

        Returns:
            Mensaje: The created Mensaje instance.
        """
        mensaje_nuevo = Mensaje()
        user = User.objects.get(id=validated_data.get('enviado_por'))
        amistad = self.validate_message(validated_data.get('amistad'))
        mensaje_nuevo.amistad = amistad
        mensaje_nuevo.enviado_por = user
        mensaje_nuevo.mensaje = validated_data.get('mensaje')
        mensaje_nuevo.save()
        return mensaje_nuevo
    
    def validate_message(self, id_amistad):
        """
        Validate the message by checking if the amistad relation exists and is accepted.

        Args:
            id_amistad (int): The ID of the amistad relation.

        Returns:
            Solicitud_amistad: The validated amistad relation.

        Raises:
            serializers.ValidationError: If the amistad relation does not exist or is not accepted.
        """
        try:
            amistad = Solicitud_amistad.objects.get(id=id_amistad)
        except:
            raise serializers.ValidationError({'Error': 'No existe esta relacion de amistad'})
        
        if not amistad.is_aceptada:
            raise serializers.ValidationError({'Error': 'No existe una relacion de amistad entre los usuarios'})
        
        return amistad

class MensajeInfoSerializer(serializers.ModelSerializer):
    """
    Serializer class for the MensajeInfo model.
    """

    class Meta:
        model = Mensaje
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']