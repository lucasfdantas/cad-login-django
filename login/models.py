import random
import string
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

def gerador_codigo_mfa():
    #Gera um código MFA número com seis posições
    return ''.join(random.choices(string.digits, k=6))

class TwoFactorCode(models.Model):
    ''' Código temporário enviado durante o login em duas etapas.'''
    
        # Excluir o usuário também exclui seus códigos MFA relacionados.

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='two_factor_codes')
    
        # CharField preserva códigos que começam com zero.

    code = models.CharField(max_length=6, default=gerador_codigo_mfa)
    # Define o início da janela de validade do código.

    created_at = models.DateTimeField(auto_now_add=True)
        # Impede que o mesmo código seja aceito mais de uma vez.

    is_used = models.BooleanField(default=False)
    
    
    def is_valid(self):
        
        if self.is_used:
            return False
        expiration_time = self.created_at + timedelta(minutes=5)
        return timezone.now() <= expiration_time
    
    def mark_as_used(self):
        self.is_user = True
        self.save(update_fields=['is_used'])
        
    def __str__(self):
        return f'Código 2FA para {self.user} - {self.code}'
    
    
    
    