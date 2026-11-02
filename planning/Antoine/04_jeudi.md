# Antoine — Jeudi, 5 novembre 2026

Objectif : s'assurer que le produit choisi correspond à une optimisation correctement arrêtée.

**Fichier partagé.** On récupère la dernière version transmise par le membre précédent, puis on renvoie le fichier entier après vérification. Une seule personne applique ses modifications à la fois. Chaque tâche ci-dessous concerne un seul fichier de `support/` et ne crée aucun module Python.

## Tâche 1 — Robustesse et motifs d'arrêt

**Fichier concerné :** `support/demo_control_polycopie2024.py`, pour la projection, la descente et leurs contrôles. Les données des campagnes sont examinées telles qu'elles existent.

**Ce qu'on fait.** On distingue une convergence locale d'un arrêt faute de pas ou d'itérations. On vérifie la cohérence du coût final, du budget et du meilleur candidat de plusieurs départs. On indique à Yann les calculs à reprendre avant de figer les résultats.

**Fichiers à joindre :**

- `support/demo_control_polycopie2024.py`, dernière version complète
- `support/_env.py`, `support/preprocessing.py`, `support/processing.py` et `support/postprocessing.py`, versions actuelles en lecture seule pour les imports et les contrôles
- `context/Sujet-EI-EXT-2026.md`
- Les historiques et les résumés réels des essais, joints ou collés dans le message


**Prompt à copier :**

```text
Relis les fonctions project_density et your_optimization_procedure ainsi que leurs contrôles dans demo_control_polycopie2024.py. Ne modifie aucun autre fichier et ne crée pas de fichier.

À partir des historiques fournis, vérifie les bornes, l'erreur absolue de budget, la condition d'acceptation avec le déplacement projeté et le motif d'arrêt. Vérifie que les essais rejetés ne remplacent jamais le point courant et qu'il n'y a pas de ligne fictive dans l'historique. Le coût, le gradient et la densité finaux doivent se rapporter à la même évaluation.

Examine plusieurs départs au même budget. Identifie le meilleur candidat admissible réellement évalué, en donnant son motif d'arrêt et son coût. Une faible baisse entre deux itérations ne suffit pas à conclure à la stationnarité. Le gradient projeté est contrôlé avec une échelle de coût annoncée et fixe. Aucune recherche locale ne prouve l'optimalité globale du produit.

Reprends les petits contrôles d'algorithme, dont les cas de budget extrême et de retour arrière. Si tu trouves une erreur dans les fonctions d'Antoine, renvoie le fichier complet corrigé en préservant les autres fonctions. Sinon, confirme qu'aucune modification n'est nécessaire. Donne les contrôles effectivement exécutés ou ceux qui restent à faire, sans inventer de résultats.

Prépare une explication courte du choix du candidat et de ses limites de calcul pour le groupe. Les campagnes au maillage affiné sont relancées par Yann et comparées par Olympia, elles ne sont pas recodées dans une autre fonction ici.
```

**Vérification et transmission.** On transmet à Yann et Olympia les essais à conserver et ceux à prolonger. Toute correction de la projection ou de la recherche de pas impose de réévaluer les candidats concernés.
