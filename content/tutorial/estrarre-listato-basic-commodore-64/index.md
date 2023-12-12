---
title: Estrarre un listato BASIC da un Commodore 64
date: 2023-10-08
tags:
    - retrogaming
    - c64
summary:
    Come estrarre un listato in BASIC per Commodore 64 da un immagine disco .D64
---

Non è di certo qualcosa per tutti i giorni, ma se mai vi servisse 
estrarre un listato BASIC del Commodore 64 da un immagine disco .D64:  
  
Installate l'emulatore <https://vice-emu.sourceforge.io> con i suoi tool da riga di comando `c1541` e `petcat`.

**P.S.:** Se usate MacOS, normalmente potete trovare questi tool all'interno della cartella `/Applications/vice-x86-64-gtk3-<versione>/bin/`

Quando siete pronti, da terminale digitate questo:


## Per elencare il contenuto su disco

```sh
c1541 -attach <input.d64> -list
```

Questo è un esempio di risultato che otterrete:

```
/Users/cesco/Downloads/disco.d64
0 "disco 64        " k6 2a
135  "file 1"           prg
8    "file 2"           prg
521 blocks free.
```

## Per estrarre il file in formato .PRG

```sh
c1541 -attach <input.d64> -read "<nome file dall'elenco>"
```

## Per convertire il file .PRG in testo

```sh
petcat -2 -o <output.txt> -- <input.prg>
```
