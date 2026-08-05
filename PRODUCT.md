# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Anunciante** — pessoa física que quer vender o próprio carro. Cria conta, cadastra o
veículo com foto e preço, informa telefone para contato. Gerencia apenas os próprios
anúncios. Não é profissional do setor: cadastra um ou dois carros, provavelmente uma vez
só, e quer que o anúncio fique pronto rápido.

**Comprador** — visitante não autenticado, navegando de desktop ou celular. Não cria conta.
Chega procurando um carro específico ou explorando faixa de preço. Precisa comparar opções,
avaliar se o carro serve, e falar com o vendedor. Sai do site para o WhatsApp — a conversão
acontece fora daqui.

O comprador é maioria absoluta do tráfego e nunca autentica. O anunciante é minoria, mas é
quem alimenta o catálogo.

## Product Purpose

Marketplace de carros usados entre particulares. Conecta quem quer vender ao quem quer
comprar, e sai do caminho: o site não intermedeia pagamento, não faz financiamento, não
valida o veículo. O sucesso é o comprador chegar ao WhatsApp do vendedor certo.

Sucesso do anunciante: publicar um anúncio completo em poucos minutos e receber contato.
Sucesso do comprador: encontrar carros compatíveis e ter informação suficiente para decidir
se vale a conversa.

## Positioning

Peça de portfólio que demonstra capacidade técnica full-stack em Django. Não compete com
marketplaces reais — a comparação relevante é com outros projetos de portfólio, e o
diferencial pretendido é parecer um produto de verdade, não um exercício de CRUD.

O único mecanismo incomum é a geração automática de descrição de venda por IA quando o
anunciante não escreve uma: reduz o atrito do cadastro e evita anúncios vazios.

## Operating Context

Comprador: navega em sessões curtas, frequentemente no celular, comparando várias abas ou
vários sites ao mesmo tempo. Escaneia preço, ano e foto antes de qualquer outra coisa.
Decide em segundos se abre o anúncio.

Anunciante: sessão única no desktop, com as fotos do carro já no computador. Preenche o
formulário uma vez. Abandona se for longo demais.

Contato acontece por WhatsApp, fora do site. Não há mensageria interna, notificação, nem
histórico de conversa.

## Capabilities and Constraints

**Existe hoje:** cadastro e login; CRUD de veículo restrito ao dono; catálogo público com
busca por marca, modelo e ano; paginação; página de detalhe com dados do veículo e contato;
perfil com telefone e e-mail; descrição gerada por IA (Mistral) quando ausente; snapshot de
inventário a cada alteração.

**Campos do veículo:** marca (FK), modelo, ano de fabricação, ano do modelo, placa, valor
(Decimal), status (novo/seminovo/usado), foto única, descrição.

**A adicionar nesta rodada:** quilometragem, câmbio, combustível, cor, múltiplas fotos por
veículo, favoritos funcionais, filtros e ordenação.

**Restrições técnicas:** Django 5.2 com templates server-side; sem framework de frontend e
sem build step — CSS e JS são servidos direto via WhiteNoise. Postgres em produção, SQLite
em desenvolvimento. Filesystem persistente necessário para `media/` (ou storage externo).

**Não existe e não deve ser inventado:** pagamento, financiamento, simulação de parcelas,
histórico veicular, laudo, avaliação de vendedor, chat interno, notificações, comparador
salvo entre sessões.

## Brand Commitments

**Nome: Southern San Andreas.** Fixo, definido pelo usuário. Aparece em header, footer e
títulos de página.

Referência declarada para a direção visual: estrutura funcional de marketplace (Webmotors)
com pele escura e premium (Southern San Andreas Super Autos, GTA V). O nome é do GTA, mas o
produto é um marketplace real entre particulares — a referência é estética, não literal.

Idioma: português do Brasil. Moeda em real, formato brasileiro (R$ 125.000,00).

## Evidence on Hand

**Fotos reais:** ~30 imagens em `media/cars/`, majoritariamente carros brasileiros de várias
épocas (Opala SS, Kombi, Uno, Corcel, Chevette, Fiat 147, Marea, S10, Toro, Corolla, Fusion,
Skyline R32). Acervo heterogêneo em qualidade e proporção — o layout precisa tolerar fotos
ruins e tamanhos irregulares.

**Não existe:** logotipo, fotografia de marca, depoimentos, números de tráfego, parcerias,
CNPJ, endereço físico. Nada disso pode ser fabricado — é peça de portfólio, mas conteúdo
falso apresentado como real desqualifica a peça.

Catálogo de demonstração: os carros cadastrados são dados de exemplo. O site deve funcionar
bem com poucos anúncios (5–20), que é o cenário realista aqui, e não quebrar com muitos.

## Product Principles

1. **O comprador não tem conta e nunca vai ter.** Tudo que importa para decidir precisa
   estar acessível sem login. Nada de parede de cadastro.
2. **A foto e o preço decidem.** São os dois elementos que o comprador processa primeiro;
   a hierarquia visual deve refletir isso em qualquer viewport.
3. **O caminho até o contato é a métrica.** Cada tela existe para aproximar o comprador do
   WhatsApp do vendedor. Qualquer elemento que não sirva a isso é candidato a corte.
4. **Cadastrar precisa ser curto.** O anunciante é amador e impaciente. Campo novo só entra
   se ajudar o comprador a decidir; o resto é opcional ou gerado.
5. **Não fingir escala que não existe.** Sem contadores inventados, selos de confiança
   falsos ou avaliações fictícias. Com 8 carros no catálogo, o design tem que parecer
   intencional, não vazio.

## Accessibility & Inclusion

Sem requisito formal declarado. Piso adotado: contraste AA, navegação completa por teclado
com foco visível, alvos de toque adequados no celular, e respeito a
`prefers-reduced-motion` — já implementado na rodada anterior e a ser preservado.

Tráfego majoritariamente móvel e em conexões variáveis: peso de página e lazy loading de
imagens são requisitos de inclusão, não só de performance.
