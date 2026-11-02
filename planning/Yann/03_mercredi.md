# Yann — Mercredi 4 novembre

**But du jour.** Lancer les comparaisons multiréquences et de quantité avec la même chaîne de calcul, puis fournir les résultats pour l'analyse sur toute la bande.

**Passage de main.** Prendre la démonstration après l'ajout multiréquence de Joachim et les contrôles de budget d'Antoine. Les fonctions de matériau et de tracé sont celles publiées par Mathis et Olympia. Les paramètres déjà validés restent identiques entre les expériences comparables.

## Tâche 1 — Piloter les expériences de bande et de quantité

**Fichier à modifier :** [support/demo_control_polycopie2024.py](../../support/demo_control_polycopie2024.py).

**Ce qui est fait.** On lance une optimisation avec une seule distribution de matériau commune à plusieurs fréquences. On compare ensuite plusieurs budgets absolus et on recalcule les réponses sur des fréquences qui n'ont pas servi à optimiser.

**Fichiers à joindre avec le prompt :**

- `support/demo_control_polycopie2024.py`, dernière version après Joachim puis Antoine, à modifier.
- Les quatre autres fichiers actuels de `support/`, en lecture seule.
- `context/Sujet-EI-EXT-2026.md` et les paramètres validés du groupe.

**Prompt à copier :**

```text
Modifie uniquement demo_control_polycopie2024.py joint. Conserve les fonctions des autres membres, les cellules imposées et toutes les interfaces déjà validées. Aucun nouveau fichier Python n'est créé.

Ajoute les appels de campagne suivants dans les zones modifiables :
- Compare les niveaux géométriques à quantité absorbante absolue identique. La géométrie reste fixe pendant chaque optimisation. Garde les références entièrement recouvertes, initiales à budget limité et optimisées à une fréquence.
- Lance evaluate_band de Joachim avec une même densité chi pour toutes les fréquences de conception. Fixe les poids de somme un et les éventuelles normalisations avant la descente. Ces références restent communes aux candidats comparés. Appelle l'optimiseur existant avec ce callback. Ne moyenne pas des densités optimisées séparément. evaluate_band renvoie u=None ; pour une carte, réévalue la densité finale à une fréquence annoncée avec evaluate_density.
- Compare quelques budgets communs à toutes les formes, faisables et annoncés en longueur, puis volume si épaisseur et profondeur sont fixées. Réutilise la projection d'Antoine lorsque l'initialisation vient d'un autre budget. N'interprète pas une fraction de nœuds comme une longueur identique entre profils.
- Recalcule pour chaque distribution finale une bande de validation incluant des fréquences intermédiaires et des voisinages de pics. Si des fréquences ont été ajoutées pour préciser un pic, réévalue les poids de quadrature du coût de bande ; leur simple accumulation ne doit pas changer arbitrairement l'importance du voisinage.
- Prépare les mêmes records que mardi, avec state='multi' pour l'optimisation commune, et conserve paramètres, budgets, résidus et causes d'arrêt. Appelle les tracés de postprocessing disponibles et transmets les tableaux bruts à Olympia.

Ajoute aussi un petit scénario distinct de contrôle ouvert/réfléchissant pour Joachim. La source supérieure reste inchangée. Pour le scénario ouvert, transforme seulement une paroi latérale en Robin de Sommerfeld avec alpha_code=+1j*k. Sépare son masque de celui du matériau de conception, conserve le coin source selon une règle annoncée, et exclue cette ouverture de get_design_faces et du budget. Le scénario du tunnel réfléchissant reste celui des comparaisons de produit. Ne suppose pas que l'énergie ouverte est inférieure à chaque fréquence.

Contrôle les dimensions, la passivité validée, les résidus et la faisabilité de chaque expérience avant d'afficher un résultat. Les données manquantes restent explicitement signalées. Les commentaires expliquent les étapes par des phrases françaises. Donne les appels à exécuter et un résumé des résultats réellement calculés.
```

**Résultat attendu.** Une comparaison à source et paramètres identiques sur toute la bande, avec budgets mesurés, fréquences de conception identifiées et validation indépendante. Joachim reçoit aussi les deux séries ouverte/réfléchissante pour son analyse.
