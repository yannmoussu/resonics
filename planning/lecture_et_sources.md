# Documents utiles

Les fiches quotidiennes indiquent les pièces précises à joindre. Les documents principaux sont les suivants.

| Document | Utilité |
|---|---|
| [État de l’art RER B — Mathis et Olympia](../SOTA.md) | Cadrage de l’application, plages exploratoires, matériaux et concept de panneau ; les valeurs et perspectives chiffrées sont à documenter |
| [Énoncé EI](../context/Sujet-EI-EXT-2026.md) | Questions, cinq journées, comparaisons et soutenance |
| [Optimisation paramétrique — Allaire](../context/GAllaire-OptimParam.pdf) | Gradient projeté, recherche du pas et adjoint ; pages PDF 13–20 et 25–29 |
| [Dirichlet non homogène](../context/Dirichlet_Nonhomogene.pdf) | Source imposée et emploi du champ total dans le gradient |
| [Mur antibruit — Filoche](../context/Mur-antibruit-Filoche.pdf) | Formes, absorption et matériaux ; les coefficients réels d'absorption ne déterminent pas une impédance complexe |
| [Programmes fournis](../support/) | Géométrie, différences finies, conditions aux limites et figures |
| [Projets précédents](../context/acoustic-pollution-fem/) | Méthodes de vérification et templates LaTeX |

Les pages mentionnées sont les pages des fichiers PDF. Les paramètres de l'ancien devoir, notamment sa contrainte d'aire, ne deviennent pas des contraintes de cette EI. Les profils fournis sont repris selon leur forme effective, qui utilise un motif orthogonal.

Le critère intérieur mesure la pression intégrée au carré. Le coefficient de matériau et son signe doivent être validés avant les campagnes physiques. Les petits cas synthétiques des fiches servent seulement à vérifier les algorithmes.

Le cas retenu est le RER B. Les bandes proposées dans SOTA.md servent à préparer les choix de J1.3, puis les calculs emploient les paramètres validés. Le profil réellement généré par le support reste un motif orthogonal. La formulation du gradient et les conventions de Robin sont vérifiées sur les équations assemblées, en s’appuyant sur les documents de méthode ci-dessus.
