$(function () {

    "use strict";

    // init the validator
    // validator files are included in the download package
    // otherwise download from http://1000hz.github.io/bootstrap-validator

    $('#contact-form').validator();


    // when the form is submitted
    $('#contact-form').on('submit', function (e) {

        // if the validator does not prevent form submit
        if (!e.isDefaultPrevented()) {
            var url = "https://formspree.io/f/mrbbvgvq";

            // POST values in the background the the script URL
            $.ajax({
                type: "POST",
                url: url,
                data: $(this).serialize(),
                success: function (data)
                {
                    // data = JSON object that contact.php returns

                    // we recieve the type of the message: success x danger and apply it to the 
                    // var messageAlert = 'alert-' + data.type;
                    // var messageText = data.message;

                    // let's compose Bootstrap alert box HTML
                    // var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';
                    
                    // If we have messageAlert and messageText
                    //if (messageAlert && messageText) {
                        // inject the alert to .messages div in our form
                    //    $('#contact-form').find('.messages').html(alertBox);
                        // empty the form
                    //    $('#contact-form')[0].reset();
                    //}
                //}
                
                $.ajax({
                    type: "POST",
                    url: url,
                    data: $form.serialize(),
                    headers: { "Accept": "application/json" },
                    dataType: "json"
                })
                .done(function (data, textStatus, jqXHR) {
                    var alertBox = '<div class="alert alert-success alert-dismissable">' +
                        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
                        'Messaggio inviato correttamente.' +
                        '</div>';
                    $form.find('.messages').html(alertBox);
                    $form[0].reset();
                })
                .fail(function (jqXHR) {
                    // Prova a estrarre eventuali errori da Formspree
                    var msg = 'Si è verificato un errore durante l\'invio. Riprova più tardi.';
                    try {
                        var resp = jqXHR.responseJSON;
                        if (resp && resp.errors && resp.errors.length) {
                            msg = resp.errors.map(function (e) { return e.message; }).join(' ');
                        }
                    } catch (_) {}
                    var alertBox = '<div class="alert alert-danger alert-dismissable">' +
                        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
                        msg +
                        '</div>';
                    $form.find('.messages').html(alertBox);
                });

                return false;
            }
        });
    });