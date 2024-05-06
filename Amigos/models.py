from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
User = get_user_model()

# Create your models here.
class Solicitud_amistad(models.Model):
    """
    Represents a friendship request between two users.

    Attributes:
        user_sender (User): The user who sent the friendship request.
        user_receptor (User): The user who received the friendship request.
        is_aceptada (bool): Indicates whether the friendship request has been accepted.
        created (datetime): The date and time when the friendship request was created.
    """

    user_sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    user_receptor = models.ForeignKey(User, related_name='receptor', on_delete=models.CASCADE)
    is_aceptada = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Solicitud-Amistad'
        verbose_name_plural = 'Solicitudes-Amistades'
        ordering = ['-created']
    

    def __str__(self) -> str:
        return f'{self.user_sender.username} to {self.user_receptor.username}'

# class Amistad(models.Model):
#     user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
#     user_amigo = models.ForeignKey(User, related_name='amigo', on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Amistad'
#         verbose_name_plural = 'Amistades'

class Mensaje(models.Model):
    """
    Represents a message in the application.
    
    Attributes:
        amistad (Solicitud_amistad): The friendship associated with the message.
        enviado_por (User): The user who sent the message.
        mensaje (str): The content of the message.
        created (datetime): The date and time when the message was created.
        time_expire (datetime): The date and time when the message will expire.
    """
    amistad = models.ForeignKey(Solicitud_amistad, on_delete=models.CASCADE)
    enviado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    time_expire = models.DateTimeField(default=(datetime.now() + timedelta(days=5)))


    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['-created']
    

    def __str__(self) -> str:
        return self.mensaje