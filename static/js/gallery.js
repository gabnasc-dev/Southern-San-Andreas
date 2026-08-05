/* Galeria do anúncio. Sem JS, a primeira foto continua visível e as miniaturas
   simplesmente não trocam — o anúncio permanece legível. */
(function () {
  'use strict';

  var raiz = document.querySelector('[data-gallery]');
  if (!raiz) return;

  var fotos = raiz.querySelectorAll('.gallery__shot');
  var miniaturas = raiz.querySelectorAll('[data-gallery-thumb]');
  var contador = raiz.querySelector('[data-gallery-counter]');
  var anterior = raiz.querySelector('[data-gallery-prev]');
  var proxima = raiz.querySelector('[data-gallery-next]');

  if (fotos.length < 2) return;

  var atual = 0;

  function mostrar(indice) {
    atual = (indice + fotos.length) % fotos.length;

    Array.prototype.forEach.call(fotos, function (foto, i) {
      foto.setAttribute('data-active', String(i === atual));
    });

    Array.prototype.forEach.call(miniaturas, function (thumb, i) {
      thumb.setAttribute('aria-current', String(i === atual));
    });

    if (contador) {
      contador.textContent = (atual + 1) + ' / ' + fotos.length;
    }
  }

  if (anterior) anterior.addEventListener('click', function () { mostrar(atual - 1); });
  if (proxima) proxima.addEventListener('click', function () { mostrar(atual + 1); });

  Array.prototype.forEach.call(miniaturas, function (thumb) {
    thumb.addEventListener('click', function () {
      mostrar(parseInt(thumb.getAttribute('data-gallery-thumb'), 10));
    });
  });

  // Setas do teclado funcionam quando a galeria tem o foco
  raiz.addEventListener('keydown', function (evento) {
    if (evento.key === 'ArrowLeft') { mostrar(atual - 1); evento.preventDefault(); }
    if (evento.key === 'ArrowRight') { mostrar(atual + 1); evento.preventDefault(); }
  });
})();
