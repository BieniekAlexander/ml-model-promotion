# Setup
# imports
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier
from google.cloud import storage
from pathlib import Path
import argparse
import json


def create_model(model_filepath, report_filepath, gcp_project, gcs_train_csv_path, gcs_test_csv_path):
	# download data
	Path("data").mkdir(parents=True, exist_ok=True)
	storage_client = storage.Client(gcp_project)

	for uri in [gcs_train_csv_path, gcs_test_csv_path]:
		bucket = uri.split("/")[2]
		object_path = "/".join(uri.split("/")[3:])
		object_name = uri.split("/")[-1]
		bucket = storage_client.get_bucket(gcp_project)
		blob = bucket.blob(object_path)
		blob.download_to_filename(f"data/{object_name}")

	train_data = pd.read_csv(f'data/{gcs_train_csv_path.split("/")[-1]}', skipinitialspace=True, comment="|")
	test_data = pd.read_csv(f'data/{gcs_test_csv_path.split("/")[-1]}', skipinitialspace=True, comment="|")
	
	train_features = list(set(train_data.columns) - set(["income"]))
	X_train, y_train = train_data.loc[:, train_data.columns.isin(train_features)], np.array(train_data["income"])
	X_test, y_test = test_data.loc[:, test_data.columns.isin(train_features)], np.array(test_data["income"])
	y_test = np.array(list(map(lambda x: x.replace('.', ''), y_test)))

	# EDA
	X_train.describe()

	# make model pipeline
	from sklearn.preprocessing import OneHotEncoder
	from sklearn.linear_model import LogisticRegression
	from sklearn.pipeline import Pipeline																																																																																																																																																																																																																																																																																																																																																																																																											

# preprocessing and training pipeline
	pipe = Pipeline([
		('ohe', OneHotEncoder(handle_unknown='ignore')),
		('svc', LogisticRegression())
	])

	pipe.fit(X_train, y_train)

	# Evaluation
	auc_roc = roc_auc_score(y_test, pipe.predict_proba(X_test)[:, 1])
	evaluation_results = {
		"evaluation_metric": "auc_roc",
		"score": auc_roc
	}

	with open(report_filepath, 'w') as report_file:
		report_file.write(json.dumps(evaluation_results))

	# Serializing the model
	import joblib
	joblib.dump(pipe, model_filepath, compress=True)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Output model somewhere')
	parser.add_argument('--model-filepath', dest='model_filename', default="model.joblib", required=False,
                    help='path of the model output file (default: model.joblib)')
	parser.add_argument('--report-filepath', dest='report_filename', default="report.json", required=False,
                    help='path of the evaluation report json (default: report.json)')

	parser.add_argument('--gcp-project', dest='gcp_project', default="report.json", required=True,
                    help='GCP project where Cloud Storage bucket lives')
	parser.add_argument('--gcs-train-csv-path', dest='gcs_train_csv_path', default="report.json", required=True,
                    help='path to train csv in Google Cloud Storage')
	parser.add_argument('--gcs-test-csv-path', dest='gcs_test_csv_path', default="report.json", required=True,
                    help='path to train csv in Google Cloud Storage')

	args = parser.parse_args()
	create_model(args.model_filename, args.report_filename)
