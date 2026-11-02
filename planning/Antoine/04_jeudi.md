# Antoine — Jeudi 5 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution d’Antoine. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

## To continue the analysis of the performances ;

**Repère :** J4.1. **Rôle :** contributeur.

**Contribution d’Antoine.** On vérifie les motifs d’arrêt, les budgets et la robustesse des candidats selon leurs points de départ.

**Fichier à modifier :** `support/demo_control_polycopie2024.py` uniquement.

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py, dernière version complète, seule cible à modifier
- support/_env.py, support/preprocessing.py, support/processing.py et support/postprocessing.py, versions actuelles en lecture seule
- Les historiques, budgets et résumés réels des campagnes, avec leurs initialisations
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
Relis les fonctions project_density et your_optimization_procedure ainsi que leurs contrôles dans demo_control_polycopie2024.py. Ne modifie aucun autre fichier et ne crée pas de fichier.

À partir des historiques fournis, vérifie les bornes, l'erreur absolue de budget, la condition d'acceptation avec le déplacement projeté et le motif d'arrêt. Vérifie que les essais rejetés ne remplacent jamais le point courant et qu'il n'y a pas de ligne fictive dans l'historique. Le coût, le gradient et la densité finaux doivent se rapporter à la même évaluation.

Examine plusieurs départs au même budget. Identifie le meilleur candidat admissible réellement évalué, en donnant son motif d'arrêt et son coût. Une faible baisse entre deux itérations ne suffit pas à conclure à la stationnarité. Le gradient projeté est contrôlé avec une échelle de coût annoncée et fixe. Aucune recherche locale ne prouve l'optimalité globale du produit.

Reprends les petits contrôles d'algorithme, dont les cas de budget extrême et de retour arrière. Si tu trouves une erreur dans les fonctions d'Antoine, renvoie le fichier complet corrigé en préservant les autres fonctions. Sinon, confirme qu'aucune modification n'est nécessaire. Donne les contrôles effectivement exécutés ou ceux qui restent à faire, sans inventer de résultats.

Prépare une explication courte du choix du candidat et de ses limites de calcul pour le groupe. Les campagnes au maillage affiné sont relancées par Yann et comparées par Olympia, elles ne sont pas recodées dans une autre fonction ici.
```

**Contrôle et passage de main.** On transmet les essais à conserver ou à prolonger à Yann et Olympia. Une correction de projection ou de recherche du pas impose de réévaluer les candidats concernés.

## To conclude which product to produce/develop.

**Repère :** J4.2. **Rôle :** contributeur.

**Contribution d’Antoine.** On vérifie que le candidat retenu est admissible et que son état de convergence est annoncé correctement.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers à joindre :**

- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- Le tableau final des candidats et les historiques des essais retenus
- context/Sujet-EI-EXT-2026.md

**Prompt à copier :**

```text
À partir du tableau et des historiques réels, identifie les candidats admissibles et leurs motifs d’arrêt. Vérifie que coût, densité, gradient projeté et budget se rapportent à la même évaluation finale. Compare les points de départ au même budget et distingue une stationnarité locale d’une limite d’itérations ou de pas.

Propose une courte conclusion pour le choix collectif du produit, en indiquant ce que l’algorithme permet d’affirmer. Le meilleur candidat évalué dans la famille testée n’est pas une preuve d’optimum global. Si le résultat jugé meilleur n’est pas suffisamment contrôlé, indique le calcul précis à reprendre avec Yann avant de le retenir.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On valide avec Olympia la façon de présenter la convergence et avec Yann les éventuels essais à relancer.
