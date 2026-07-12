$(function () {

  "use strict";

  // Quando il form viene inviato
  $('#contact-form').on('submit', function (e) {
    e.preventDefault(); // evita submit tradizionale
    const $form = $(this);

    const url = "https://formspree.io/f/mrbbvgvq";

    $.ajax({
      type: "POST",
      url: url,
      data: $form.serialize(),
      headers: { "Accept": "application/json" },
      dataType: "json"
    })
    .done(function () {
      const alertBox = `
        <div class="alert alert-success alert-dismissable">
          <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
          Messaggio inviato correttamente.
        </div>`;
      $form.find('.messages').html(alertBox);
      $form[0].reset();
    })
    .fail(function (jqXHR) {
      let msg = 'Si è verificato un errore durante l\'invio. Riprova più tardi.';
      try {
        const resp = jqXHR.responseJSON;
        if (resp && resp.errors && resp.errors.length) {
          msg = resp.errors.map(e => e.message).join(' ');
        }
      } catch (_) {}
      const alertBox = `
        <div class="alert alert-danger alert-dismissable">
          <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
          ${msg}
        </div>`;
      $form.find('.messages').html(alertBox);
    });

    return false;
  });
});