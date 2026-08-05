#!/usr/bin/env bash
# Comando de build para Render (e utilizável em qualquer plataforma).
# No Render, cole em "Build Command": ./build.sh
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Estáticos são servidos pelo WhiteNoise, então precisam ser coletados no build.
python manage.py collectstatic --noinput

# O Render não tem fase de "release" separada, então a migração roda aqui.
# É idempotente.
python manage.py migrate --noinput

# --- Carga inicial ---------------------------------------------------------
# O plano gratuito do Render não dá acesso a shell, então o build é o único
# lugar onde dá para rodar um comando. Ambos os passos abaixo são opcionais e
# controlados por variável de ambiente, para que um deploy comum não recrie
# dados sem você mandar.

# SEED_DEMO=true  -> publica o catálogo de demonstração.
# Rode uma vez e depois remova a variável: o comando é idempotente, mas
# mantê-lo ligado desfaz qualquer edição feita nos anúncios de exemplo.
#
# A comparação é insensível a maiúsculas e aceita 1/yes/sim: a variável é
# digitada à mão no painel da plataforma, e um "True" silenciosamente ignorado
# custa um ciclo inteiro de deploy para descobrir.
SEED_NORM=$(printf '%s' "${SEED_DEMO:-}" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')

echo "--- Carga inicial ---"
echo "SEED_DEMO recebido: '${SEED_DEMO:-<vazio>}' (normalizado: '${SEED_NORM}')"

case "${SEED_NORM}" in
  true|1|yes|sim|y|s)
    echo "Publicando o catálogo de demonstração..."
    python manage.py seed_demo --password "${DEMO_PASSWORD:-demo-southern-2026}"
    ;;
  *)
    echo "SEED_DEMO não ativo; catálogo não alterado."
    echo "Para popular, defina SEED_DEMO=true e faça um novo deploy."
    ;;
esac

# DJANGO_SUPERUSER_USERNAME + DJANGO_SUPERUSER_PASSWORD -> cria/atualiza o admin.
# Sem elas o comando não faz nada. Depois de criar a conta, remova as variáveis:
# a senha fica visível no painel da plataforma enquanto estiverem lá.
python manage.py ensure_superuser
