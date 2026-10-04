---
# Pagina "Chi sono": testo in markdown, blocchi grafici con gli shortcode di
# layouts/_shortcodes/ (ognuno ha in cima un commento con l'uso).
# I titoli dei blocchi sono titoli markdown: ### Parola <span>Evidenziata</span>
# Il contenuto degli shortcode si indenta (4 spazi per livello); i tag del
# livello più esterno restano invece a inizio riga.
#
# Blocchi oggi non usati, pronti da copiare nel testo:
#
#   ### Formazione            (oppure: ### Esperienze)
#   {{< timeline >}}
#       {{< tappa periodo="2016 – oggi" luogo="Azienda" titolo="Ruolo" >}}
#           Breve descrizione.
#       {{< /tappa >}}
#   {{< /timeline >}}
#
#   ### Conoscenze
#   {{< conoscenze "Marketing" "Social media" >}}
#
#   ### Certificati
#   {{< certificati >}}
#       {{< certificato titolo="Nome" id="XXXX" data="19 aprile 2018" logo="images/certificates/logo.png" >}}
#   {{< /certificati >}}
title: Chi Sono
description: "Francesco Maida, perito informatico e consulente digitale a Venezia: chi sono, competenze, piani tariffari ed esempi di lavori."
slug: chi-sono
layout: about
# Nei dati strutturati la pagina è un ProfilePage che descrive la persona
schema: ProfilePage
sitemap: {changefreq: monthly, priority: 0.8}
---

{{< titolo "Chi <span>Sono</span>" >}}

{{< scheda lato="destra" >}}
    {{< voce titolo="Residenza" >}}{{< dato "fiscal.locality" >}} ({{< dato "fiscal.region" >}}){{< /voce >}}
    {{< voce titolo="Email" >}}<{{< dato "support.email" >}}>{{< /voce >}}
    {{< voce titolo="Telefono" nota="Solo SMS e WhatsApp, niente chiamate" >}}{{< dato "support.phone" >}}{{< /voce >}}
    {{< voce titolo="Partita IVA" >}}{{< dato "fiscal.partita-iva" >}}{{< /voce >}}
{{< /scheda >}}

Mi chiamo Francesco Maida, vivo a Venezia e sono un perito informatico.

Puoi pensarmi come un'estetista per aziende: lavoro con cura e dedizione per rendere bella e desiderabile la tua impresa agli occhi delle persone, così che tu possa vendere di più. Non infiocchetto, né creo illusioni: faccio emergere il meglio della tua azienda, raccontandone con autenticità e passione la missione.

Scrivo software su misura fin da quando i dati si salvavano su floppy disk. Per l'Università di Venezia ho realizzato sistemi per le iscrizioni ai corsi, la prenotazione delle aule via internet e strumenti per gli studenti: test di verifica interattivi e un lettore per riascoltare le librerie audio a velocità rallentata.

Per Gabetti Franchising ho creato un sistema per gestire gli immobili in vendita e in affitto, con un sito statico e ricercabile: niente database, niente porte d'ingresso per chi vuole fare danni, solo pagine generate in anticipo e un piccolo motore di ricerca interno.

Oggi lavoro soprattutto con la ristorazione veneziana, che conosco da dentro perché è il mondo in cui sono cresciuto, quello dei miei genitori. Ho sviluppato un sistema di prenotazione dei tavoli che conferma il cliente via SMS ed email e permette di versare un acconto con Stripe o SumUp, per ridurre i no-show.

### Le Mie <span>Competenze</span>

{{< competenze >}}
    {{< competenza nome="Sviluppo web (HTML + CSS + Javascript)" valore="85" >}}
    {{< competenza nome="Python" valore="80" >}}
    {{< competenza nome="FileMaker" valore="70" >}}
{{< /competenze >}}

### Perché <span>Scegliere Me</span>

Perché dovresti scegliere me anziché un altro servizio per la tua azienda?

{{< risposta titolo="I colossi del web non fanno i tuoi interessi" immagine="locale-affollato.jpg" >}}
    **Le piattaforme gratuite non lavorano per il tuo business: lavorano per il loro.**
    Mostrano dati e suggerimenti che possono scoraggiare i tuoi clienti
    (*“locale molto affollato”*) e indirizzarli verso altri che potrebbero
    investire in pubblicità.
{{< /risposta >}}

{{< risposta titolo="Possono usarti per promuovere i tuoi concorrenti" immagine="consigliano-altri.jpg" >}}
    Anche quando un potenziale cliente visita il tuo profilo sulle loro piattaforme,
    **queste possono suggerire i tuoi diretti concorrenti.** È un meccanismo studiato
    per favorire chi investe in pubblicità presso di loro. Fai caso a questo: quando
    un’azienda paga per la visibilità, i concorrenti consigliati spariscono dalla sua scheda.
{{< /risposta >}}

{{< risposta titolo="Cosa faccio per te" immagine="venice-bio.jpg" >}}
    Io, invece, lavoro direttamente per te: analizzo i dati in modo trasparente,
    creo strategie personalizzate e ti aiuto ad attrarre clienti senza distorsioni,
    usando anche [Venice.bio](https://venice.bio), un potente sito di promozione che
    ti offro gratuitamente in alcuni pacchetti delle mie consulenze.\
    In questo modo trasformi i dati in un vantaggio competitivo, non in un rischio.
{{< /risposta >}}

### Piani <span>Tariffari</span>

Il mio costo per ora singola è di {{< dato "fares.standard" >}} € l’ora, tasse incluse.
Per chi desidera un impegno continuativo offro piani di abbonamento annuali a prezzi
scontati, con pacchetti di ore prepagate e benefit aggiuntivi. Tutti i piani qui
sotto esposti hanno durata annuale, comprendono le tasse e prevedono il pagamento
anticipato dell’intera somma, rinnovandosi automaticamente ogni anno salvo disdetta,
da richiedere almeno sette giorni prima della scadenza. Alcuni pacchetti includono
anche una pagina promozionale su Venice.bio. [Scopri di più su Venice.bio](https://venice.bio).

{{< piani >}}
    {{< piano titolo="Shampoo & Manicure alla tua Impresa" icona="images/icons/009-cleaning.svg" prezzo="199" >}}
        Prova il mio lavoro con un impegno di 2 ore e mezza. Lascia che io migliori
        i tuoi profili su Google, Instagram e TripAdvisor. In modo da farti arrivare
        più prenotazioni.

        - 2 ore e 1/2 di lavoro
        - ~~Profilo su Venice.bio~~
        - ~~Ore extra a {{< dato "fares.discounted" >}}€/h per 12 mesi~~
        - Supporto da lunedì a venerdì
        - Risposte in 48 ore lavorative
        - Supporto via email
        - ~~Supporto via WhatsApp~~
        - ~~Assistenza da remoto~~
    {{< /piano >}}

    {{< piano titolo="Trattamento Di Bellezza Aziendale" icona="images/icons/013-cut.svg" prezzo="399" >}}
        Con 6 ore posso aiutare la tua azienda a presentarsi rinnovata agli occhi dei
        tuoi clienti. Magari con dei profili social migliorati, e foto ed informazioni
        di qualità.

        - 6 ore di lavoro
        - ~~Profilo su Venice.bio~~
        - Ore extra a {{< dato "fares.discounted" >}}€/h per 12 mesi
        - Supporto da lunedì a venerdì
        - Risposte in 48 ore lavorative
        - Supporto via email
        - ~~Supporto via WhatsApp~~
        - ~~Assistenza da remoto~~
    {{< /piano >}}

    {{< piano titolo="Il Visagista Delle Dive Societarie" icona="images/icons/018-woman.svg" prezzo="699" consigliato="true" >}}
        Qui il lavoro si fa serio: 12 ore in cui insieme a te posso fare molto per dare
        un nuovo volto alla tua attività, e farla apprezzare come merita.

        - 12 ore di lavoro
        - Profilo su Venice.bio
        - 261€ di sconto (-27%)
        - Ore extra a {{< dato "fares.discounted" >}}€/h per 12 mesi
        - Supporto da lunedì a venerdì
        - Risposte in 48 ore lavorative
        - Supporto via email
        - Supporto via WhatsApp
        - Assistenza da remoto
    {{< /piano >}}
{{< /piani >}}

### Alcuni <span>Esempi</span>

Ecco alcuni esempi di cosa potrai ottenere assumendomi per 2,5 / 6 / 12 ore.
Ricorda che posso fare molto altro per te e per la tua azienda, per cui non
esitare a contattarmi se desideri richiedermi un preventivo per un lavoro specifico.

{{< timeline >}}
    {{< tappa periodo="2,5 ore" titolo="Ottimizzazione dei tuoi profili su Google e TripAdvisor" >}}
        Modifico le informazioni sui tuoi profili, aggiornando le informazioni sulla tua
        attività commerciale. Quando posso e se me le fornisci, inserisco le tue nuove
        fotografie promozionali per presentare al meglio la tua attività.
    {{< /tappa >}}

    {{< tappa periodo="2,5 ore" titolo="Promozione dell'attività su due social network per un mese" >}}
        Creerò un post la settimana per la vostra attività commerciale che posterò su due
        social network (solitamente Google My Business + Instagram, ma potete sceglierlo voi).

        **Extra che possono essere aggiunti:**

        - Due post la settimana anziché uno hanno un costo addizionale di 2,5 ore di lavoro.
        - Tre post la settimana anziché uno hanno un costo addizionale di 5 ore di lavoro.

        **Da sapere prima di richiedere il lavoro**\
        Dovrete provvedere voi a fornirmi fotografie di alta qualità del locale e dei vostri
        prodotti / servizi, che poi provvederò a riadattare nel formato richiesto dai social
        network. Nel caso in cui non abbiate a disposizione materiale fotografico, posso
        portare da voi un fotografo professionista ad un costo aggiuntivo.
    {{< /tappa >}}

    {{< tappa periodo="2,5 ore" titolo="Registrazione di un dominio web e di un email aziendale" >}}
        Registro per tuo conto un tuo dominio web aziendale del tipo *www\.azienda\.com* e gli
        associo uno o più indirizzi email aziendali, del tipo *mario\.rossi@azienda\.com*
    {{< /tappa >}}

    {{< tappa periodo="5 ore" titolo="Listino prezzi in due lingue con carta dei vini e bevande" >}}
        Creo per te un listino prezzi cartaceo in due lingue (generalmente Italiano + Inglese),
        comprensivo di una carta dei vini di massimo due pagine e di una carta delle bevande e
        caffetteria di massimo una pagina. La stampa su carta dei menù non è compresa nel prezzo.
    {{< /tappa >}}

    {{< tappa periodo="6 ore" titolo="Dominio + Landing page basilare" >}}
        Registro per te un dominio web, registro per te una o più email aziendali e creo una
        semplice landing page in una sola lingua (solitamente Italiano) che presenti i link ai
        tuoi profili social ed alle tue gallerie fotografiche esterne. Incluso nel prezzo un
        aggiornamento alla landing page da effettuare entro 12 mesi.
    {{< /tappa >}}

    {{< tappa periodo="7 ore" titolo="Listino prezzi in quattro lingue con carta dei vini e bevande" >}}
        Creo per te un listino prezzi cartaceo in quattro lingue (generalmente Italiano +
        Inglese + Francese + Tedesco), comprensivo di una carta dei vini di massimo 60 voci e
        di una carta delle bevande e caffetteria di massimo una pagina. Viene inoltre consegnata,
        per essere in regola con la legge, una tabella degli allergeni che andrà compilata a
        mano a cura del cuoco del ristorante.

        **Extra che possono essere aggiunti:**

        - Ogni lingua extra nel menù ha un costo addizionale di 1 ora di lavoro.
        - Dopo le prime 60 comprese, ogni 30 voci extra da inserire nella carta dei vini viene
          aggiunto un costo addizionale di 1 ora di lavoro.
        - La creazione dei listini da esterno ha un costo addizionale di 2 ore di lavoro.

        **Da sapere prima di richiedere il lavoro**\
        La stampa su carta dei menù non è compresa nel prezzo.
    {{< /tappa >}}

    {{< tappa periodo="12 ore" titolo="Dominio + Email professionale + Landing page in due lingue" >}}
        Registro per te un dominio web, registro per te una casella email aziendale di livello
        professionale e creo una landing page di media lunghezza in due lingue (solitamente
        Italiano + Inglese) che presenti la tua azienda, mostri una breve galleria fotografica
        sui tuoi prodotti e servizi (massimo 16 fotografie di prodotti e servizi) e una galleria
        fotografica che presenti il tuo lavoro (massimo 16 fotografie). Incluso nel prezzo un
        aggiornamento alla landing page da effettuare entro 12 mesi.

        **Da sapere prima di richiedere il lavoro**\
        Dovrai provvedere tu a fornirmi fotografie di alta qualità del locale e dei tuoi
        prodotti / servizi, che poi provvederò a riadattare nel formato richiesto per la
        pubblicazione sul tuo sito. Nel caso in cui tu non abbia a disposizione materiale
        fotografico, posso portare da te un fotografo professionista ad un costo aggiuntivo.
    {{< /tappa >}}
{{< /timeline >}}

<p class="text-center"><small>Gli esempi sono indicativi. Il servizio può essere personalizzato sulle tue esigenze.</small></p>

{{< pulsante pagina="/contact" >}}Richiedi Un Preventivo Gratuito{{< /pulsante >}}

