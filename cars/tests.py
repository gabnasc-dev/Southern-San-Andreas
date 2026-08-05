from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cars.forms import CarModelForm
from cars.models import Brand, Car, CarInventory, CarPhoto
from cars.templatetags.car_extras import brl, km


# get_car_ai_bio faz chamada de rede; nos testes ela e sempre mockada.
@patch('cars.signals.get_car_ai_bio', return_value='Descricao de teste')
class CarModelTests(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(nameBrand='Fiat')
        self.user = User.objects.create_user(username='dono', password='senha-forte-123')

    def test_inventory_atualiza_ao_criar_carro(self, _mock_ai):
        Car.objects.create(
            modelCar='Uno', brandCar=self.brand, factoryYear=2015,
            valueCar=30000, carOwner=self.user,
        )
        inventory = CarInventory.objects.first()
        self.assertEqual(inventory.carsCount, 1)
        self.assertEqual(inventory.carsValue, 30000)

    def test_inventory_nao_duplica_snapshot_identico(self, _mock_ai):
        car = Car.objects.create(
            modelCar='Uno', brandCar=self.brand, factoryYear=2015,
            valueCar=30000, carOwner=self.user,
        )
        total_antes = CarInventory.objects.count()
        # Salvar de novo sem mudar contagem nem valor nao deve gerar novo registro
        car.save()
        self.assertEqual(CarInventory.objects.count(), total_antes)

    def test_valor_nao_sofre_erro_de_arredondamento(self, _mock_ai):
        """Estes tres valores somados como float dao 375172.58999999997.

        Como Decimal, o total do inventario fecha exatamente em 375172.59.
        """
        valores = [
            Decimal('110673.17'),
            Decimal('62237.77'),
            Decimal('202261.65'),
        ]
        for i, valor in enumerate(valores):
            Car.objects.create(
                modelCar=f'Carro {i}', brandCar=self.brand, factoryYear=2015,
                valueCar=valor, carOwner=self.user,
            )

        car = Car.objects.get(modelCar='Carro 0')
        self.assertIsInstance(car.valueCar, Decimal)
        self.assertEqual(car.valueCar, Decimal('110673.17'))

        total = CarInventory.objects.first().carsValue
        self.assertIsInstance(total, Decimal)
        self.assertEqual(total, Decimal('375172.59'))
        # A soma equivalente em float nao bate com o valor exato
        self.assertNotEqual(repr(sum(float(v) for v in valores)), '375172.59')

    def test_bio_gerada_pela_ia_quando_ausente(self, mock_ai):
        car = Car.objects.create(
            modelCar='Uno', brandCar=self.brand, factoryYear=2015,
            valueCar=30000, carOwner=self.user,
        )
        mock_ai.assert_called_once()
        self.assertEqual(car.bioCar, 'Descricao de teste')

    def test_carro_salva_mesmo_com_ia_indisponivel(self, mock_ai):
        mock_ai.return_value = None
        car = Car.objects.create(
            modelCar='Palio', brandCar=self.brand, factoryYear=2015,
            valueCar=30000, carOwner=self.user,
        )
        self.assertIsNone(car.bioCar)
        self.assertTrue(Car.objects.filter(pk=car.pk).exists())


class CarModelFormTests(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(nameBrand='Fiat')

    def _dados(self, **overrides):
        dados = {
            'modelCar': 'Uno',
            'brandCar': self.brand.pk,
            'factoryYear': 2015,
            'modelYear': 2016,
            'valueCar': 30000,
            'plateCar': 'ABC1D23',
            'carStatus': 'usado',
            'bioCar': 'Carro em bom estado.',
        }
        dados.update(overrides)
        return dados

    def test_formulario_valido(self):
        self.assertTrue(CarModelForm(data=self._dados()).is_valid())

    def test_valor_vazio_nao_quebra(self):
        """Antes levantava TypeError (None < 20000) e virava erro 500."""
        form = CarModelForm(data=self._dados(valueCar=''))
        self.assertFalse(form.is_valid())
        self.assertIn('valueCar', form.errors)

    def test_ano_fabricacao_vazio_nao_quebra(self):
        form = CarModelForm(data=self._dados(factoryYear=''))
        self.assertFalse(form.is_valid())
        self.assertIn('factoryYear', form.errors)

    def test_valor_abaixo_do_minimo(self):
        form = CarModelForm(data=self._dados(valueCar=1000))
        self.assertFalse(form.is_valid())
        self.assertIn('valueCar', form.errors)

    def test_ano_anterior_a_1975(self):
        form = CarModelForm(data=self._dados(factoryYear=1970, modelYear=1971))
        self.assertFalse(form.is_valid())
        self.assertIn('factoryYear', form.errors)

    def test_ano_modelo_anterior_ao_de_fabricacao(self):
        form = CarModelForm(data=self._dados(factoryYear=2016, modelYear=2015))
        self.assertFalse(form.is_valid())
        self.assertIn('modelYear', form.errors)

    def test_placa_invalida(self):
        form = CarModelForm(data=self._dados(plateCar='123'))
        self.assertFalse(form.is_valid())
        self.assertIn('plateCar', form.errors)


class FormatFilterTests(TestCase):
    def test_brl_sem_centavos(self):
        self.assertEqual(brl(Decimal('89000.00')), '89.000')

    def test_brl_com_centavos(self):
        self.assertEqual(brl(Decimal('87654.32')), '87.654,32')

    def test_brl_valor_ausente(self):
        self.assertEqual(brl(None), 'Sob consulta')

    def test_km_formatada(self):
        self.assertEqual(km(89000), '89.000 km')

    def test_km_zero_e_informacao(self):
        """0 km é um carro zero — diferente de não ter informado."""
        self.assertEqual(km(0), '0 km')

    def test_km_ausente(self):
        self.assertEqual(km(None), 'Km não informada')


@patch('cars.signals.get_car_ai_bio', return_value='Descricao de teste')
class CarViewTests(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(nameBrand='Chevrolet')
        self.dono = User.objects.create_user(username='dono', password='senha-forte-123')
        self.outro = User.objects.create_user(username='outro', password='senha-forte-123')

    def _criar_carro(self, **overrides):
        dados = {
            'modelCar': 'Opala', 'brandCar': self.brand, 'factoryYear': 1980,
            'valueCar': 50000, 'carOwner': self.dono,
        }
        dados.update(overrides)
        return Car.objects.create(**dados)

    def test_raiz_redireciona_para_lista(self, _mock_ai):
        self.assertRedirects(self.client.get('/'), reverse('cars_list'))

    def test_lista_acessivel_sem_login(self, _mock_ai):
        self._criar_carro()
        response = self.client.get(reverse('cars_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Opala')

    def test_busca_por_marca(self, _mock_ai):
        self._criar_carro()
        response = self.client.get(reverse('cars_list'), {'search': 'chevrolet'})
        self.assertContains(response, 'Opala')

    def test_busca_por_ano(self, _mock_ai):
        self._criar_carro()
        response = self.client.get(reverse('cars_list'), {'search': '1980'})
        self.assertContains(response, 'Opala')

    def test_busca_sem_resultado(self, _mock_ai):
        self._criar_carro()
        response = self.client.get(reverse('cars_list'), {'search': 'ferrari'})
        self.assertContains(response, 'Nenhum veículo com esses filtros')

    def test_novo_carro_exige_login(self, _mock_ai):
        response = self.client.get(reverse('new_car'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_nao_dono_nao_edita_carro(self, _mock_ai):
        car = self._criar_carro()
        self.client.login(username='outro', password='senha-forte-123')
        response = self.client.get(reverse('car_update', kwargs={'pk': car.pk}))
        self.assertEqual(response.status_code, 404)

    def test_nao_dono_nao_exclui_carro(self, _mock_ai):
        car = self._criar_carro()
        self.client.login(username='outro', password='senha-forte-123')
        response = self.client.post(reverse('car_delete', kwargs={'pk': car.pk}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Car.objects.filter(pk=car.pk).exists())

    def test_dono_exclui_carro(self, _mock_ai):
        car = self._criar_carro()
        self.client.login(username='dono', password='senha-forte-123')
        self.client.post(reverse('car_delete', kwargs={'pk': car.pk}))
        self.assertFalse(Car.objects.filter(pk=car.pk).exists())

    def test_detalhe_sem_telefone_nao_mostra_whatsapp(self, _mock_ai):
        car = self._criar_carro()
        response = self.client.get(reverse('car_detail', kwargs={'pk': car.pk}))
        self.assertNotContains(response, 'wa.me/55"')
        self.assertContains(response, 'Chamar no WhatsApp', count=0)

    # ---- filtros da vitrine ------------------------------------------------

    def test_filtro_por_faixa_de_preco(self, _mock_ai):
        self._criar_carro(modelCar='Barato', valueCar=30000)
        self._criar_carro(modelCar='Caro', valueCar=200000)
        response = self.client.get(reverse('cars_list'), {'price_max': 100000})
        self.assertContains(response, 'Barato')
        self.assertNotContains(response, '>Caro<')

    def test_filtro_por_cambio(self, _mock_ai):
        self._criar_carro(modelCar='Automatico', transmission='automatico')
        self._criar_carro(modelCar='Manualzinho', transmission='manual')
        response = self.client.get(reverse('cars_list'), {'transmission': 'manual'})
        self.assertContains(response, 'Manualzinho')
        self.assertNotContains(response, '>Automatico<')

    def test_faixa_invertida_e_corrigida(self, _mock_ai):
        """Digitar 100000 no mínimo e 50000 no máximo não deve zerar a lista."""
        self._criar_carro(modelCar='Meio', valueCar=75000)
        response = self.client.get(
            reverse('cars_list'), {'price_min': 100000, 'price_max': 50000}
        )
        self.assertContains(response, 'Meio')

    def test_ordenacao_por_menor_preco(self, _mock_ai):
        self._criar_carro(modelCar='Caro', valueCar=200000)
        self._criar_carro(modelCar='Barato', valueCar=30000)
        response = self.client.get(reverse('cars_list'), {'sort': 'valueCar'})
        corpo = response.content.decode()
        self.assertLess(corpo.index('Barato'), corpo.index('Caro'))

    def test_paginacao_preserva_filtros(self, _mock_ai):
        for i in range(14):
            self._criar_carro(modelCar=f'Carro {i}', transmission='manual')
        response = self.client.get(reverse('cars_list'), {'transmission': 'manual'})
        self.assertContains(response, 'transmission=manual&amp;page=2')

    # ---- galeria -----------------------------------------------------------

    def test_galeria_reune_capa_e_extras(self, _mock_ai):
        car = self._criar_carro(photo='cars/toro.jpg')
        CarPhoto.objects.create(car=car, image='cars/kombi.JPG', position=0)
        self.assertEqual(len(car.gallery), 2)

    def test_galeria_sem_capa_usa_so_extras(self, _mock_ai):
        car = self._criar_carro()
        CarPhoto.objects.create(car=car, image='cars/kombi.JPG')
        self.assertEqual(len(car.gallery), 1)

    # ---- painel do anunciante ---------------------------------------------

    def test_meus_anuncios_exige_login(self, _mock_ai):
        response = self.client.get(reverse('my_cars'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_meus_anuncios_mostra_so_os_proprios(self, _mock_ai):
        self._criar_carro(modelCar='MeuCarro', carOwner=self.dono)
        self._criar_carro(modelCar='CarroAlheio', carOwner=self.outro)
        self.client.login(username='dono', password='senha-forte-123')
        response = self.client.get(reverse('my_cars'))
        self.assertContains(response, 'MeuCarro')
        self.assertNotContains(response, 'CarroAlheio')


class SeedDemoCommandTests(TestCase):
    """O seed vai para um site público: contato plausível ali faria o botão de
    WhatsApp de um anúncio tocar o telefone de um desconhecido."""

    def setUp(self):
        from django.core.management import call_command
        from io import StringIO
        call_command('seed_demo', stdout=StringIO())

    def test_cria_o_catalogo(self):
        self.assertEqual(Car.objects.count(), 14)
        self.assertTrue(CarPhoto.objects.exists())

    def test_emails_usam_dominio_reservado(self):
        """example.com é reservado pela RFC 2606 — ninguém pode registrá-lo."""
        for user in User.objects.filter(username__endswith='.demo'):
            self.assertTrue(
                user.email.endswith('@example.com'),
                f'{user.username} tem e-mail fora do domínio reservado: {user.email}',
            )

    def test_telefones_sao_sequenciais(self):
        from accounts.templatetags.telefone_filters import remove_chars
        for user in User.objects.filter(username__endswith='.demo'):
            telefone = user.profile.telefone
            if not telefone:
                continue
            digitos = remove_chars(telefone)
            corpo = digitos[2:]  # sem o DDD
            self.assertTrue(
                corpo.startswith('91234'),
                f'{user.username} tem telefone sem o padrão fictício: {telefone}',
            )

    def test_nenhum_anuncio_pertence_a_conta_nao_demo(self):
        donos = set(Car.objects.values_list('carOwner__username', flat=True))
        for dono in donos:
            self.assertTrue(
                dono.endswith('.demo'),
                f'Anúncio da demo atribuído a conta real: {dono}',
            )

    def test_flush_nao_duplica(self):
        from django.core.management import call_command
        from io import StringIO
        call_command('seed_demo', '--flush', stdout=StringIO())
        self.assertEqual(Car.objects.count(), 14)

    def test_only_photos_nao_toca_no_banco(self):
        """Permite popular o banco de outra máquina: o banco é remoto e
        acessível, o disco do serviço não é."""
        from django.core.management import call_command
        from io import StringIO
        Car.objects.all().delete()
        User.objects.filter(username__endswith='.demo').delete()

        saida = StringIO()
        call_command('seed_demo', '--only-photos', stdout=saida)

        self.assertEqual(Car.objects.count(), 0)
        self.assertFalse(User.objects.filter(username__endswith='.demo').exists())
        self.assertIn('banco não alterado', saida.getvalue())

    def test_only_photos_publica_o_acervo(self):
        import shutil
        from pathlib import Path
        from django.conf import settings
        from django.core.management import call_command
        from io import StringIO

        destino = Path(settings.MEDIA_ROOT) / 'cars'
        if destino.exists():
            shutil.rmtree(destino)

        call_command('seed_demo', '--only-photos', stdout=StringIO())
        self.assertTrue(destino.is_dir())
        self.assertTrue(any(destino.iterdir()), 'nenhuma foto publicada')
