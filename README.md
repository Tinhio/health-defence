# Health Defence

Projet NSI (Terminale) : un jeu de tower defence en Python avec pygame.

## Récupérer le projet

### Méthode 1 — sans git (la plus simple)

1. Ouvrir la page du dépôt sur GitHub.
2. Cliquer sur le bouton vert **Code**, puis **Download ZIP**.
3. Décompresser l'archive où tu veux (le Bureau, par exemple).
4. Ouvrir le dossier obtenu : il contient `Jeu.py`, `Classe.py` et les images.

### Méthode 2 — avec git

```bash
git clone <URL_DU_DEPOT>
```

## Lancer le jeu

1. Installer Python 3 (cocher « Add Python to PATH » pendant l'installation).
2. Installer pygame, une seule fois, dans le dossier du projet :

```bash
py -m pip install pygame
```

3. Lancer le jeu :

```bash
py Jeu.py
```

Important : les images (`background.png`, `ennemi_1.png`) doivent rester **dans le même dossier** que `Jeu.py`, sinon le programme plante au démarrage.

## Contenu du dossier

| Fichier | Rôle |
|---|---|
| `Jeu.py` | la boucle de jeu : fenêtre, événements, affichage |
| `Classe.py` | les classes `Ennemi_1` et `Tour_1` |
| `background.png` | le décor (900 × 600) |
| `ennemi_1.png` | le sprite de l'ennemi |

## Travailler à plusieurs

- **Avant de coder**, récupérer les nouvelles versions : `git pull`.
- **Après avoir codé**, envoyer son travail : `git add Jeu.py` (le fichier modifié, pas tout), puis `git commit -m "ce que j'ai fait"`, puis `git push`.
- Ne jamais travailler à deux sur le même fichier en même temps : prévenez-vous sur Discord avant de toucher à `Jeu.py`.
- Un commit = une modification compréhensible. Éviter « modif » ou « test ».

## État du projet

- Décor affiché, un ennemi qui suit le chemin.
- À faire : système d'argent, achat de tours, pose et déplacement des tours, tir, pouvoirs.

Note : la classe `Tour_1` de `Classe.py` charge une image `tour_1.png` qui n'est pas encore dans le dossier. Elle n'est pas utilisée par `Jeu.py` pour l'instant, donc le jeu démarre normalement.
