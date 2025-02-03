# 📞 Gestion des Opérateurs Téléphoniques et des Abonnés

## Description
Ce projet est une application de gestion des opérateurs télécom et de leurs clients, permettant d'administrer les opérateurs, gérer les abonnés et faciliter les transactions téléphoniques.

## Fonctionnalités

### 🔹 Administrateur
- Gère directement les fichiers de données.
- Configure les paramètres et constantes de l’application.

### 🔹 Gestionnaires
- Création et gestion des opérateurs.
- Gestion des numéros et des transactions (vente de numéros et de crédit).
- Consultation des états financiers (journalier, mensuel, annuel).

### 🔹 Clients
- Gestion de compte (connexion par code PIN).
- Consultation et achat de crédit.
- Gestion des appels et des contacts (historique, répertoire, blocage).
- Transfert de crédit entre abonnés du même opérateur.

## 📂 Structure du Projet

- **BD/** : Fichiers de stockage des données.
- **Views/** : Interface utilisateur et affichage (`Functions.py`, `Client.py`, `Operateur.py`).
- **Models/** : Gestion des données et interactions avec les fichiers (`Client.py`, `Operateur.py`).
- **Controllers/** : Logique métier et gestion des actions (`Functions.py`, `Operateur.py`).
- **consts.py** : Constantes du programme.
- **main.py** : Point d’entrée du programme.

## 🛠 Technologies Utilisées
- **Python 3**
- Gestion des fichiers `.txt` pour le stockage des données.
- Bibliothèques standard Python:
    - `os` 
    - `random`
    - `datetime`
    - `sys`
    - `shutil`
    - `re`
    - `threading`
    - `hashlib`
- Bibliothèques installées:
    - `rich`
    - `pyfiglet`
    - `numpy`
    - `sounddevice`
    - `soundfile`

## 📝 Règles de Gestion Importantes
- Un opérateur ne peut pas avoir plus de 3 indices.
- Un numéro est unique et appartient à un seul client.
- Les transferts de crédit sont soumis à des frais de 10 %.
- Les contacts bloqués ne peuvent ni appeler ni être appelés.

## ⚙️ Installation et Exécution

1. **Cloner le dépôt :**
   ```sh
   git clone https://github.com/ShadowHaku54/Operateur-telephonique.git
   cd Operateur-telephonique
   ```

2. **Créer et activer un environnement virtuel**

3. **Installer les dépendances**
    ```sh
    pip install rich pyfiglet numpy sounddevice soundfile
    ```

4. **Assurer vous les éléments importants de la base de donné**
- Le dossier **DB**.
- Le fichier **DB\Gestionnaires.txt** formé par: `nom_admin,mot_de_passe`.
- Les fichiers **DB\Sounds\calling.wav**, **DB\Sounds\coupure_appel.wav**.
- Les dossiers (peuvent être vide) **DB\Clients**, **DB\Operateurs** et **DB\Sounds\Vocaux**.

5. **Exécuter le script principal :**
   ```sh
   python main.py
   ```


## 🚀 Auteur [@ShadowHaku54](https://github.com/ShadowHaku54)

## 📂 Projet [Operateur-telephonique](https://github.com/ShadowHaku54/Operateur-telephonique)
