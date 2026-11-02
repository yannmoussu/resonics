# Joachim — Vendredi 6 novembre 2026

Les titres ci-dessous reprennent mot pour mot les tirets de l’énoncé. Une même tâche est partagée avec les autres membres indiqués dans le Gantt, et cette fiche décrit la contribution de Joachim. On reprend toujours la dernière version des fichiers communs. Les modifications de la démonstration suivent Joachim, puis Antoine, puis Yann.

**Cas d’usage RER B.** On utilise la synthèse de Mathis et Olympia dans [SOTA.md](../../SOTA.md). La première plage de travail proposée est le roulement de 250 à 2 000 Hz, puis on prévoit les cas traction et auxiliaires de 100 à 500 Hz et crissement de 1 500 à 4 000 Hz selon les données et les moyens de calcul. Ces plages sont des indications de la synthèse à documenter et à valider en J1.3. Les petits contrôles synthétiques du code restent indépendants de ces bandes.

## To finalize everything

**Repère :** J5.1. **Rôle :** contributeur.

**Contribution de Joachim.** On refait les contrôles des fonctions de coût et de gradient avant de valider le code final.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- support/_env.py, support/preprocessing.py et support/postprocessing.py, en lecture seule
- Les sorties finales des contrôles du gradient et des campagnes
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Vérifie que les paramètres, exports et figures finaux indiquent RER B, le régime, la bande, la source, le matériau, la quantité et la provenance des données. Centre les textes de restitution sur le scénario RER B retenu. Conserve les titres officiels de l’énoncé et tous les contrôles numériques.

Explique les équations et hypothèses pour le panneau RER B, puis relie chaque conclusion aux courbes et aux paramètres réellement retenus.

Relis les fonctions your_compute_objective_function, evaluate_density et evaluate_band de la démonstration finale. Ne modifie aucun fichier pour cette vérification. Liste les appels de contrôles présents et vérifie leurs sorties lorsqu’elles sont fournies. Contrôle les poids, le facteur deux, les conjugaisons, les résidus et la correspondance des paramètres avec les figures. Si une correction est nécessaire, précise la fonction et le contrôle à reprendre pour une intervention séparée dans ce seul fichier.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On donne à Yann la validation des fonctions de Joachim ou la liste précise des corrections à effectuer avant de figer le rendu.

## Preparation of the defense

**Repère :** J5.2. **Rôle :** contributeur.

**Contribution de Joachim.** On prépare l’explication orale du critère, du système adjoint et des conditions aux limites.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- Les figures, valeurs et plan de soutenance retenus par le groupe
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Présente le besoin RER B puis la chaîne qui mène du scénario choisi au panneau retenu. Attribue la synthèse d’état de l’art à Mathis et Olympia. Annonce les bandes effectivement calculées, la représentation de la source et les gains mesurés par le code, sans transformer les perspectives de SOTA.md en résultats obtenus. Garde vingt minutes d’exposé à cinq puis dix minutes de questions.

Explique les équations et hypothèses pour le panneau RER B, puis relie chaque conclusion aux courbes et aux paramètres réellement retenus.

À partir du fichier final demo_control_polycopie2024.py et des résultats fournis, prépare une explication orale des fonctions your_compute_objective_function, evaluate_density et evaluate_band. Ne modifie aucun fichier et ne crée aucun nouveau fichier.

Explique pour chaque fonction les entrées, les étapes et les sorties. Présente le critère de pression, le système direct et l'adjoint, puis montre pourquoi le gradient coûte deux résolutions par fréquence au lieu d'une résolution par variable de conception. Donne un exemple simple de module au carré pour un nombre complexe et un exemple de perturbation pour vérifier une dérivée.

Rappelle la nécessité du champ total avec la source Dirichlet non homogène et la comparaison entre réflexion et ouverture. Relie chaque conclusion aux résultats réellement fournis. Prépare des réponses courtes sur la conjugaison, le facteur deux, le contrôle par différences centrées et la distinction entre pression intégrée et puissance dissipée.

Liste les appels de contrôles déjà présents dans ce même fichier et les résultats à vérifier avant la soutenance. Ne dis pas qu'un calcul a réussi si ses sorties ne sont pas jointes. Donne la réponse directement dans le message pour qu'elle puisse être reprise par Yann dans les documents communs.
```

**Contrôle et passage de main.** On répète avec Antoine la transition entre gradient et descente, puis avec le groupe l’exposé de vingt minutes suivi de dix minutes de questions.

## Finalization of the rapport by the team.

**Repère :** J5.3. **Rôle :** contributeur.

**Contribution de Joachim.** On fournit les équations et les explications validées pour la partie mathématique du rapport.

**Fichier à modifier :** aucun pour cette contribution d’analyse ou de restitution.

**Fichiers concernés :**

- `SOTA.md`, synthèse de Mathis et Olympia sur le RER B, en lecture seule.
- support/demo_control_polycopie2024.py et support/processing.py, versions actuelles en lecture seule
- context/Dirichlet_Nonhomogene.pdf, les deux pages
- Les paragraphes de rapport existants et les équations/figures à relire, s’ils sont disponibles
- context/Sujet-EI-EXT-2026.md

**Contexte :**

```text
Protection du support : cette contribution est une analyse ou une restitution. Tous les fichiers de code joints restent en lecture seule, y compris les deux cellules « Do not modify this cell » du programme principal et les fonctions qu’elles appellent. Donne les explications dans la réponse, sans modifier de fichier.

Le cas d’usage est le bruit du RER B. Utilise SOTA.md joint comme document d’orientation et les paramètres validés du scénario, en distinguant les données sourcées des hypothèses d’étude.

Le rapport final porte sur le cas RER B. Il distingue les plages proposées dans SOTA.md des bandes finalement retenues, donne toutes les valeurs numériques utilisées et justifie la source et les poids fréquentiels. Les liens de l’état de l’art sont cités pour les affirmations qu’ils établissent. Les résultats de calcul, les quantités et le choix du panneau concordent avec les figures et le programme.

Explique les équations et hypothèses pour le panneau RER B, puis relie chaque conclusion aux courbes et aux paramètres réellement retenus.

Prépare dans le message la contribution mathématique finale au rapport, sans créer ni modifier de fichier. Présente le modèle et ses hypothèses, l’étude énergétique selon la forme avec réflexion et ouverture, le critère intérieur, l’adjoint et le gradient de densité, puis le critère multifréquence. Relie les équations aux fonctions réellement présentes et aux contrôles exécutés. Donne les références des documents fournis et les valeurs numériques utilisées dans les tests, sans inventer de résultat manquant.

Relis les paragraphes existants lorsqu’ils sont joints et propose les corrections de fond nécessaires. Les titres de figures décrivent les données représentées et les conclusions figurent dans le texte. Yann intégrera ensuite les éléments approuvés dans le fichier LaTeX commun lors d’une tâche dédiée.

Donne ta réponse dans le message, sans créer ni modifier de fichier. Appuie les affirmations sur les documents et résultats joints. Signale les données manquantes au lieu d’inventer un résultat.
```

**Contrôle et passage de main.** On approuve sa portion du rapport avec Yann et on vérifie que le code, les figures et les explications utilisent les mêmes conventions.
