from cars.models import Car
from cars.forms import CarFilterForm, CarModelForm
from django.contrib import messages
from django.db.models import F, Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView


class carsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    paginate_by = 12

    def get_queryset(self):
        cars = super().get_queryset().select_related('brandCar')

        form = CarFilterForm(self.request.GET or None)
        self.filter_form = form
        if not form.is_valid():
            return cars

        data = form.cleaned_data

        if data.get('search'):
            term = data['search'].strip()
            filters = (
                Q(modelCar__icontains=term)
                | Q(brandCar__nameBrand__icontains=term)
                | Q(color__icontains=term)
            )
            if term.isdigit():
                year = int(term)
                filters |= Q(factoryYear=year) | Q(modelYear=year)
            cars = cars.filter(filters)

        if data.get('brand'):
            cars = cars.filter(brandCar=data['brand'])
        if data.get('status'):
            cars = cars.filter(carStatus=data['status'])
        if data.get('transmission'):
            cars = cars.filter(transmission=data['transmission'])
        if data.get('fuel'):
            cars = cars.filter(fuel=data['fuel'])
        if data.get('price_min') is not None:
            cars = cars.filter(valueCar__gte=data['price_min'])
        if data.get('price_max') is not None:
            cars = cars.filter(valueCar__lte=data['price_max'])
        if data.get('year_min') is not None:
            cars = cars.filter(factoryYear__gte=data['year_min'])
        if data.get('year_max') is not None:
            cars = cars.filter(factoryYear__lte=data['year_max'])

        # Anuncios sem o campo ordenado vao para o fim da lista em vez de
        # encabecar a vitrine com um vazio.
        sort = data.get('sort') or '-createdAt'
        field = sort.lstrip('-')
        order = F(field).desc(nulls_last=True) if sort.startswith('-') else F(field).asc(nulls_last=True)
        return cars.order_by(order, '-idCar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        context['active_filters'] = self.filter_form.active_count
        # Querystring sem "page", para os links de paginacao preservarem filtros
        params = self.request.GET.copy()
        params.pop('page', None)
        context['querystring'] = params.urlencode()
        return context


class carDetailView(DetailView):
    model = Car
    template_name = 'carDetail.html'

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('brandCar', 'carOwner__profile')
            .prefetch_related('photos')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Outros anuncios da mesma marca, para o comprador continuar navegando
        context['related'] = (
            Car.objects.filter(brandCar=self.object.brandCar)
            .exclude(pk=self.object.pk)
            .select_related('brandCar')[:3]
        )
        # Mensagem ja escrita no WhatsApp: o comprador so aperta enviar, e o
        # vendedor recebe o contato ja sabendo de qual anuncio se trata.
        context['whatsapp_text'] = (
            f'Olá! Vi o {self.object.title} {self.object.factoryYear or ""} '
            f'anunciado na Southern San Andreas e queria saber mais.'
        ).strip()
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class newCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'newCar.html'

    def form_valid(self, form):
        form.instance.carOwner = self.request.user # vincula o carro ao usuario
        messages.success(self.request, "Anúncio publicado.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='login'), name='dispatch')
class carUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'carUpdate.html'

    def get_queryset(self):
        return Car.objects.filter(carOwner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Anúncio atualizado.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required(login_url='login'),name='dispatch')
class carDeleteView(DeleteView):
    model = Car
    template_name = 'carDelete.html'
    success_url = '/cars/'

    def get_queryset(self):
        return Car.objects.filter(carOwner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Anúncio removido.")
        return super().form_valid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class myCarsListView(ListView):
    """Painel do anunciante: so os proprios anuncios."""
    model = Car
    template_name = 'myCars.html'
    context_object_name = 'cars'
    paginate_by = 12

    def get_queryset(self):
        return (
            Car.objects.filter(carOwner=self.request.user)
            .select_related('brandCar')
            .order_by('-createdAt')
        )
