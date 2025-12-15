Prévisions ML — guide rapide

But: rendre l'interface de prévision opérationnelle avec vos modèles XGBoost/RandomForest.

1) Pré-requis
- Python 3.8+ (une distribution locale est recommandée)
- Installez les dépendances du projet :

```bash
pip install -r projet_coorrige/requirements.txt
```

2) Préparer les modèles
- Les modèles doivent être au format `joblib` et idéalement emballés sous la forme d'un artifact dict :
  `{ 'model': <estimator>, 'feature_columns': [..] }`.

- Un script utilitaire est fourni pour envelopper les modèles bruts si nécessaire :

```bash
python projet_coorrige/scripts/prepare_models.py projet_coorrige/app/models/model_final_bourse_random_forest.joblib
python projet_coorrige/scripts/prepare_models.py projet_coorrige/app/models/model_final_bourse_xgboost.joblib
```

Par défaut le script écrit des fichiers nommés `*_artifact.joblib`. Utilisez `--inplace` pour écraser le fichier d'origine.

3) Démarrer l'application

```bash
python projet_coorrige/app_main.py
```

Puis ouvrir: http://localhost:5000/previsions

4) Tester la prévision
- Charger un fichier CSV (via l'UI Import) ou utiliser un fichier déjà présent dans `projet_coorrige/uploads/`.
- Sélectionner un modèle et la colonne cible (`Close` si présente), configurer le nombre de périodes et lancer.
- Les résultats apparaîtront sous forme de graphique (image base64) et tableau; l'historique est stocké en session.

5) Débogage / Background jobs
- Les tâches de prévision sont soumises en background et stockent leur état sous `projet_coorrige/logs/jobs/<jobid>.json`.
- Si la page n'affiche pas les résultats, consulter les fichiers JSON dans `logs/jobs/` pour l'état et les erreurs.

6) Notes techniques
- Les utilitaires de transformation (features, préparation des données) sont dans `app/utils.py`.
- Les helpers de job (écriture/lecture) ont été ajoutés à `app/utils.py`.

Si vous voulez, je peux maintenant :
- Exécuter une préparation automatique des modèles présents (créez les artefacts),
- Démarrer l'application et simuler une prévision de test automatiquement et vous transmettre le résultat.

Dites-moi si vous voulez que j'exécute ces étapes ici (je peux tenter de lancer un test de bout en bout).