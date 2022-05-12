# Setup
# imports
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from google.cloud import storage
from pathlib import Path
import argparse	 


def create_model(filename):
	# download data
	project_name = "mw-ds-model-promotion-poc-res"
	Path("data").mkdir(parents=True, exist_ok=True)
	storage_client = storage.Client(project_name)
	bucket = storage_client.get_bucket(project_name)

	for csv_name in ['census_income_census_income_data_adult.test.csv', 'census_income_census_income_data_adult.data.csv']:
		blob = bucket.blob(csv_name)
		blob.download_to_filename(f"data/{csv_name}")

	train_data = pd.read_csv('data/census_income_census_income_data_adult.data.csv', skipinitialspace=True, comment="|")
	test_data = pd.read_csv('data/census_income_census_income_data_adult.test.csv', skipinitialspace=True, comment="|")
	
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
	pipe.score(X_test, y_test)

	# TODO do cross-validation

	# Evaluation
	pipe.score(X_test, y_test)

	# Serializing
	import joblib
	joblib.dump(pipe, filename, compress=True)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Output model somewhere')
	parser.add_argument('--filename', dest='filename', default="model.joblib", required=False,
                    help='name of the model output file (default: model.joblib)')

	args = parser.parse_args()
	create_model(args.filename)
