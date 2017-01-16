$(document).ready(function() {
    // initialize bootstrap material
    $.material.init();

    $('.grid').masonry({
        itemSelector: '.grid-item'
    });

    var DOMAIN_URL = 'http://127.0.0.1:8000/';

    var HttpReq = function() {
        this.request = function(params) {
            $.ajax({
                url: params['url'],
                type: params['type'],
                data: params['data'],
                success: params['success'],
                error: params['error']
            });
        };
    }

    $('#id_date_of_birth').bootstrapMaterialDatePicker({format: 'D-M-YYYY', time: false});

    var options = {
        content: "Some text", // text of the snackbar
        timeout: 3000
    }
    $.snackbar(options);

    var CookieStore = {};
    CookieStore.all = {};
    CookieStore.start = function () {
        var cookies = document.cookie.split('; ');
        for (var i = 0; i < cookies.length; ++i) {
            var parts = cookies[i].split('=');
            CookieStore.all[parts[0]] = parts[1];
        }
    }
    CookieStore.start();
    CookieStore.get = function(key) {
        if (!Object.keys(CookieStore.all).length) {
            CookieStore.start();
        }
        return CookieStore.all[key] ? CookieStore.all[key] : undefined;
    };
    CookieStore.set = function (key, value) {
        document.cookie = key+"="+value;
    }
    CookieStore.delete = function (key) {
        var deleteConfirm = CookieStore.all[key] ? delete(CookieStore.all[key]) : false;
        document.cookie = key+"=";
        return document.cookie;
    }

    for (key in form) {
        if (form[key]) {
            $('input[name="' + key + '"]').parent().addClass('has-error');
        }
        else {
            $('input[name="' + key + '"]').parent().removeClass('has-error');
        }
    }

    var csrftoken = CookieStore.get('csrftoken');

});
