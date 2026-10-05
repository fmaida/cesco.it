/*
 * cesco.it – interazioni del layout (nessuna dipendenza).
 */
(function () {
    "use strict";

    // Menu laterale a scomparsa (sotto i 992px)
    var toggle = document.querySelector(".menu-toggle");
    if (toggle) {
        var chiudi = function () {
            document.body.classList.remove("menu-open");
            toggle.setAttribute("aria-expanded", "false");
        };
        toggle.addEventListener("click", function () {
            var aperto = document.body.classList.toggle("menu-open");
            toggle.setAttribute("aria-expanded", aperto ? "true" : "false");
        });
        document.addEventListener("keydown", function (evento) {
            if (evento.key === "Escape" && document.body.classList.contains("menu-open")) {
                chiudi();
                toggle.focus();
            }
        });
    }

    var animazioniRidotte = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // Selettore del tema (chiaro / automatico / scuro); la logica che
    // applica il tema sta in head.html, qui ci sono solo i pulsanti
    var radice = document.documentElement;
    var pulsantiTema = document.querySelectorAll("[data-theme-choice]");
    var segnaTemaAttivo = function () {
        var preferenza = radice.getAttribute("data-theme-pref") || "auto";
        pulsantiTema.forEach(function (pulsante) {
            var attivo = pulsante.dataset.themeChoice === preferenza;
            pulsante.setAttribute("aria-pressed", attivo ? "true" : "false");
        });
    };
    pulsantiTema.forEach(function (pulsante) {
        pulsante.addEventListener("click", function () {
            if (typeof window.impostaTema !== "function") {
                return;
            }
            if (!animazioniRidotte) {
                radice.classList.add("cambio-tema");
                setTimeout(function () {
                    radice.classList.remove("cambio-tema");
                }, 400);
            }
            window.impostaTema(pulsante.dataset.themeChoice);
            segnaTemaAttivo();
        });
    });
    segnaTemaAttivo();

    // Nomi della promessa in homepage scritti "a macchina": scrive un nome
    // una lettera alla volta, lo lascia 3 secondi con il cursore che lampeggia,
    // lo cancella da destra a sinistra e passa al successivo; dopo l'ultimo
    // riparte dal primo.
    var SCRITTURA = 90;            // ms per ogni lettera scritta
    var CANCELLAZIONE = SCRITTURA / 2;  // ms per ogni lettera cancellata
    var PAUSA = 3000;              // ms a frase completa, con il cursore che lampeggia
    var ATTESA = 400;              // ms tra la cancellazione e la frase successiva

    document.querySelectorAll("[data-typewriter]").forEach(function (contenitore) {
        var ruoli = Array.prototype.map.call(contenitore.querySelectorAll(".sp-subtitle"), function (ruolo) {
            return Array.from(ruolo.textContent.trim());  // accenti ed emoji contano come una lettera
        });
        var testo = contenitore.querySelector(".sp-typed-text");
        var cursore = contenitore.querySelector(".sp-cursor");
        if (!ruoli.length || !testo || !cursore || animazioniRidotte) {
            return;  // resta il primo ruolo, fermo
        }
        contenitore.classList.add("is-typing");

        var indice = 0;

        var scrivi = function (lettere) {
            if (lettere < ruoli[indice].length) {
                testo.textContent = ruoli[indice].slice(0, lettere + 1).join("");
                setTimeout(function () { scrivi(lettere + 1); }, SCRITTURA);
                return;
            }
            cursore.classList.add("is-blinking");
            if (ruoli.length > 1) {
                setTimeout(function () {
                    cursore.classList.remove("is-blinking");
                    cancella(ruoli[indice].length);
                }, PAUSA);
            }
        };

        var cancella = function (lettere) {
            if (lettere > 0) {
                testo.textContent = ruoli[indice].slice(0, lettere - 1).join("");
                setTimeout(function () { cancella(lettere - 1); }, CANCELLAZIONE);
                return;
            }
            indice = (indice + 1) % ruoli.length;
            setTimeout(function () { scrivi(0); }, ATTESA);
        };

        scrivi(0);
    });

    // Filtri per tag (servizi, portfolio, laboratorio, blog): i pulsanti .filter
    // mostrano solo le voci con quel tag in data-groups
    document.querySelectorAll("[data-filtri]").forEach(function (contenitore) {
        var filtri = contenitore.querySelectorAll(".filter");
        var progetti = contenitore.querySelectorAll("[data-groups]");
        filtri.forEach(function (filtro) {
            filtro.addEventListener("click", function () {
                var gruppo = filtro.dataset.group;
                filtri.forEach(function (altro) {
                    var attivo = altro === filtro;
                    altro.classList.toggle("active", attivo);
                    altro.setAttribute("aria-pressed", attivo ? "true" : "false");
                });
                progetti.forEach(function (progetto) {
                    var tag = progetto.dataset.groups.split(" ");
                    progetto.hidden = gruppo !== "all" && tag.indexOf(gruppo) === -1;
                });
            });
        });
    });

    // Contatti: ?oggetto= nell'URL (pulsanti "Acquista" dei piani in Chi sono)
    // precompila il campo Oggetto
    var oggetto = document.getElementById("InputSubject");
    if (oggetto && !oggetto.value) {
        var precompilato = new URLSearchParams(window.location.search).get("oggetto");
        if (precompilato) oggetto.value = precompilato;
    }
})();
