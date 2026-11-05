# État du nettoyage et des calculs

- Version de départ : refactor/main 6c24fdd. Les modifications locales des documents et les références dans context sont préservées.
- Code de travail sans classe dans /tmp/resonics_antoine_clean/support.
- Nouvelle présentation basée sur le travail du groupe dans /tmp/resonics_antoine_clean/presentation/presentation.tex.
- Matrices complètes du support, signe plus Robin, adjoint discret et gradient contrôlés. Tests indépendants dans /tmp/antoine_clean_validation.json et /tmp/clean_modes_validation.json.
- Calcul N128 en cours : /tmp/run_clean_production.py, journal /tmp/clean_production.log, résultats /tmp/resonics_antoine_clean/support/resultats_antoine. Budget réellement demandé : dix itérations par procédure.
- Matériaux, quantités et gradient N128 en cours séparément : /tmp/run_clean_auxiliary.py et /tmp/clean_auxiliary.log.
- À terminer : réunir les résultats auxiliaires et principaux, régénérer les figures, compiler et inspecter la présentation réelle, appliquer /tmp/nettoyage_figures.json, archiver les anciennes données brutes, puis commits/push refactor/main.
- La nouvelle présentation ne doit utiliser aucune ancienne figure des études supprimées. Ne pas inventer de résultats ni attribuer au nouveau code les anciens résultats produits par l'autre solveur.
