#!/bin/bash

if [ -f /home/guacamole/tomcat/webapps/guacamole/templates.js ]; then
  cat <<EOF >> /home/guacamole/tomcat/webapps/guacamole/templates.js
  \$(window).on('load', function() {
    function getHashParam(param) {
      var hash = window.location.hash.substr(1);
      var hashParams = new URLSearchParams(hash.split('?')[1]);
      return hashParams.get(param);
    }

    setTimeout(function() {
      var quickconnectValue = getHashParam('quickconnect');
      if (quickconnectValue) {
        var \$field = \$('.quickconnect-field');
        \$field.val(quickconnectValue);
        \$field.trigger('input');
        \$field.trigger('change');
        \$('.quickconnect-button').click();
      }
    }, 500);
  });
EOF
fi

