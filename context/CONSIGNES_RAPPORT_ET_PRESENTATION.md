# Consigne actuelle — rapport après la soutenance

La demande du 15 novembre 2026 remplace les consignes de rédaction ci-dessous :
réécrire report/report.tex en suivant uniquement le récit et les figures de
context/SlidesVF/. Garder un rapport court, simple, sans nouveaux résultats,
nouvelles figures ou nouvelles slides. Le rapport reprend les formulations données par le groupe dans le récit de la soutenance et emploie le même ton pour le reste, en alternant « on », « nous » et des formulations impersonnelles pour éviter les répétitions, tout en gardant les tournures de la soutenance. Le choix présenté est l'ouate de polyester,
une paroi de niveau deux et une fraction garnie de 20 %. La réponse fréquentielle
est décrite par ses maxima d'énergie, sans les assimiler systématiquement à des
résonances propres. Les essais sur cinq maxima précèdent l'optimisation sur la bande
jusqu'à 2 000 Hz, au pas annoncé de 5 Hz.

Les programmes de context/EI_Antoine sont repris dans support sans changer leurs
algorithmes. Les seuls ajustements concernent les chemins de sortie et l'indication
du dossier source. Le programme actuel ne régénère pas par défaut toutes les figures
historiques de la soutenance, notamment la sélection finale niveau deux à 20 %.
L'ancien rapport et les anciens programmes sont conservés dans context/archives/,
ignoré par Git, pour d'éventuelles améliorations ultérieures.

---

## Anciennes consignes conservées pour mémoire

# Consignes pour la prochaine rédaction

La priorité actuelle est le code et la validation numérique. Le rapport et la présentation ne doivent pas être repris avant la fin de cette étape.

## Point de départ

- Le rapport réinitialisé par le groupe est dans `context/Rapport_EI/`.
- Les fonctions fournies initialement par les professeurs sont identifiables dans `context/fichiers_support/`.
- La progression du rapport et de la présentation doit suivre précisément les tirets de `context/Sujet-EI-EXT-2026.md`, dans l'ordre de la semaine.

## Contenu et style

- Présenter avant tout les courbes, les résultats réellement calculés, leurs comparaisons et leur interprétation physique.
- Expliquer simplement les algorithmes développés par le groupe : coefficient du matériau, source RER B, gradient projeté et optimisation sur la bande.
- Utiliser les notations et définitions déjà fournies dans l'énoncé et les documents de cours, sans les redéfinir longuement.
- Évoquer les fonctions du support initial lorsqu'on les utilise, sans détailler leur implémentation.
- Garder des explications courtes, naturelles et accessibles, à l'échelle d'un projet étudiant d'une semaine.
- Employer le libellé « Énergie J » dans les figures et le texte.
- Ne pas décrire les travaux de Magoulès et Rozanova-Pierrat dans l'état de l'art. Leurs documents peuvent rester dans la bibliographie comme références pédagogiques et scientifiques.
- Conserver mélamine, laine de verre et ouate polyester comme matériaux d'étude, sans désigner de produit gagnant à ce stade.

## Résultats à présenter après validation

- Distinguer la référence aux trois centres des gaussiennes de l'optimisation principale sur toute la bande 50–3 500 Hz.
- Comparer les mêmes conditions physiques, le même matériau et la même quantité pour le mur initial, le placement à trois fréquences et le placement sur la bande.
- Montrer les spectres avant/après sur une grille d'évaluation plus fine et discuter les pics qui diminuent, apparaissent ou se déplacent.
- Donner l'intégrale d'énergie, sa réduction relative, le maximum et sa fréquence, avec les paramètres effectifs des simulations.
- Distinguer le résultat continu et le résultat après binarisation, ainsi que les historiques obtenus sur des grilles différentes.
- Justifier l'échantillonnage fréquentiel par les essais de raffinement et préciser leurs limites. Aucun pas fixe ne garantit à lui seul la détection de toutes les résonances.
- Indiquer clairement les exécutions réalisées, leur résolution spatiale et les limites observées, sans inventer de résultat.
