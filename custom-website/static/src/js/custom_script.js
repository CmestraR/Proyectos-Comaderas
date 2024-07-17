odoo.define('website.user_custom_code', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var Dialog = require('web.Dialog');
    
    function levenshtein(a, b) {
        var tmp;
        if (a.length === 0) { return b.length; }
        if (b.length === 0) { return a.length; }
        if (a.length > b.length) { tmp = a; a = b; b = tmp; }

        var i, j, res, alen = a.length, blen = b.length, row = Array(alen + 1);
        for (i = 0; i <= alen; i++) { row[i] = i; }

        for (i = 1; i <= blen; i++) {
            res = i;
            for (j = 1; j <= alen; j++) {
                tmp = row[j - 1];
                row[j - 1] = res;
                res = b[i - 1] === a[j - 1] ? tmp : Math.min(tmp + 1, Math.min(res + 1, row[j] + 1));
            }
        }
        return res;
    }

    publicWidget.registry.CityZipUpdater = publicWidget.Widget.extend({
        selector: '#wrapwrap',
    
        events: {
            'change input[name="city"]': '_onCityChange',
        },
    
        _onCityChange: function (event) {
            var self = this;
            var city = $(event.target).val().trim().toLowerCase(); // Convertir a minúsculas para comparación case-insensitive
            var MAX_DISTANCE = 2; // Distancia máxima de Levenshtein permitida

            console.log('City input changed:', city);

            if (city === '') {
                // Si el campo de ciudad está vacío, limpiar los campos de código postal, departamento y país
                console.log('City input is empty');
                $('input[name="zip"]').val('').prop('readonly', true);
                $('select[name="state_id"]').val('').prop('disabled', true);
                $('select[name="country_id"]').val('').prop('disabled', true);
                return;
            }

            if (city.length === 1) {
                $('input[name="zip"]').val('No Disponible').prop('readonly', true);
                var errorMessage = 'Por favor, escribe el nombre completo de la ciudad de destino';
                var dialog = new Dialog(self, {
                    title: 'Entrada No Válida',
                    size: 'medium',
                    $content: $('<div>').text(errorMessage),
                    buttons: [{
                        text: 'Aceptar',
                        classes: 'btn-primary',
                        click: function () {
                            dialog.close();
                        }
                    }]
                });
                dialog.open();
                return;
            }
    
            // Llamada RPC para obtener el código postal y el departamento basado en la ciudad
            rpc.query({
                model: 'res.city',
                method: 'search_read',
                args: [[['name', 'ilike', city[0] + '%']], ['name', 'zipcode', 'state_id']], // Usamos 'ilike' para búsqueda case-insensitive y obtener ciudades que comiencen con la misma letra
            }).then(function (records) {
                console.log('Records fetched:', records);
                if (records.length > 0) {
                    // Buscar coincidencia exacta
                    var matchingRecord = records.find(record => record.name.toLowerCase() === city);
                    var zip = matchingRecord ? matchingRecord.zipcode : null;
                    var state = matchingRecord ? matchingRecord.state_id[0] : null; // Obtenemos el ID del estado

                    console.log('Matching record:', matchingRecord);

                    // Si no hay coincidencia exacta, buscar la coincidencia más cercana
                    if (!matchingRecord) {
                        var minDistance = Infinity;
                        var closestCity = '';
                        records.forEach(function(record) {
                            var distance = levenshtein(city, record.name.toLowerCase());
                            if (distance < minDistance) {
                                minDistance = distance;
                                closestCity = record.name;
                                zip = record.zipcode;
                                state = record.state_id[0]; // Obtenemos el ID del estado
                            }
                        });

                        console.log('Closest city:', closestCity, 'with distance:', minDistance);

                        if (minDistance > MAX_DISTANCE) { // Si la distancia es mayor a 2, considerar que no hay coincidencia válida
                            closestCity = '';
                            zip = null;
                            state = null;
                        }
                    }

                    if (zip === null) {
                        // Mostrar mensaje de error si no se encontraron coincidencias válidas
                        $('input[name="zip"]').val('No Disponible').prop('readonly', true);
                        var errorMessage = 'No tenemos envíos disponibles para la ciudad de ' + city + '. Revisa que esté bien escrito o si crees que esto es un error, ponte en contacto con nosotros.';
                        var dialog = new Dialog(self, {
                            title: 'Envios No Disponibles Para Esta Ciudad',
                            size: 'medium',
                            $content: $('<div>').text(errorMessage),
                            buttons: [{
                                text: 'Contáctanos',
                                classes: 'btn-primary',
                                click: function () {
                                    window.open('https://api.whatsapp.com/send?phone=573185202411', '_blank');
                                    dialog.close();
                                }
                            }]
                        });
                        dialog.open();
                        $('select[name="state_id"]').val('').prop('disabled', true);
                        $('select[name="country_id"]').val('').prop('disabled', true);
                    } else {
                        console.log('Zip code found:', zip);
                        $('input[name="zip"]').val(zip).prop('readonly', true);
                        $('select[name="state_id"]').val(state).prop('disabled', true); // Asignar el estado y hacer que no sea editable
                        $('select[name="country_id"]').val(49).prop('disabled', true); // Establecer el país a Colombia (ID 49) y hacerlo no editable

                        // Obtener y establecer la responsabilidad tributaria
                        self._setPersonType();
                    }
                } else {
                    // Mostrar mensaje de error si no se encontraron registros
                    $('input[name="zip"]').val('No Disponible').prop('readonly', true);
                    var errorMessage = 'No se encontró la ciudad: ' + city + '. Revisa que esté bien escrito o ponte en contacto con nosotros.';
                    var dialog = new Dialog(self, {
                        title: 'Ciudad No Encontrada',
                        size: 'medium',
                        $content: $('<div>').text(errorMessage),
                        buttons: [{
                            text: 'Ver todos los códigos postales',
                            classes: 'btn-primary',
                            click: function () {
                                window.location.href = 'https://comaderas-tests-2205-13793766.dev.odoo.com/codigos-postales';
                            }
                        }]
                    });
                    dialog.open();
                    $('select[name="state_id"]').val('').prop('disabled', true);
                    $('select[name="country_id"]').val('').prop('disabled', true);
                }
            }).catch(function (error) {
                console.error('Error fetching city data:', error);
    
                // Verificar si el error es debido a sesión expirada
                if (error.message && error.message.code === 100 && error.message.message === 'Odoo Session Expired') {
                    // Manejar la sesión expirada aquí, por ejemplo, redirigiendo a la página de inicio de sesión de Odoo
                    alert('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
                    window.location.href = '/web/login'; // Redirigir a la página de inicio de sesión de Odoo
                } else {
                    // Manejar otros errores de manera adecuada
                    $('input[name="zip"]').val('').prop('readonly', true); // Limpia el campo en caso de error
                    $('select[name="state_id"]').val('').prop('disabled', true);
                    $('select[name="country_id"]').val('').prop('disabled', true);
                }
            });
        },

        _setPersonType: function () {
            console.log('_setPersonType called');
            // Lógica para establecer la responsabilidad tributaria
            // Implementa tu lógica aquí
        },
    });
});
