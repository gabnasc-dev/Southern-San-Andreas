from decimal import Decimal

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from cars.models import Car, CarInventory
from django.db.models import Sum
from mistralai_api.client import get_car_ai_bio



def CarInventoryUpdate():
    carsCount = Car.objects.all().count() # SELECT * FROM CARS
    carsValue = Car.objects.aggregate(
        totalValue = Sum('valueCar') # {'totalValue': Decimal('100000.00')}
    )['totalValue'] or Decimal('0')

    # Só grava um novo snapshot se algo mudou de fato. Sem isso a tabela
    # crescia uma linha a cada save/delete, mesmo em edicoes que nao
    # alteravam nem a contagem nem o valor total.
    latest = CarInventory.objects.first()  # Meta.ordering = ['-createdAt']
    if latest and latest.carsCount == carsCount and latest.carsValue == carsValue:
        return

    CarInventory.objects.create(
        carsCount = carsCount,
        carsValue = carsValue,
    )

@receiver(pre_save, sender=Car)
def carPreSave(sender, instance, **kwargs):
    if not instance.bioCar:
        # get_car_ai_bio ja trata os proprios erros e devolve None se a IA
        # estiver indisponivel; nesse caso o carro e salvo sem descricao.
        ai_bio = get_car_ai_bio(
            instance.modelCar, instance.brandCar, instance.factoryYear
        )
        if ai_bio:
            instance.bioCar = ai_bio

@receiver(post_save, sender=Car)
def carPostSave(sender, instance, **kwargs):
    CarInventoryUpdate()


@receiver(post_delete, sender=Car)
def carPostDelete(sender, instance, **kwargs):
    CarInventoryUpdate()
