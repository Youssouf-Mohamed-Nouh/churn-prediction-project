# 🚀 Projet Churn Prediction : Optimisation de la Rétention Client

## 📝 Description du projet
Ce projet a pour objectif de prédire le désabonnement (churn) des clients d'une entreprise de télécommunications en utilisant l'apprentissage automatique sur AWS. Le système est conçu pour être automatisé de bout en bout, de l'ingestion des données jusqu'à la visualisation des prédictions.

## 🏗️ Architecture Technique
Le pipeline suit une approche moderne de MLOps :



1. **Ingestion :** Les données sont déposées dans S3 (`raw/`).
2. **Orchestration :** EventBridge déclenche des Lambdas pour automatiser le cycle de vie via AWS Glue.
3. **ETL :** AWS Glue (PySpark) nettoie et équilibre les données (SMOTE).
4. **Machine Learning :** Entraînement avec XGBoost sur Amazon SageMaker.
5. **Prédictions :** Batch Transform pour le traitement de masse.
6. **Reporting :** Dashboard interactif via Amazon QuickSight.

## 📊 Étapes du Workflow
1. **EDA (Analyse Exploratoire) :** Identification des corrélations clés et gestion du déséquilibre des classes.
2. **Feature Engineering :** Transformation des données brutes en indicateurs pertinents pour le modèle (encodage, normalisation).
3. **Modélisation :** - Utilisation de **XGBoost**.
   - Optimisation des hyperparamètres via SageMaker.
   - Validation via AUC-ROC et Rappel (Recall).
4. **Déploiement :** Système de prédiction par lot (Batch) pour identifier les clients à risque.

## 📈 Résultats et Évaluation
- **Modèle :** XGBoost
- **Score (AUC ROC) :** 0.999
- **Indicateur métier :** Le rappel (Recall) est priorisé pour maximiser la détection des clients quittant réellement le service.

## 🚀 Comment utiliser ce projet
1. Charger les données dans le bucket S3 `telecom-customer-churn-v2/raw/`.
2. Le pipeline d'automatisation (Crawler -> Glue -> SageMaker) s'exécutera automatiquement.
3. Consulter les résultats dans S3 `predictions/` ou visualiser le dashboard dans **QuickSight**.

## 🛠️ Outils utilisés
* **AWS :** S3, Glue, Lambda, EventBridge, SageMaker (Notebooks & Canvas), Athena, QuickSight.
* **Langages/Frameworks :** Python, PySpark, XGBoost, Pandas.

---
*Projet réalisé dans le cadre d'un pipeline de Data Science / MLOps.*
