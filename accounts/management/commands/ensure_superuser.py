"""Cria ou atualiza o superusuário a partir de variáveis de ambiente.

    DJANGO_SUPERUSER_USERNAME=matheus
    DJANGO_SUPERUSER_PASSWORD=...
    DJANGO_SUPERUSER_EMAIL=...        (opcional)

    python manage.py ensure_superuser

Existe porque o `createsuperuser --noinput` do Django falha quando a conta já
existe, e no plano gratuito de plataformas como o Render não há shell: o único
lugar onde dá para rodar um comando é o build, que roda a cada deploy. Este
comando é idempotente, então pode ficar no build sem quebrar a publicação.

Sem as variáveis definidas ele não faz nada e sai com sucesso — assim o build
de quem não quer criar admin automático não falha.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Cria ou atualiza o superusuário a partir das variáveis DJANGO_SUPERUSER_*.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', '').strip()
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '').strip()
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '').strip()

        if not username or not password:
            self.stdout.write(
                'DJANGO_SUPERUSER_USERNAME/PASSWORD não definidas; nenhum admin criado.'
            )
            return

        User = get_user_model()
        user, criado = User.objects.get_or_create(username=username)

        user.is_staff = True
        user.is_superuser = True
        if email:
            user.email = email
        user.set_password(password)
        user.save()

        verbo = 'criado' if criado else 'atualizado'
        self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" {verbo}.'))
