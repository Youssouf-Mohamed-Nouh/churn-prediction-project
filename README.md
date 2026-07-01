# 🚀 Projet Churn Prediction : Optimisation de la Rétention Client

## 📝 Description du projet
Ce projet présente une solution MLOps complète pour prédire le désabonnement (churn) des clients d'une entreprise de télécommunications. Il combine le développement de modèles personnalisés avec l'industrialisation via les outils AWS pour automatiser la chaîne de valeur de la donnée, de l'ingestion jusqu'à la visualisation décisionnelle.

## 🏗️ Architecture Technique
Le pipeline intègre une approche hybride, alliant prototypage expert et industrialisation no-code/low-code :

- **Ingestion & ETL :** Automatisation via EventBridge, Lambda, et Glue (PySpark).
- **Développement (Prototypage) :** Analyse exploratoire et entraînement du modèle XGBoost via **SageMaker Notebooks**.
- **Industrialisation :** Utilisation de **SageMaker Canvas** pour la gestion du cycle de vie des prédictions par lots (Batch Transform).
- **Reporting :** Analyse des segments à risque via Amazon QuickSight et Athena.

## 📊 Workflow du projet
1. **Pipeline de données :** S3 (raw/) ➔ Lambda ➔ Glue Crawler ➔ Glue Job (ETL/SMOTE) ➔ S3 (processud/).
2. **Cycle de vie du modèle :**
   - **Prototypage :** Exploration et développement du modèle XGBoost dans **SageMaker Notebooks**.
   - **Industrialisation :** Déploiement des modèles sur **SageMaker Canvas** pour le traitement de gros volumes.
3. **Visualisation :** Dashboarding interactif sur QuickSight pour le suivi métier.

## 📈 Résultats et Évaluation
- **Modèle :** XGBoost
- **Performance :** AUC ROC de 0.999.
- **Approche métier :** Focus sur le rappel (Recall) pour identifier proactivement les clients susceptibles de quitter l'opérateur.

## 🛠️ Outils utilisés
* **Cloud & MLOps :** AWS (S3, Glue, Lambda, EventBridge, SageMaker, Athena, QuickSight).
* **Développement :** Python, PySpark, XGBoost, Pandas.
* **Méthodologies :** MLOps, ETL, Feature Engineering, Gestion du déséquilibre de classe (SMOTE).

## 🚀 Accès au projet
- **Code & Scripts :** [Lien vers ton GitHub]
- **Documentation technique :** Voir le dossier `/scripts` dans ce dépôt.

---
*Projet réalisé dans le cadre de l'optimisation des stratégies de rétention client par l'intelligence artificielle.*
