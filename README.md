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
