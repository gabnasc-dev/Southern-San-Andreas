# Sistema de Revenda de Carros

Este projeto é um **sistema de revenda de carros** desenvolvido em **Python** utilizando o framework **Django** (padrão MVT – Model-View-Template) e **PostgreSQL** como banco de dados.

O sistema permite o **gerenciamento completo de veículos**, desde a adição de novos carros ao catálogo até a exclusão de registros, passando pela visualização detalhada e atualização de informações.

Uma funcionalidade inovadora é a **integração com Inteligência Artificial**, que gera automaticamente descrições para os carros quando estas não são fornecidas, otimizando o processo de cadastro e enriquecendo a apresentação dos veículos.

---

## Tecnologias Utilizadas

- **Python 3.13** – Linguagem de programação principal
- **Django 5.2** – Framework web de alto nível para desenvolvimento rápido e seguro
- **PostgreSQL** – Banco de dados relacional robusto
- **WhiteNoise** – Servir arquivos estáticos em produção
- **Inteligência Artificial (IA)** – Integração para geração automática de descrições de veículos
  - IA utilizada: **Mistral AI**

---

## Funcionalidades Principais

- **Adicionar Carro** – Cadastra novos veículos no sistema, incluindo marca, modelo, ano, preço e descrição (gerada automaticamente pela IA, caso não fornecida)
- **Listar Carros** – Exibe o catálogo com busca por marca, modelo ou ano, e paginação
- **Ver Detalhes do Carro** – Informações detalhadas, dados de contato do anunciante e link de WhatsApp
- **Atualizar Carro** – Edição restrita ao dono do anúncio
- **Deletar Carro** – Remoção restrita ao dono do anúncio
- **Perfil do Usuário** – Cadastro de telefone e e-mail para contato
- **Integração com IA** – Geração automática de descrições para veículos sem descrição prévia

---

## Como rodar localmente

### 1. Pré-requisitos

- Python 3.13 ou 3.14
- **Nenhum banco precisa ser instalado.** Em desenvolvimento o projeto usa SQLite
  automaticamente. O PostgreSQL só entra em produção.

### 2. Clonar e criar o ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente:

```bash
venv\Scripts\activate
```

No Linux/macOS use `source venv/bin/activate`.

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Copie o arquivo de exemplo e preencha os valores:

```bash
copy .env.example .env
```

Gere uma `SECRET_KEY` nova (o Django exige pelo menos 50 caracteres):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Variáveis disponíveis:

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | sim | Chave secreta do Django (50+ caracteres) |
| `DEBUG` | não | `True` em desenvolvimento, `False` em produção (padrão: `False`) |
| `ALLOWED_HOSTS` | em produção | Domínios permitidos, separados por vírgula |
| `CSRF_TRUSTED_ORIGINS` | em produção HTTPS | Origens com esquema, separadas por vírgula |
| `DATABASE_URL` | só em produção | URL do banco. Em dev, deixe em branco: com `DEBUG=True` o Django usa `db.sqlite3` automaticamente |
| `MISTRAL_KEY` | não | Chave da API Mistral. Se vazia, o cadastro funciona sem descrição gerada |
| `SECURE_SSL_REDIRECT` | não | Desative se o proxy já redireciona para HTTPS |

### 5. Aplicar as migrações

```bash
python manage.py migrate
```

### 6. Criar um usuário administrador

```bash
python manage.py createsuperuser
```

### 7. Rodar o servidor

```bash
python manage.py runserver
```

A aplicação fica disponível em http://127.0.0.1:8000/ (a raiz redireciona para `/cars/`).

---

## Testes

```bash
python manage.py test
```

As chamadas à API da Mistral são substituídas por mocks nos testes, então a suíte roda sem rede e sem consumir cota.

---

## Dados de demonstração

O catálogo de exemplo é criado por um comando, não por um dump de banco:

```bash
python manage.py seed_demo
```

Para recriar do zero (apaga os anúncios e contas de demonstração antes):

```bash
python manage.py seed_demo --flush
```

**Todo contato do seed é deliberadamente fictício**, porque o site é público:

- e-mails em `@example.com` — domínio reservado pela RFC 2606, que ninguém pode
  registrar, então nenhuma mensagem enviada por engano chega a uma pessoa real;
- telefones em sequência óbvia (`(11) 91234-5678`). Um número plausível aqui
  faria o botão de WhatsApp de um anúncio tocar o celular de um desconhecido;
- contas com sufixo `.demo`, o que permite ao `--flush` distinguir a demo de
  anúncios reais e nunca apagar os de terceiros.

Há testes que travam isso (`cars.tests.SeedDemoCommandTests`) — se alguém editar
o seed e colocar um contato de aparência real, a suíte falha.

As fotos ficam em `demo_assets/`, versionadas, e o comando as copia para o
`MEDIA_ROOT`. Elas **não** ficam em `media/` de propósito: em produção esse
diretório é um volume montado, e um volume esconde o que veio no repositório —
fotos versionadas ali sumiriam no primeiro deploy.

Para exibir a credencial de demonstração na tela de login, defina `DEMO_USER` e
`DEMO_PASSWORD` no ambiente. Sem as duas, a dica não aparece.

---

## Deploy no Render (plano gratuito)

Precisa de um Postgres externo — o do próprio Render é apagado depois de 30
dias no plano gratuito. Use o **Neon** (neon.tech), que é gratuito sem prazo.

### Serviço

**New → Web Service** → conecte o repositório e configure:

| Campo | Valor |
|---|---|
| Build Command | `./build.sh` |
| Start Command | `gunicorn app.wsgi --bind 0.0.0.0:$PORT` |
| Instance Type | Free |

### Variáveis

| Variável | Valor |
|---|---|
| `SECRET_KEY` | gere uma nova, 50+ caracteres |
| `DEBUG` | `False` |
| `DATABASE_URL` | a connection string do Neon |
| `PYTHON_VERSION` | `3.13.1` |
| `DEMO_USER` / `DEMO_PASSWORD` | opcional, exibe a credencial no login |

`ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` são preenchidos a partir do
`RENDER_EXTERNAL_HOSTNAME`, que o Render injeta sozinho.

### Carga inicial sem terminal

O plano gratuito não dá acesso a shell, então o `build.sh` faz o trabalho —
mas só quando você pede. Adicione **temporariamente**:

| Variável | Valor |
|---|---|
| `SEED_DEMO` | `true` |
| `DJANGO_SUPERUSER_USERNAME` | seu usuário de admin |
| `DJANGO_SUPERUSER_PASSWORD` | uma senha forte |
| `DJANGO_SUPERUSER_EMAIL` | opcional |

Faça um deploy manual e **remova as quatro depois**. Motivos:

- com `SEED_DEMO=true` ligado, todo deploy desfaz edições feitas nos anúncios
  de exemplo;
- a senha do admin fica visível no painel enquanto a variável existir.

O `ensure_superuser` é idempotente — rodar de novo atualiza a senha em vez de
falhar, que é o que o `createsuperuser --noinput` faria (derrubando o build).

### Limitações do plano gratuito

**O serviço dorme** após ~15 minutos sem acesso; o primeiro request depois
disso leva cerca de 50 segundos.

**Não há disco persistente.** Uploads feitos por visitantes desaparecem no
próximo deploy. As fotos da demonstração **não** são afetadas: vêm de
`demo_assets/`, versionado, e o `seed_demo` as recria. Se precisar que os
uploads sobrevivam, o caminho é um storage externo (S3, R2, Cloudinary) ou uma
plataforma com disco.

---

## Deploy no Railway

O projeto já traz `Procfile`, `build.sh` e `.python-version`.

### 1. Suba o código para o GitHub

### 2. Crie o serviço

**Railway:** New Project → Deploy from GitHub. Ele detecta o `Procfile` sozinho.

**Render:** New → Web Service. Build Command `./build.sh`, Start Command
`gunicorn app.wsgi --bind 0.0.0.0:$PORT`.

### 3. Adicione o banco

Crie um PostgreSQL no mesmo projeto. Railway e Render injetam a `DATABASE_URL`
automaticamente no serviço web — não precisa copiar nada.

### 4. Monte um volume para as fotos

Este passo é o que faz os uploads sobreviverem ao deploy. Monte em `/app/media`
(Railway) ou no caminho equivalente do Render. Sem volume, toda foto que um
usuário enviar desaparece na próxima publicação.

### 5. Configure as variáveis

| Variável | Valor |
|---|---|
| `SECRET_KEY` | gere uma nova, 50+ caracteres |
| `DEBUG` | `False` |
| `MISTRAL_KEY` | sua chave, ou deixe vazia |
| `DEMO_USER` | `ana.demo` (opcional) |
| `DEMO_PASSWORD` | a senha que você passar ao `seed_demo` (opcional) |

`ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` são preenchidos sozinhos a partir do
domínio que a plataforma gera. Só configure manualmente se usar domínio próprio.

### 6. Popule o catálogo

Depois do primeiro deploy, no console da plataforma:

```bash
python manage.py seed_demo --password SUA_SENHA_DEMO
```

E crie seu acesso ao admin:

```bash
python manage.py createsuperuser
```

### 7. Confira

```bash
python manage.py check --deploy
```

---

## Deploy em servidor próprio

1. Defina `DEBUG=False`, `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` no `.env`.
2. Rode o checklist de segurança do Django:

```bash
python manage.py check --deploy
```

3. Colete os arquivos estáticos:

```bash
python manage.py collectstatic --noinput
```

4. Sirva a aplicação com `gunicorn app.wsgi` ou com o uWSGI (`carros_uwsgi.ini`).

### Banco de dados em produção

Qualquer Postgres gerenciado funciona — basta definir `DATABASE_URL`. Serviços comuns:
Neon, Supabase, Railway, Render. A maioria exige SSL, então acrescente `?sslmode=require`
ao final da URL.

Migrar do SQLite de desenvolvimento para o Postgres de produção é só rodar `migrate`
apontando para o novo banco — não é preciso transferir dados, já que o SQLite local
serve apenas para testes.

### Arquivos de mídia

As fotos enviadas pelos usuários ficam em `media/`. O `urls.py` tem um fallback que serve
esses arquivos pelo próprio Django quando `DEBUG=False`, para o site não quebrar — mas isso
é ineficiente e **só funciona onde o disco é persistente** (VPS, Railway com volume, Render
com disk).

Em servidor próprio, o recomendado é um alias no nginx:

```nginx
location /media/ {
    alias /var/www/carros/media/;
}
```

> **Atenção em plataformas serverless (Vercel, Netlify, Cloud Run):** o filesystem é
> efêmero. As fotos enviadas pelos usuários são apagadas a cada deploy — e, no caso da
> Vercel, entre invocações. Como este projeto é centrado em fotos de carros, hospedar lá
> **exige** um storage externo antes: S3, Cloudflare R2, Supabase Storage ou Cloudinary
> (via `django-storages`). Sem isso, todo upload se perde.
>
> Se a ideia é o caminho mais curto, uma plataforma com disco persistente
> (Railway, Render, Fly.io) ou uma VPS evita esse trabalho inteiro.

---

## Estrutura do projeto

```
app/               configuração do Django (settings, urls, wsgi) e template base
accounts/          autenticação, perfil do usuário e filtros de telefone
cars/              models, views, forms e templates dos veículos
mistralai_api/     cliente da API da Mistral
static/            CSS e JS servidos ao navegador
media/             fotos enviadas pelos usuários (não versionar)
```

---

## Status do Projeto

- **Versão:** BETA
- **Status:** Em desenvolvimento ativo 🚧

---

## Licença

Este projeto é de uso **educacional** e não possui fins comerciais.
