import 'https://cdn.jsdelivr.net/gh/orestbida/cookieconsent@v3.0.0-rc.17/dist/cookieconsent.umd.js';

// Enable dark mode
document.documentElement.classList.add('cc--darkmode');

CookieConsent.run({
    guiOptions: {
        consentModal: {
            layout: "box",
            position: "bottom right",
            equalWeightButtons: true,
            flipButtons: false
        },
        preferencesModal: {
            layout: "box",
            position: "right",
            equalWeightButtons: true,
            flipButtons: false
        }
    },
    categories: {
        necessary: {
            readOnly: true
        },
        analytics: {}
    },
    language: {
        default: "it",
        autoDetect: "browser",
        translations: {
            en: {
                consentModal: {
                    title: "Cookie Usage Information",
                    description: "This website uses cookies to enhance user experience and ensure proper functionality of the site. By using my website, you consent to the use of cookies in accordance with my <a href='/privacy'>Privacy Policy</a>.",
                    acceptAllBtn: "Accept all",
                    acceptNecessaryBtn: "Reject all",
                    showPreferencesBtn: "Manage preferences",
                    footer: "<a href=\"/privacy\">Privacy Policy</a>\n<a href=\"/termini-condizioni\">Terms and conditions</a>"
                },
                preferencesModal: {
                    title: "Consent Preferences Center",
                    acceptAllBtn: "Accept all",
                    acceptNecessaryBtn: "Reject all",
                    savePreferencesBtn: "Save preferences",
                    closeIconLabel: "Close modal",
                    serviceCounterLabel: "Service|Services",
                    sections: [
                        {
                            title: "Cookie Usage",
                            description: "This website uses cookies to enhance user experience and ensure proper functionality of the site. By using my website, you consent to the use of cookies in accordance with my <a href='/privacy'>Privacy Policy</a>."
                        },
                        {
                            title: "Strictly Necessary Cookies <span class=\"pm__badge\">Always Enabled</span>",
                            description: "Strictly necessary cookies are essential for the proper functioning of the website and are indispensable for providing the services requested by the user. These cookies do not require explicit consent as they are crucial for navigation, access to secure areas, and the proper functioning of the site. Their collection is based on the necessity to fulfill a contract or comply with legal obligations.",
                            linkedCategory: "necessary"
                        },
                        {
                            title: "Analytics Cookies",
                            description: "Analytical cookies are used to collect information about the use of the website, allowing the site owner to analyze and understand how users interact with the content. These cookies help improve the site's performance and optimize the user experience. The collection of such data occurs in an aggregated and anonymous form, respecting user privacy. The use of analytical cookies is based on user consent, which can be managed through cookie settings.",
                            linkedCategory: "analytics"
                        },
                        {
                            title: "More information",
                            description: "For any query in relation to my policy on cookies and your choices, please <a class=\"cc__link\" href=\"#yourdomain.com\">contact me</a>."
                        }
                    ]
                }
            },
            it: {
                consentModal: {
                    title: "Informativa sull'Uso dei Cookie",
                    description: "Questo sito utilizza i cookie per migliorare l'esperienza dell'utente e garantire un corretto funzionamento del sito. Utilizzando il mio sito, acconsenti all'uso dei cookie in conformità con la mia <a href='/privacy'>Informativa sulla Privacy</a>",
                    acceptAllBtn: "Accetta tutto",
                    acceptNecessaryBtn: "Rifiuta tutto",
                    showPreferencesBtn: "Gestisci preferenze",
                    footer: "<a href=\"/privacy\">Informativa sulla privacy</a>\n<a href=\"/termini-condizioni\">Termini e condizioni</a>"
                },
                preferencesModal: {
                    title: "Centro preferenze per il consenso",
                    acceptAllBtn: "Accetta tutto",
                    acceptNecessaryBtn: "Rifiuta tutto",
                    savePreferencesBtn: "Salva le preferenze",
                    closeIconLabel: "Chiudi la finestra",
                    serviceCounterLabel: "Servizi",
                    sections: [
                        {
                            title: "Utilizzo dei Cookie",
                            description: "Questo sito utilizza i cookie per migliorare l'esperienza dell'utente e garantire un corretto funzionamento del sito. Utilizzando il mio sito, acconsenti all'uso dei cookie in conformità con la mia <a href='/privacy'>Informativa sulla Privacy</a>"
                        },
                        {
                            title: "Cookie Strettamente Necessari <span class=\"pm__badge\">Sempre Attivati</span>",
                            description: "I cookie strettamente necessari sono essenziali per il corretto funzionamento del sito web e sono indispensabili per fornire i servizi richiesti dall'utente. Questi cookie non richiedono il consenso esplicito in quanto sono fondamentali per la navigazione, l'accesso alle aree protette e il corretto funzionamento del sito. La loro raccolta è basata sulla necessità di adempiere a un contratto o per rispettare obblighi legali.",
                            linkedCategory: "necessary"
                        },
                        {
                            title: "Cookie Analitici",
                            description: "I cookie analitici vengono utilizzati per raccogliere informazioni sull'utilizzo del sito web, consentendo al gestore di analizzare e comprendere come gli utenti interagiscono con il contenuto. Questi cookie aiutano a migliorare le prestazioni del sito e a ottimizzare l'esperienza dell'utente. La raccolta di tali dati avviene in forma aggregata e anonima, rispettando la privacy degli utenti. L'uso di cookie analitici si basa sul consenso dell'utente, che può essere gestito attraverso le impostazioni dei cookie.",
                            linkedCategory: "analytics"
                        },
                        {
                            title: "Ulteriori informazioni",
                            description: "Per qualsiasi domanda in merito alle mie politiche sui cookies e sulla gestione delle tue scelte, ti prego di <a class=\"cc__link\" href=\"#yourdomain.com\">contattarmi</a>."
                        }
                    ]
                }
            }
        }
    }
});