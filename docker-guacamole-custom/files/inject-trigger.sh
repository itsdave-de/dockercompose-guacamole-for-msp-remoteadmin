#!/bin/bash

if [ -f /home/guacamole/tomcat/webapps/guacamole/templates.js ]; then
  cat <<'EOF' >> /home/guacamole/tomcat/webapps/guacamole/templates.js
$(window).on('load', function() {
  function getHashParam(param) {
    var hash = window.location.hash.substr(1);
    var hashParams = new URLSearchParams(hash.split('?')[1]);
    return hashParams.get(param);
  }

  setTimeout(function() {
    var quickconnectValue = getHashParam('quickconnect');
    if (quickconnectValue) {
      // Extração dos componentes da URI sem decodificação completa
      var baseUri = quickconnectValue.split('?')[0];
      var queryParams = quickconnectValue.split('?')[1];

      // Manuseio manual dos parâmetros devido a caracteres especiais
      var params = queryParams.split('&');
      var newParams = [];
      var password = '';

      for (var i = 0; i < params.length; i++) {
        var param = params[i];
        var [key, value] = param.split('=');

        if (key === 'password') {
          password = param.substring(param.indexOf('=') + 1);
          // Trata o restante da string como parte do password
          for (var j = i + 1; j < params.length; j++) {
            password += '&' + params[j];
          }
          break; // exit loop after password is captured
        } else {
          newParams.push(param);
        }
      }

      // Codificar novamente apenas o campo password
      if (password) {
        var encodedPassword = encodeURIComponent(password);
        newParams.push(`password=${encodedPassword}`);
      }

      // Construir a nova URI com o password codificado
      var formattedValue = `${baseUri}?${newParams.join('&')}`;

      // Preencher o campo do formulário e disparar eventos
      var $field = $('.quickconnect-field');
      $field.val(formattedValue);
      $field.trigger('input');
      $field.trigger('change');
      $('.quickconnect-button').click();
    }
  }, 500);
});
EOF
fi

