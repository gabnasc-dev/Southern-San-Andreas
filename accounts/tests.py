from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile
from accounts.templatetags.telefone_filters import format_telefone, remove_chars


class ProfileSignalTests(TestCase):
    def test_perfil_criado_junto_com_usuario(self):
        user = User.objects.create_user(username='joao', password='senha-forte-123')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_signal_e_idempotente(self):
        user = User.objects.create_user(username='joao', password='senha-forte-123')
        user.save()  # dispara post_save de novo
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)


class AuthViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='joao', password='senha-forte-123')

    def test_login_valido_redireciona_para_lista(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'joao', 'password': 'senha-forte-123'},
        )
        self.assertRedirects(response, reverse('cars_list'))

    def test_logout_por_get_e_bloqueado(self):
        """GET nao pode deslogar: um prefetch ou imagem externa faria isso."""
        self.client.login(username='joao', password='senha-forte-123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(self.client.session.get('_auth_user_id'))

    def test_logout_por_post_funciona(self):
        self.client.login(username='joao', password='senha-forte-123')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('cars_list'))
        self.assertIsNone(self.client.session.get('_auth_user_id'))


class ProfileUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='joao', password='senha-forte-123')

    def test_anonimo_e_redirecionado_para_login(self):
        """Antes retornava erro 500 em vez de redirecionar."""
        response = self.client.get(reverse('profile_update'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_usuario_sem_perfil_nao_quebra(self):
        Profile.objects.filter(user=self.user).delete()
        self.client.login(username='joao', password='senha-forte-123')
        response = self.client.get(reverse('profile_update'))
        self.assertEqual(response.status_code, 200)

    def test_atualiza_telefone_e_email(self):
        self.client.login(username='joao', password='senha-forte-123')
        self.client.post(
            reverse('profile_update'),
            {'telefone': '(11) 98765-4321', 'email': 'joao@exemplo.com'},
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'joao@exemplo.com')
        self.assertEqual(self.user.profile.telefone, '(11) 98765-4321')


class TelefoneFilterTests(TestCase):
    def test_format_telefone_celular(self):
        self.assertEqual(format_telefone('11987654321'), '(11) 98765-4321')

    def test_format_telefone_fixo(self):
        self.assertEqual(format_telefone('1133334444'), '(11) 3333-4444')

    def test_format_telefone_valor_vazio(self):
        self.assertEqual(format_telefone(None), '')

    def test_remove_chars(self):
        self.assertEqual(remove_chars('(11) 98765-4321'), '11987654321')

    def test_remove_chars_vazio(self):
        self.assertEqual(remove_chars(None), '')
