# Calculs ResoniCS

## Lancer l'étude principale

Avec Python, NumPy, SciPy et Matplotlib, depuis la racine du projet :

```sh
python support/demo_control_polycopie2024.py
```

Le mode par défaut est `ETUDE = "spectre_complet"`. Les paramètres se règlent au début du fichier. `MATERIAL_NAME` choisit le matériau du calcul et `SOURCE` la source. L'ouate polyester sert d'exemple initial. Mélamine, laine de verre et ouate polyester restent les trois matériaux d'étude, sans sélection de produit final.

Les résultats sont enregistrés dans `support/resultats_spectre_complet/`, séparément des études antérieures. Le calcul à N=128 est sensiblement plus long qu'un essai réduit. `N_ITERATIONS` fixe le budget maximal d'itérations, distinct du nombre d'itérations effectivement acceptées.

## Optimisation sur la bande

On calcule une seule répartition pour la bande 50–3 500 Hz. Le coefficient du matériau et la source sont évalués à chaque fréquence. Les coefficients et les seconds membres indépendants du placement sont préparés une fois. Les champs d'une proposition acceptée sont réutilisés pour le calcul de l'adjoint suivant.

Par défaut, le placement continu obtenu aux trois pics sert de point de départ à la descente sur la bande. Cette réutilisation évite de consacrer toutes les itérations à la grille très dense requise par les résonances du mur binaire initial. Les deux budgets d'itérations sont enregistrés séparément. L'argument `warm_start=False` de `run_full_spectrum_optimization` permet aussi de repartir directement du mur initial. La fonction `your_optimization_procedure_spectrum` accepte directement la répartition initiale souhaitée.

Le critère utilise les poids de la méthode des trapèzes. On les normalise par la largeur de bande pour conserver une échelle pratique du gradient et du pas de descente. La moyenne ainsi minimisée a les mêmes minimiseurs que l'intégrale. Les fichiers enregistrent aussi l'intégrale, obtenue en multipliant par la largeur de bande. L'amplitude de la source est déjà incluse dans le champ et n'est pas appliquée une deuxième fois.

La projection respecte les bornes de densité et la quantité initiale de matériau. Une étape n'est acceptée que si l'énergie pondérée diminue sur la même grille, avec les mêmes poids. Le pas est multiplié par 1,1 après acceptation et divisé par deux après refus. Les arrêts conservent le seuil de pas et le contrôle de variation des densités. Le tri binaire garde le nombre arrondi de points garnis, puis son énergie est recalculée séparément.

## Choix des fréquences

`FREQUENCES_HZ` fournit une grille de départ, espacée de 50 Hz. Elle n'est pas supposée résoudre tous les pics. On compare les trapèzes de chaque intervalle aux deux trapèzes obtenus en ajoutant son milieu. On raffine en priorité les intervalles contribuant le plus à l'écart, tout en limitant l'espacement sur toute la bande.

Les seuils par défaut sont 1 % pour l'indicateur d'intégrale et 5 % pour la variation du maximum entre les grilles testées. Ce sont des contrôles observés, et non des bornes mathématiques sur l'erreur réelle. `FREQUENCY_REFINEMENTS` limite le nombre de raffinements. Les fréquences finales et les contrôles sont enregistrés.

La grille de descente est ensuite fixe. Après optimisation, une autre grille, comportant des points régulièrement répartis et de nouveaux milieux, est raffinée pour comparer le mur initial, le placement à trois fréquences et les placements de bande continu et binaire. Un arrêt par limite de raffinement est signalé dans les paramètres. Le bilan donne aussi l'écart entre l'intégrale estimée pendant la descente et celle du contrôle plus fin.

Une résonance initiale d'environ 0,27 Hz de largeur à mi-hauteur a été observée à N=128 dans le cas ouate polyester étudié. Cela justifie un raffinement local plutôt qu'un pas universel de 10 ou 20 Hz. La procédure ne certifie pas la détection de toute résonance arbitrairement étroite.

## Résultats enregistrés

- Spectres superposés et détaillés, avec les mêmes conditions pour chaque configuration.
- Historique continu de l'énergie de bande et valeur binaire distincte.
- Répartitions initiale, à trois fréquences, continue et binaire sur la bande.
- Intégrale de l'énergie, réduction relative, maximum et fréquence du maximum.
- Grilles, poids, coefficients complexes, paramètres et contrôles de raffinement.
- CSV, JSON et NPZ contenant les données numériques, ainsi qu'un bilan des observations.

Le pas spatial doit aussi représenter les ondes. À N=128 et 3 500 Hz, on dispose d'environ 12,54 pas par longueur d'onde. Les petits essais servent à vérifier le programme et ne suffisent pas à valider les résultats physiques.

## Autres modes conservés

| `ETUDE` | Calcul |
| --- | --- |
| `"demo"` | Descente monofréquence du support, dont les lignes imposées sont conservées |
| `"trois_pics"` | Somme aux centres des trois gaussiennes, utilisée comme comparaison |
| `"materiaux_validation"` | Coefficients, parois de référence et contrôle du gradient |
| `"monofrequence"` | Comparaisons et placements à une fréquence |
| `"multifrequence"` | Anciennes comparaisons à quelques fréquences cibles et étude des quantités |
| `"comparaison_dispositifs"` | Comparaisons de formes et de matériaux à quantité annoncée |
| `"tous"` | Ensemble des anciennes études comparatives |

Les fonctions à trois pics, de bande et multifréquences partagent désormais le même moteur `optimize_frequency_distribution` dans `processing.py`. L'évaluation du spectre et la définition de l'énergie sont également communes. Le support imposé du professeur conserve sa procédure propre. Les figures et leurs fichiers sont produits dans `postprocessing.py`.

La convention active est celle du polycopié, avec le signe plus devant le coefficient de Robin. Le coefficient identifié est appliqué directement. Les copies de `context/EI_Antoine/` et de `context/fichiers_support/` servent de références et ne sont pas importées par le programme.
