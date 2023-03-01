# Taxon builder
https://app.diagrams.net/#G1DlnbuonQCZw0q1Sc8tzbFq5Sa0SL-HmF
## Regex IAWA extraction

- FAMILLE : 

```REGEX
[A-Z]*^[A-Za-z]*
```

- GENRE + ESPECE: 

```REGEX
[A-Z][a-z]+ [a-z]+
```

La partie gauche de la regex est le genre, la partie droite de la regex est l'espèce

- AUTHOR:

```regex
\([A-Z\.]*\) [A-Z\.]+
```

- NOM COMMUN:

```
\([A-Z\.\s\,]*\)(?! [A-Z]*)
```

