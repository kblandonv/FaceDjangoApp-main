from django.db import models
from django.contrib.auth.models import User

class LogoPerfil(models.Model):
    """
    Represents the logo for a user's profile.

    Attributes:
        user (ForeignKey): The user associated with the logo.
        url_imagen (CharField): The URL of the logo image.

    Meta:
        verbose_name (str): The singular name for the model.
        verbose_name_plural (str): The plural name for the model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_imagen = models.CharField(max_length=500, default='https://img2.freepng.es/20180401/dbq/kisspng-user-profile-computer-icons-profile-5ac09245049c32.0935523415225697970189.jpg')

    class Meta:
        verbose_name = 'Logo'
        verbose_name_plural = 'Logos'

    def __str__(self) -> str:
        return f'{self.user.username}'