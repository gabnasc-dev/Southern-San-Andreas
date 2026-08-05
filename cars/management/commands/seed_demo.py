"""Popula o catálogo com anúncios de demonstração.

    python manage.py seed_demo
    python manage.py seed_demo --flush      # apaga a demo anterior antes
    python manage.py seed_demo --password X # senha das contas de demonstração

Todos os dados de contato são deliberadamente fictícios:

  * e-mails em @example.com — domínio reservado pela RFC 2606, que ninguém
    pode registrar, então nenhuma mensagem enviada por engano chega a alguém;
  * telefones em sequência óbvia (91234-5678), impossíveis de confundir com
    um número real — o botão de WhatsApp de um anúncio de vitrine tocaria o
    celular de um desconhecido se aqui houvesse um número plausível;
  * nomes de vendedores marcados com o sufixo `.demo`.

Nada aqui deve ser apresentado como cliente, venda ou depoimento real.
"""

import shutil
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from cars.models import Brand, Car, CarPhoto

# --- Vendedores de demonstração -------------------------------------------
# (username, primeiro nome, e-mail, telefone)
VENDEDORES = [
    ('ana.demo',     'Ana',     'ana.demo@example.com',     '(11) 91234-5678'),
    ('bruno.demo',   'Bruno',   'bruno.demo@example.com',   '(21) 91234-5679'),
    ('carla.demo',   'Carla',   'carla.demo@example.com',   '(31) 91234-5680'),
    # Sem telefone de propósito: exercita o estado em que o botão de WhatsApp
    # não aparece e o comprador cai no e-mail.
    ('diego.demo',   'Diego',   'diego.demo@example.com',   ''),
]

# --- Anúncios ---------------------------------------------------------------
# marca, modelo, ano fab, ano mod, placa, preço, km, câmbio, combustível,
# cor, foto de capa, estado, fotos extras, índice do vendedor
ANUNCIOS = [
    ('Chevrolet', 'Opala SS', 1978, 1978, 'ABC1D23', 89000, 78400, 'manual', 'gasolina', 'Vermelho',
     'cars/OPALA_SS.jpg', 'usado', ['cars/comodoro.jpg', 'cars/kadet.jpg'], 0),
    ('Volkswagen', 'Kombi', 1985, 1986, 'ABC1D24', 45000, 210500, 'manual', 'gasolina', 'Azul',
     'cars/kombi.JPG', 'usado', ['cars/kombi_4p27XHC.JPG', 'cars/kombi_Crq2dDz.JPG', 'cars/kombi_J3RLpFp.JPG'], 1),
    ('Fiat', 'Uno Firma', 1994, 1994, 'ABC1D25', 22000, 189000, 'manual', 'gasolina', 'Branco',
     'cars/uno_firma.jpg', 'usado', [], 3),
    ('Toyota', 'Corolla XEi', 2020, 2021, 'ABC1D26', 125000, 42300, 'automatico', 'flex', 'Preto',
     'cars/corolla.png', 'seminovo', [], 0),
    ('Ford', 'Fusion Titanium', 2014, 2014, 'ABC1D27', 78000, 118700, 'automatico', 'gasolina', 'Branco',
     'cars/fusion2014.jpg', 'seminovo', ['cars/fusion2014_IMgnmOk.jpg'], 2),
    ('Fiat', 'Toro Volcano', 2023, 2024, 'ABC1D28', 145000, 12400, 'automatico', 'diesel', 'Preto',
     'cars/toro.jpg', 'novo', [], 1),
    ('Nissan', 'Skyline GT-R R32', 1991, 1991, 'ABC1D29', 250000, 96000, 'manual', 'gasolina', 'Prata',
     'cars/r32.webp', 'usado', ['cars/r32_ADR5Ec8.webp'], 2),
    ('Chevrolet', 'S10 High Country', 2019, 2020, 'ABC1D30', 132000, 88900, 'automatico', 'diesel', 'Branco',
     'cars/s10.jpg', 'seminovo', ['cars/s10_J41REZc.jpg', 'cars/s10_RnKAPmY.jpg'], 0),
    ('Ford', 'Corcel II', 1980, 1980, 'ABC1D31', 32000, 154000, 'manual', 'gasolina', 'Bege',
     'cars/corcel.JPG', 'usado', ['cars/corcel_7xVd1Sf.JPG'], 1),
    ('Chevrolet', 'Chevette Tubarão', 1983, 1983, 'ABC1D32', 28000, 167000, 'manual', 'gasolina', 'Amarelo',
     'cars/chevette_tubarao.jpeg', 'usado', [], 3),
    ('Fiat', 'Marea Turbo 20V', 1999, 1999, 'ABC1D33', 41000, 143200, 'manual', 'gasolina', 'Cinza',
     'cars/marea_20v.jpg', 'usado', [], 2),
    ('Fiat', '147', 1982, 1982, 'ABC1D34', 24000, 198000, 'manual', 'etanol', 'Branco',
     'cars/fiat147.jpg', 'usado', [], 0),
    ('Fiat', 'Strada Working', 2018, 2019, 'ABC1D35', 62000, 71500, 'manual', 'flex', 'Branco',
     'cars/strada.jpg', 'seminovo', [], 1),
    ('Fiat', 'Elba Weekend', 1993, 1993, 'ABC1D36', 21000, 176000, 'manual', 'gasolina', 'Verde',
     'cars/elba.jpg', 'usado', [], 2),
]

DESCRICAO = (
    '{marca} {modelo} {ano}, {cor}, com {km} rodados. Câmbio {cambio}, '
    '{combustivel}. Documentação em dia, aceito avaliação na troca.'
)


def _milhar(n):
    return f'{n:,}'.replace(',', '.')


def _publicar_fotos(stdout):
    """Copia o acervo da demo de demo_assets/ para o MEDIA_ROOT.

    As fotos ficam fora de media/ de propósito: em Railway e Render o volume
    persistente é montado justamente sobre MEDIA_ROOT, e um volume montado
    esconde o que veio no repositório. Fotos versionadas dentro de media/
    sumiriam no primeiro deploy, deixando a vitrine inteira sem imagem.
    """
    origem = Path(settings.BASE_DIR) / 'demo_assets' / 'cars'
    destino = Path(settings.MEDIA_ROOT) / 'cars'

    if not origem.is_dir():
        stdout.write(f'  aviso: {origem} não existe; fotos não publicadas')
        return 0

    destino.mkdir(parents=True, exist_ok=True)
    copiadas = 0
    for arquivo in origem.iterdir():
        if not arquivo.is_file():
            continue
        alvo = destino / arquivo.name
        # Não sobrescreve: um upload real de mesmo nome tem precedência.
        if not alvo.exists():
            shutil.copy2(arquivo, alvo)
            copiadas += 1
    return copiadas


class Command(BaseCommand):
    help = 'Cria anúncios de demonstração com dados de contato fictícios.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true',
            help='Remove os anúncios e contas de demonstração antes de recriar.',
        )
        parser.add_argument(
            '--password', default='demo-southern-2026',
            help='Senha das contas de demonstração.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        senha = options['password']

        if options['flush']:
            apagados, _ = Car.objects.filter(
                carOwner__username__endswith='.demo'
            ).delete()
            User.objects.filter(username__endswith='.demo').delete()
            self.stdout.write(f'  removidos {apagados} registros da demo anterior')

        copiadas = _publicar_fotos(self.stdout)
        self.stdout.write(f'  {copiadas} fotos copiadas para {settings.MEDIA_ROOT}')

        vendedores = []
        for username, nome, email, telefone in VENDEDORES:
            user, criado = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'first_name': nome},
            )
            user.email = email
            user.first_name = nome
            user.set_password(senha)
            user.save()

            perfil = user.profile
            perfil.telefone = telefone
            perfil.save()

            vendedores.append(user)
            self.stdout.write(f'  vendedor {username} ({email}, {telefone or "sem telefone"})')

        # A geração de descrição por IA é uma chamada de rede paga; o seed traz
        # a própria descrição, então a chamada é neutralizada durante a carga.
        with patch('cars.signals.get_car_ai_bio', return_value=None):
            for dados in ANUNCIOS:
                (marca, modelo, fab, mod, placa, preco, quilometragem,
                 cambio, combustivel, cor, foto, estado, extras, idx) = dados

                brand, _ = Brand.objects.get_or_create(nameBrand=marca)
                car, _ = Car.objects.update_or_create(
                    modelCar=modelo,
                    brandCar=brand,
                    defaults=dict(
                        factoryYear=fab,
                        modelYear=mod,
                        plateCar=placa,
                        valueCar=Decimal(preco),
                        mileage=quilometragem,
                        transmission=cambio,
                        fuel=combustivel,
                        color=cor,
                        photo=foto,
                        carStatus=estado,
                        carOwner=vendedores[idx],
                        bioCar=DESCRICAO.format(
                            marca=marca, modelo=modelo, ano=fab,
                            cor=cor.lower(), km=_milhar(quilometragem) + ' km',
                            cambio=cambio, combustivel=combustivel,
                        ),
                    ),
                )

                car.photos.all().delete()
                for i, extra in enumerate(extras):
                    CarPhoto.objects.create(car=car, image=extra, position=i)

        self.stdout.write(self.style.SUCCESS(
            f'\n{Car.objects.count()} anúncios, '
            f'{CarPhoto.objects.count()} fotos adicionais, '
            f'{len(vendedores)} vendedores de demonstração.'
        ))
        self.stdout.write(
            f'Contas de demonstração: senha "{senha}". '
            'Contatos são fictícios (@example.com, telefones em sequência).'
        )
