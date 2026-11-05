# Présentation sobre et nouvelle comparaison

## Consignes en vigueur

- La nouvelle base est context/Slides_EI/presentation.tex fournie par l’équipe.
- Ne modifier que les blocs mur plan, influence de la géométrie, optimisation et quantité. Retirer les sous-titres des frames. Aucun schéma TikZ.
- Figures simples, une figure par slide. Paramètres indiqués dans le titre de chaque nouvelle figure.
- Après clarification, seules les quatre descentes des matériaux MELAMINE, LAINE_ROCHE, LAINE_VERRE et OUATE_POLYESTER au niveau 3 sont à calculer, sur 50–3500 Hz au pas 5 Hz et avec 100 itérations maximum. Ne pas lancer 64 optimisations.
- Géométries et quantité : niveaux 0, 1, 2 et 3. L’étude de quantité agrandit une portion centrale garnie à position fixée.

## Calcul en cours

- Code préparé dans /tmp/resonics_sobre/support, présentation dans /tmp/resonics_sobre/presentation.
- Programme /tmp/run_sobre_studies.py, session exec 23165, journal /tmp/sobre_studies.log.
- Quatre processus indépendants, un par matériau. Les matrices complètes du support sont utilisées, avec voisinages fixes préparés et factorisation commune au champ et à l’adjoint. Aucune classe ajoutée.
- Tests /tmp/sobre_system_checks.json : matrices identiques à celles de la version validée aux quatre niveaux à N128. Test /tmp/sobre_gradient_checks.json : gradient pondéré validé par différences finies, erreur relative environ 2,5e-9 sur petit cas.
- Toutes les références et quantités des quatre niveaux sont terminées. Les descentes au niveau 3 continuent vers 100 itérations maximum.
- Données dans /tmp/resonics_sobre/support/resultats, copies des PNG dans /tmp/resonics_sobre/presentation. Une copie des résultats déjà terminés est aussi dans le vrai dossier support/resultats.
- Le fichier /tmp/sobre_preservation.json vérifie que les 31 autres blocs de slides sont conservés, hormis le retrait demandé du sous-titre.

## Suite

1. Attendre SOBRE_STUDIES_DONE, puis vérifier les données, les volumes et les étapes acceptées.
2. Compiler et inspecter la nouvelle présentation avec ses vraies figures. Ne pas fabriquer de figure de remplacement.
3. Installer code et données. Toutes les nouvelles figures sont dans support/resultats et copiées directement dans presentation.
4. Supprimer les anciennes figures et les dossiers obsolètes, sans restaurer les archives déjà supprimées par l’utilisateur. Conserver les images requises par les slides inchangées.
5. Mettre à jour le guide, consigner le bilan, commits et push sur main/refactor.
6. Le rapport et les autres modifications locales sont préservés.

## Points hors périmètre des slides conservées

Le brouillon de l’équipe contient une référence eole absente de la bibliographie, une affirmation de régularité H2 sur le domaine irrégulier et des dimensions d’annexe différentes de la grille utilisée. Ces passages ne sont pas modifiés, conformément au périmètre demandé. Ils restent à relire avec l’équipe.

## État complémentaire

- Le calcul actif reste /tmp/run_sobre_studies.py, session 23165. Ne pas lancer /tmp/run_sobre_parallel.py : ce dernier était un essai d’orchestration inutilisé.
- Le contrôle du gradient au maillage N128 et au niveau 3 est dans /tmp/sobre_gradient_n128.json, erreur relative environ 2,6e-6.
- Au niveau 3, la contrainte conserve 410 points garnis sur 1024. Le contour mesure 8 m dans la discrétisation retenue.
- La présentation rassemble les quatre géométries dans une seule figure Matplotlib. Les autres nouvelles figures sont des courbes sur un seul graphique.
- Les compilations de vérification excluent les deux figures de descente encore en calcul. Ces PDF partiels ne doivent pas être livrés comme PDF final.
- Les débordements repérés pendant ces vérifications appartiennent aux blocs de slides conservés. Les nouvelles slides de murs et de quantité passent la vérification de mise en page.
