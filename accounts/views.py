from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView
from accounts.models import Profile
from accounts.forms import ProfileForm


def registerView(request):
    if request.user.is_authenticated:
        return redirect("cars_list")

    if request.method == "POST":
        userForm = UserCreationForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            messages.success(request, "Conta criada com sucesso! Faça login para continuar.")
            return redirect("login")
    else:
        userForm = UserCreationForm()
    return render(
        request,
        'register.html',
        {'userForm': userForm}
    )


def loginView(request):
    if request.user.is_authenticated:
        return redirect("cars_list")

    if request.method == "POST":
        loginForm = AuthenticationForm(request, data=request.POST)
        if loginForm.is_valid():
            user = loginForm.get_user()
            login(request, user)
            return redirect("cars_list")
    else:
        loginForm = AuthenticationForm()
    return render(
        request,
        'login.html',
        {
            'loginForm': loginForm,
            # Só aparece se as duas variáveis existirem no ambiente.
            'demo_user': settings.DEMO_USER,
            'demo_password': settings.DEMO_PASSWORD,
        }
    )


@require_POST
def logoutView(request):
    """Logout apenas via POST: por GET qualquer link/prefetch externo
    conseguiria deslogar o usuario (CSRF de logout)."""
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect("cars_list")


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profileUpdate.html'
    success_url = '/cars/'

    def get_object(self, queryset=None):
        # get_or_create protege contas criadas antes do signal de perfil
        # existir (ex.: superusuarios antigos ou importados por fixture).
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Perfil atualizado com sucesso.")
        return super().form_valid(form)
