# Raycasting Project

Ce projet est un moteur de rendu 3D par raycasting, développé pour tourner sur un Raspberry Pi dans le cadre de cours d’informatique. L’objectif est de comprendre comment créer une perspective 3D à partir d’une carte 2D et d’optimiser le rendu sur des systèmes limités.

---

## Concept

Le raycasting est une technique utilisée pour simuler une vue 3D en projetant des rayons depuis la position du joueur vers l’environnement. Chaque rayon calcule la distance à l’objet qu’il rencontre (souvent un mur), ce qui permet de déterminer la hauteur des murs à afficher à l’écran et de créer l’illusion de profondeur.  

C’est le principe utilisé dans des jeux classiques comme Wolfenstein 3D. Ici, nous l’utilisons pour :

- Apprendre les bases du rendu 3D pseudo‑3D
- Comprendre comment optimiser les calculs pour des plateformes peu puissantes
- Visualiser les concepts de trigonométrie, DDA et framerate

---

## Techniques utilisées

### Tables trigonométriques

Pour chaque angle possible du rayon, les valeurs de sinus et cosinus sont pré-calculées et stockées dans des tables. Cela évite de recalculer les fonctions trigonométriques à chaque frame, ce qui est coûteux sur un Raspberry Pi.

### Algorithme DDA (Digital Differential Analysis)

Le DDA permet de trouver rapidement les intersections entre les rayons et les murs sur une grille 2D. Il simplifie les calculs et accélère le rendu.

### Gestion du framerate

Le framerate est volontairement réduit (divisé par 2) pour améliorer les performances et garantir un rendu fluide sur du matériel limité.

---

## Fonctionnement global

1. Le joueur a une position et un angle de vue sur une carte 2D.
2. Des rayons sont envoyés depuis sa position dans la direction de la vue.
3. Pour chaque rayon, le DDA calcule où il touche un mur.
4. La distance calculée est utilisée pour déterminer la hauteur du mur à afficher à l’écran.
5. Les valeurs de sinus/cosinus sont récupérées dans les tables pour accélérer les calculs.
6. Le rendu est affiché en 2D pseudo‑3D, créant l’illusion de profondeur.

---

## Objectifs pédagogiques

Ce projet permet de :

- Visualiser et comprendre le raycasting
- Explorer les optimisations pour le rendu 3D sur des systèmes embarqués
- Expérimenter avec la trigonométrie appliquée aux jeux et la gestion des performances
- Apprendre à structurer un projet graphique en Python pour un Raspberry Pi

---

## Références

- [Raycasting sur Wikipédia](https://fr.wikipedia.org/wiki/Raycasting)
- Jeux classiques utilisant le raycasting : Wolfenstein 3D, Doom (premiers épisodes)
- Techniques d’optimisation sur systèmes embarqués
