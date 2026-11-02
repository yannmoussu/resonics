# Mathis — Mardi 3 novembre

**Organisation.** On utilise les versions complètes et à jour. Chaque contribution de code porte sur un seul fichier de `support/`, les dépendances restent en lecture seule et aucun nouveau module Python n’est créé. Les intitulés ci-dessous reprennent exactement les tirets de l’énoncé.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## Study the energy on the chosen plage of frequencies for a fully absorbent wall of the plane shape and to define the local maxima ;

**Repère :** J2.1. **Rôle :** contributeur.

**Contribution de Mathis.** On valide les coefficients du matériau pour la référence plane calculée par Yann et tracée par Olympia.

**Fichier à compléter :** `support/preprocessing.py`.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py` — cible à modifier.
- `support/processing.py` — lecture seule.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Calcule d’abord la référence du mur plan entièrement recouvert sur la plage de roulement proposée de 250 à 2 000 Hz après validation de ses paramètres. Les pics recherchés sont les pics de réponse du modèle ; ils ne constituent pas un spectre mesuré du RER B. Les cas complémentaires de traction ou de crissement sont identifiés séparément et utilisent leurs propres bandes validées.

Vérifie la passivité et la validité fréquentielle de la loi complexe sur chaque bande RER B effectivement calculée ; un coefficient pris à une seule fréquence ne représente pas toute la bande.

Modifie uniquement support/preprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

Ajoute au même module un contrôle d’impédance à incidence normale en conservant compute_material_response. Avec exp(-i*omega_phys*t), Z0=rho_air*c et R=(Z_s-Z0)/(Z_s+Z0), l’absorption plane vaut 1-abs(R)**2. Pour une surface passive, Re(Z_s)>=0 et cette absorption est comprise entre zéro et un aux erreurs d’arrondi près.

Contrôle les cas synthétiques Z_s=Z0, Z_s grand devant Z0 et une impédance purement réactive non singulière. Vérifie alpha_code=+i*omega_phys*rho_air/Z_s et alpha_phys=-alpha_code. Signale données invalides, divisions presque nulles et fréquences hors validité. Conserve les clés du dictionnaire. Fournis à Yann les coefficients des fréquences retenues. Un résidu du solveur ne suffit pas à valider la passivité et ce contrôle plan ne mesure pas la performance du tunnel. Ne lance aucune campagne Helmholtz dans preprocessing.py.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** L’impédance adaptée donne une réflexion nulle dans le cas synthétique et une impédance réactive donne une absorption nulle aux arrondis près.

**Passage de main.** Transmettre la loi et les diagnostics à Yann avant le calcul de la référence plane, puis à Olympia pour annoter les courbes.

## Study the same question for different shapes of fully absorbent walls ;

**Repère :** J2.2. **Rôle :** contributeur.

**Contribution de Mathis.** On vérifie que les différentes formes utilisent la même loi complexe, la même source et les mêmes unités. On réutilise les contrôles de la référence plane.

**Fichier à compléter :** `support/preprocessing.py`.

### Fichiers à joindre

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- `support/preprocessing.py` — cible à modifier.
- `support/demo_control_polycopie2024.py` — lecture seule.
- `context/Sujet-EI-EXT-2026.md` — lecture seule.
- Les paramètres validés, les tableaux et les figures réels de la journée. Pour les tracés, joindre également les champs ou historiques utilisés ; si ces données manquent, les demander avant toute conclusion physique.

### Prompt à copier

```text
Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Compare au plan les profils fournis entièrement recouverts pour le même régime de bruit RER B, avec mêmes source, bande et dimensions de référence annoncées. Chaque profil reste fixe pendant le parcours de sa bande. Affiche les longueurs et quantités de matériau de chaque mur.

Vérifie la passivité et la validité fréquentielle de la loi complexe sur chaque bande RER B effectivement calculée ; un coefficient pris à une seule fréquence ne représente pas toute la bande.

Modifie uniquement support/preprocessing.py joint et renvoie sa version complète si une modification est nécessaire. Les autres fichiers sont fournis en lecture seule. Conserve les fonctions des autres membres et les signatures validées.

Relis compute_material_response pour les fréquences utilisées par les profils de niveaux zéro, un et deux. Vérifie que la même fréquence donne le même coefficient quelle que soit la forme, que la loi est évaluée à chaque fréquence et que la bande de validité est respectée. Ne duplique pas le contrôle de passivité déjà ajouté pour le mur plan. Corrige uniquement une erreur identifiée dans preprocessing.py et renvoie sa version complète seulement si une correction est nécessaire. Rappelle dans ta réponse les hypothèses de comparaison et le fait qu’un mur entièrement recouvert emploie une quantité liée à sa longueur. Aucun calcul de champ ni tracé n’est ajouté dans ce module.

Ne crée aucun autre fichier Python. Les commentaires et docstrings sont de courtes phrases françaises sans équations ni symboles mathématiques. Les petits contrôles restent dans ce même fichier et ne se lancent pas lors de son import. Après le fichier complet, donne une courte explication et les contrôles réellement exécutés. Si tu ne peux pas les lancer, indique les appels à faire sans annoncer leur réussite.
```

**Contrôle attendu.** Les données physiques sont identiques entre formes à fréquence donnée, et les quantités des références entièrement recouvertes sont annoncées.

**Passage de main.** Confirmer ces paramètres à Yann et Olympia avant de comparer les courbes de formes différentes.
