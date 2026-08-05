from decimal import Decimal

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import User

# Aceita o padrao antigo (ABC1234) e o Mercosul (ABC1D23), com ou sem hifen.
plate_validator = RegexValidator(
    regex=r'^[A-Za-z]{3}-?\d[A-Za-z0-9]\d{2}$',
    message='Placa inválida. Use o formato ABC1234 ou ABC1D23.',
)


class Brand(models.Model):
    idBrand = models.AutoField(primary_key=True)
    nameBrand = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['nameBrand']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nameBrand


class Car(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('seminovo', 'Seminovo'),
        ('usado', 'Usado'),
    ]
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatico', 'Automático'),
        ('automatizado', 'Automatizado'),
        ('cvt', 'CVT'),
    ]
    FUEL_CHOICES = [
        ('flex', 'Flex'),
        ('gasolina', 'Gasolina'),
        ('etanol', 'Etanol'),
        ('diesel', 'Diesel'),
        ('gnv', 'GNV'),
        ('eletrico', 'Elétrico'),
        ('hibrido', 'Híbrido'),
    ]
    idCar = models.AutoField(primary_key=True)
    modelCar = models.CharField(max_length=200)
    brandCar = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="carBrand")
    factoryYear = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1975)]
    )
    modelYear = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(1975)]
    )
    plateCar = models.CharField(
        max_length=10, blank=True, null=True, validators=[plate_validator]
    )
    # Decimal e nao Float: valor monetario com Float acumula erro de
    # arredondamento binario (0.1 + 0.2 != 0.3). max_digits=10 comporta
    # ate 99.999.999,99.
    valueCar = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True, validators=[MinValueValidator(Decimal('20000'))]
    )
    # Foto de capa: e a que aparece no card da listagem. Fotos adicionais
    # ficam em CarPhoto e so aparecem na galeria do detalhe.
    photo = models.ImageField(upload_to="cars/", blank=True, null=True)
    carOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ownerCar", null=True)
    carStatus = models.CharField(max_length=10, choices=STATUS_CHOICES, default='novo')

    mileage = models.PositiveIntegerField(
        'Quilometragem', blank=True, null=True,
        help_text='Em quilômetros rodados.',
    )
    transmission = models.CharField(
        'Câmbio', max_length=15, choices=TRANSMISSION_CHOICES, blank=True,
    )
    fuel = models.CharField(
        'Combustível', max_length=10, choices=FUEL_CHOICES, blank=True,
    )
    color = models.CharField('Cor', max_length=30, blank=True)

    bioCar = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        # Mais recentes primeiro: num marketplace o anuncio novo e o que
        # interessa, e ordem alfabetica por modelo nao diz nada ao comprador.
        ordering = ['-createdAt', 'modelCar']
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'
        indexes = [
            models.Index(fields=['carStatus']),
            models.Index(fields=['valueCar']),
            models.Index(fields=['factoryYear']),
        ]

    def __str__(self):
        return f'{self.brandCar} {self.modelCar}'

    @property
    def title(self):
        return f'{self.brandCar} {self.modelCar}'

    @property
    def gallery(self):
        """Capa + fotos adicionais, na ordem em que aparecem na galeria."""
        extras = list(self.photos.all())
        if self.photo:
            return [self.photo] + [p.image for p in extras]
        return [p.image for p in extras]


class CarPhoto(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='cars/')
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = 'Foto do carro'
        verbose_name_plural = 'Fotos do carro'

    def __str__(self):
        return f'Foto de {self.car}'


class CarInventory(models.Model):
    carsCount = models.IntegerField()
    # Acompanha o tipo de Car.valueCar: guardar a soma de Decimals em Float
    # reintroduziria o erro de arredondamento que estamos eliminando.
    # max_digits maior porque este campo e a soma de todos os carros.
    carsValue = models.DecimalField(max_digits=14, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-createdAt']

    def __str__(self):
        return f'{self.carsCount} - {self.carsValue}'