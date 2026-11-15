# -*- coding: utf-8 -*-


# On distingue les points intérieurs.
NODE_INTERIOR = -1
# On distingue les points extérieurs au domaine.
NODE_COMPLEMENTARY = -2
# On distingue les points où le champ est imposé.
NODE_DIRICHLET = 1
# On distingue les points où la dérivée normale est imposée.
NODE_NEUMANN = 2
# On distingue les points du mur avec une condition de Robin.
NODE_ROBIN = 3
