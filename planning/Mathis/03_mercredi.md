# Mathis — Mercredi 4 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## to study which quantity of the porous material gives the most optimal result ;

**Repère :** J3.3. **Rôle :** responsable.

**Contribution de Mathis.** On prépare les paramètres nécessaires à la comparaison de plusieurs quantités de poreux et, si les données existent, de plusieurs matériaux.

**Fichier à compléter :** `support/preprocessing.py`.

### Fichiers concernés

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Contexte

```text
Protection du support : les cellules protégées du programme principal sont en lecture seule. Garde aussi inchangées les fonctions initialement fournies de preprocessing.py, notamment _set_coefficients_of_pde, _set_rhs_of_pde, _set_geometry_of_domain et les fonctions du motif qu’elle appelle. Ajoute les fonctions du projet à côté ; seules ces fonctions ajoutées peuvent être complétées ou corrigées. Elles travaillent sur des tableaux indépendants et ne changent pas les valeurs du cas initial par effet de bord. Compare les fonctions fournies à la version jointe avant de rendre le fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Étudie la quantité nécessaire aux cartouches poreuses du panneau RER B avec les mêmes bandes et sources entre candidats comparables. La réduction de matière doit résulter des calculs. Les divisions par deux ou trois et la fraction de 40 % citées comme perspectives dans SOTA.md ne sont pas des résultats imposés. Compare les performances et la quantité à épaisseur et profondeur annoncées.

Documente la quantité des cartouches et la validité de chaque matériau pour le scénario retenu, en distinguant le budget absolu d’une fraction de nœuds.

Modifie uniquement support/preprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

Étends les contrôles de compute_material_response pour traiter successivement les matériaux documentés déjà retenus, sans changer sa signature. Vérifie la validité sur toute la grille fréquentielle et l’absence de réemploi d’un coefficient calculé à une autre fréquence. Conserve name, thickness_m, valid_frequency_hz et provenance. N’invente pas un matériau supplémentaire.

Ajoute si nécessaire une petite fonction de conversion du budget de longueur en volume à épaisseur et profondeur uniformes. Vérifie les valeurs réelles positives et les unités. Les longueurs pondérées viennent des faces du maillage et un pourcentage de nœuds ne remplace pas ce budget. Si l’épaisseur change entre matériaux, précise la longueur compatible avec le même volume et sa faisabilité. Donne dans la réponse les budgets proposés et les conditions d’une comparaison à même volume. Les simulations restent dans le pilote de Yann.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les quantités sont données en longueur et, lorsque pertinent, en volume. Chaque matériau possède ses propres paramètres et son domaine de validité.

**Passage de main.** Fournir à Antoine les budgets faisables, à Yann les paramètres de campagne et à Olympia les unités pour les courbes de quantité.
