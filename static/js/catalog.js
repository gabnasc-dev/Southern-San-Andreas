/* Vitrine: gaveta de filtros, ordenação e favoritos.
   Sem dependências. O site funciona inteiro sem este arquivo — ele só
   encurta caminhos que já existem em HTML. */
(function () {
  'use strict';

  /* ---- Gaveta de filtros no celular ---------------------------------- */
  var rail = document.getElementById('rail');
  var toggle = document.querySelector('[data-rail-toggle]');

  if (rail && toggle) {
    toggle.addEventListener('click', function () {
      var open = rail.getAttribute('data-open') === 'true';
      rail.setAttribute('data-open', String(!open));
      toggle.setAttribute('aria-expanded', String(!open));
    });
  }

  /* ---- O botão "Aplicar" só acende quando há algo para aplicar --------- */
  if (rail) {
    rail.addEventListener('input', function () {
      rail.setAttribute('data-dirty', 'true');
    });
    rail.addEventListener('change', function () {
      rail.setAttribute('data-dirty', 'true');
    });
  }

  /* ---- Ordenação: aplica sozinha, preservando os filtros da URL ------- */
  var sort = document.querySelector('[data-sort]');
  if (sort) {
    sort.addEventListener('change', function () {
      var params = new URLSearchParams(window.location.search);
      params.set('sort', sort.value);
      params.delete('page');
      window.location.search = params.toString();
    });
  }

  /* ---- Favoritos -----------------------------------------------------
     Ficam no navegador, não na conta: o comprador nunca se cadastra, então
     exigir login para salvar um carro seria uma parede sem propósito. */
  var STORE = 'ssa:favoritos';

  function read() {
    try {
      var raw = window.localStorage.getItem(STORE);
      var list = raw ? JSON.parse(raw) : [];
      return Array.isArray(list) ? list : [];
    } catch (e) {
      return [];
    }
  }

  function write(list) {
    try {
      window.localStorage.setItem(STORE, JSON.stringify(list));
    } catch (e) {
      /* modo privativo ou cota cheia: o botão ainda responde na sessão */
    }
  }

  var favoritos = read();
  var botoes = document.querySelectorAll('[data-fav]');

  Array.prototype.forEach.call(botoes, function (botao) {
    var id = botao.getAttribute('data-fav');
    var salvo = favoritos.indexOf(id) !== -1;

    botao.setAttribute('aria-pressed', String(salvo));
    rotular(botao, salvo);

    botao.addEventListener('click', function (event) {
      // O botão vive dentro do link do card; sem isto, salvar abriria o anúncio
      event.preventDefault();
      event.stopPropagation();

      var index = favoritos.indexOf(id);
      var agora = index === -1;

      if (agora) {
        favoritos.push(id);
      } else {
        favoritos.splice(index, 1);
      }

      write(favoritos);
      botao.setAttribute('aria-pressed', String(agora));
      rotular(botao, agora);
    });
  });

  function rotular(botao, salvo) {
    var nome = botao.getAttribute('data-fav-name') || 'veículo';
    botao.setAttribute('aria-label', (salvo ? 'Remover ' : 'Salvar ') + nome);
    botao.setAttribute('title', salvo ? 'Salvo' : 'Salvar');
  }
})();
