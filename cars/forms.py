from decimal import Decimal

from django import forms

from cars.models import Brand, Car, CarPhoto


class MultipleFileInput(forms.ClearableFileInput):
    """O Django 5 removeu o suporte a multiple=True no ClearableFileInput.

    Este par (widget + field) reintroduz o comportamento: o widget aceita
    varios arquivos e o field roda a validacao de imagem em cada um.
    """
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single = super().clean
        if isinstance(data, (list, tuple)):
            return [single(item, initial) for item in data]
        return [single(data, initial)] if data else []


class CarModelForm(forms.ModelForm):
    extra_photos = MultipleFileField(
        label='Mais fotos',
        required=False,
        help_text='Opcional. Selecione várias de uma vez.',
    )

    class Meta:
        model = Car
        exclude = ['carOwner']
        labels = {
            'modelCar': 'Modelo',
            'brandCar': 'Marca',
            'factoryYear': 'Ano de fabricação',
            'modelYear': 'Ano do modelo',
            'plateCar': 'Placa',
            'valueCar': 'Preço',
            'photo': 'Foto de capa',
            'bioCar': 'Descrição',
            'carStatus': 'Estado',
            'mileage': 'Quilometragem',
            'transmission': 'Câmbio',
            'fuel': 'Combustível',
            'color': 'Cor',
        }
        help_texts = {
            'factoryYear': 'A partir de 1975.',
            'valueCar': 'Mínimo de R$ 20.000.',
            'bioCar': 'Deixe em branco e nós escrevemos uma para você.',
            'plateCar': 'Formato ABC1234 ou ABC1D23.',
        }
        widgets = {
            'bioCar': forms.Textarea(attrs={'rows': 5}),
            'modelCar': forms.TextInput(attrs={'placeholder': 'Ex.: Opala SS'}),
            'color': forms.TextInput(attrs={'placeholder': 'Ex.: Prata'}),
            'mileage': forms.NumberInput(attrs={'placeholder': '0', 'min': 0}),
            'factoryYear': forms.NumberInput(attrs={'placeholder': '1978'}),
            'modelYear': forms.NumberInput(attrs={'placeholder': '1978'}),
            'valueCar': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '89000,00'}),
            'plateCar': forms.TextInput(attrs={'placeholder': 'ABC1D23'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brandCar'].empty_label = 'Selecione a marca'
        self.fields['transmission'].choices = (
            [('', 'Não informado')] + list(Car.TRANSMISSION_CHOICES)
        )
        self.fields['fuel'].choices = (
            [('', 'Não informado')] + list(Car.FUEL_CHOICES)
        )

    def clean_valueCar(self):
        valueCar = self.cleaned_data.get("valueCar")
        if valueCar is None:
            raise forms.ValidationError("Informe o preço do carro.")
        if valueCar < Decimal('20000'):
            raise forms.ValidationError("O preço mínimo é de R$ 20.000.")
        return valueCar

    def clean_factoryYear(self):
        factoryYear = self.cleaned_data.get("factoryYear")
        if factoryYear is None:
            raise forms.ValidationError("Informe o ano de fabricação.")
        if factoryYear < 1975:
            raise forms.ValidationError(
                "Não é possível cadastrar carros fabricados antes de 1975."
            )
        return factoryYear

    def clean_modelYear(self):
        modelYear = self.cleaned_data.get("modelYear")
        if modelYear is not None and modelYear < 1975:
            raise forms.ValidationError(
                "O ano do modelo não pode ser anterior a 1975."
            )
        return modelYear

    def clean(self):
        cleaned = super().clean()
        factoryYear = cleaned.get("factoryYear")
        modelYear = cleaned.get("modelYear")
        if factoryYear and modelYear and modelYear < factoryYear:
            self.add_error(
                "modelYear",
                "O ano do modelo não pode ser anterior ao ano de fabricação.",
            )
        return cleaned

    def save(self, commit=True):
        car = super().save(commit=commit)
        if commit:
            for i, image in enumerate(self.cleaned_data.get('extra_photos') or []):
                CarPhoto.objects.create(car=car, image=image, position=i)
        return car


class CarFilterForm(forms.Form):
    """Filtros da vitrine. Todos opcionais: a lista completa e um estado valido."""

    SORT_CHOICES = [
        ('-createdAt', 'Mais recentes'),
        ('valueCar', 'Menor preço'),
        ('-valueCar', 'Maior preço'),
        ('-factoryYear', 'Mais novos'),
        ('factoryYear', 'Mais antigos'),
        ('mileage', 'Menor quilometragem'),
    ]

    search = forms.CharField(required=False)
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(), required=False, empty_label='Todas',
    )
    status = forms.ChoiceField(
        choices=[('', 'Todos')] + Car.STATUS_CHOICES, required=False,
    )
    transmission = forms.ChoiceField(
        choices=[('', 'Todos')] + Car.TRANSMISSION_CHOICES, required=False,
    )
    fuel = forms.ChoiceField(
        choices=[('', 'Todos')] + Car.FUEL_CHOICES, required=False,
    )
    price_min = forms.DecimalField(required=False, min_value=0)
    price_max = forms.DecimalField(required=False, min_value=0)
    year_min = forms.IntegerField(required=False, min_value=1900)
    year_max = forms.IntegerField(required=False, min_value=1900)
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False)

    def clean(self):
        cleaned = super().clean()
        # Faixas invertidas sao erro de digitacao, nao de intencao: em vez de
        # devolver zero resultados sem explicacao, corrige a ordem.
        for lo, hi in (('price_min', 'price_max'), ('year_min', 'year_max')):
            a, b = cleaned.get(lo), cleaned.get(hi)
            if a is not None and b is not None and a > b:
                cleaned[lo], cleaned[hi] = b, a
        return cleaned

    @property
    def active_count(self):
        """Quantos filtros o visitante realmente aplicou (a ordenação não conta)."""
        if not self.is_valid():
            return 0
        return sum(
            1 for name, value in self.cleaned_data.items()
            if name != 'sort' and value not in (None, '', [])
        )
