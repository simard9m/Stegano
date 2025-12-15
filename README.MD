# Travail Pratique #3 – Stégano


## Auteurs
- SIME09050100 – Simard, Émile  
- BOIX19050400 – Boivin-Thibeault, Xavier

## Description
Application CLI de stéganographie permettant de cacher et récupérer des messages secrets dans des images PNG en utilisant la technique de substitution des bits de poids faible (LSB - Least Significant Bit).

Prérequis
Avant de pouvoir utiliser cette application, assurez-vous d'avoir les éléments suivants installés sur votre système :

Python
Téléchargez et installez Python 3.8+ depuis : https://www.python.org/downloads/

## 1. Installation de l'environnement

Le projet a été réalisé avec un environnement **conda**, mais il est aussi possible d'installer les dépendances avec **pip**, peu importe si l'utilisateur choisit un environnement virtuel ou un autre gestionnaire d'environnements Python

### 1.1. Installation avec conda

1. Se placer dans le dossier `install` du projet.
2. Créer l'environnement à partir du fichier `environment.yml` :
   ```bash
   conda env create -f environment.yml
3. Activer l'environnement :
   ```bash
   conda activate tp2_Emile_xavier
L'environnement est maintenant prêt à être utilisé.

### 1.2. Installation avec pip
1. Créer et activer un environnement virtuel (venv, conda, etc.).
2. Se placer dans le dossier `install`.
3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
Le projet est alors prêt à être utilisé.

---

## Commandes disponibles
1. Cacher un secret dans une image
Syntaxe :

```bash
python src/stegano.py hide -i <chemin_image_input.png> -o <chemin_image_output.png> -s "votre message secret"
```
Exemple :

```bash
python src/stegano.py hide -i input/image.png -o output/image_secret.png -s "Ceci est un message secret"
```
### Options :

-i, --input : Chemin vers l'image PNG source (obligatoire)

-o, --output : Chemin vers l'image PNG de destination (obligatoire)

-s, --secret : Le message secret à cacher en tant que chaîne de caractères (obligatoire)

### Résultat :

Crée une nouvelle image PNG avec le message caché

Le message ne sera pas visible à l'oeil nu

L'image peut être ouverte normalement dans n'importe quel visualiseur

2. Révéler un secret caché
Syntaxe :

```bash
python src/stegano.py reveal <chemin_image_avec_secret.png>
```
Exemple :

```bash
python src/stegano.py reveal output/image_secret.png
```
Résultat :
Affiche le message secret dans la console :

```text
--> secret message is: "Ceci est un message secret"
```
### Limitations

- Seul le format PNG est supporté

- Les modifications apportées aux images PNG sont imperceptibles mais présentes

- Les images JPEG ne sont pas supportées (considérez les convertir en PNG)

- Le message doit être en UTF-8

---
