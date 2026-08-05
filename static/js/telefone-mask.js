// Mascara de telefone em JS puro: substitui jQuery + jquery.mask (~90 KB de CDN)
// por ~1 KB local. Formata como (00) 00000-0000 ou (00) 0000-0000.
(function () {
  'use strict';

  function formatarTelefone(valor) {
    var digitos = valor.replace(/\D/g, '').slice(0, 11);

    if (digitos.length === 0) {
      return '';
    }
    if (digitos.length <= 2) {
      return '(' + digitos;
    }
    if (digitos.length <= 6) {
      return '(' + digitos.slice(0, 2) + ') ' + digitos.slice(2);
    }
    if (digitos.length <= 10) {
      return '(' + digitos.slice(0, 2) + ') ' + digitos.slice(2, 6) + '-' + digitos.slice(6);
    }
    return '(' + digitos.slice(0, 2) + ') ' + digitos.slice(2, 7) + '-' + digitos.slice(7);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var campos = document.querySelectorAll('.telefone-mask');

    Array.prototype.forEach.call(campos, function (campo) {
      campo.setAttribute('inputmode', 'tel');
      campo.setAttribute('placeholder', '(00) 00000-0000');
      campo.value = formatarTelefone(campo.value);

      campo.addEventListener('input', function () {
        campo.value = formatarTelefone(campo.value);
      });
    });
  });
})();
