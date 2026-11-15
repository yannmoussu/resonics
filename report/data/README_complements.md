# Provenance des compléments du rapport

Les spectres des géométries, le cas au niveau deux avec 40 % de matériau, le
panneau à 20 % et l'historique des premiers essais sont repris des images de
context/SlidesVF. Les images originales sont copiées sans modification. Le
panneau à 20 % est sélectionné dans LaTeX par trim et clip. Ses courbes ne sont
ni numérisées ni recalculées ; les valeurs 608 et 832 restent celles de la soutenance.
L'historique historique illustre la décroissance pendant cent itérations, sans
l'attribuer au cas final dont les données de convergence ne sont pas disponibles.

alpha_ouate.csv reprend les coefficients de context/EI_Antoine/resultats pour
l'ouate sur 50–2 000 Hz par pas de 5 Hz. Les trois valeurs à 200, 800 et 2 000 Hz
ont été recalculées avec compute_alpha et comparées aux valeurs enregistrées.
Les paramètres et écarts sont dans verification_parametres_alpha.json.
prepare_complements.py retrace seulement les parties réelle et imaginaire
depuis ce CSV. Il ne modifie aucun programme de calcul.

Les autres données numériques récentes ne sont pas utilisées pour redessiner
les spectres historiques : les valeurs obtenues avec la version actuelle ne
coïncident pas avec les courbes de soutenance.
