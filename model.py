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

	# prepare data
	def preprocess(df):
		# clean prediction feature, make binary
		df['income'] = df['income'].str.replace('.', '')
		assert set(df['income']) == set([">50K", "<=50K"])
		
		df['income_gt_50k'] = (df['income']==">50K")
		df = df.drop(['income'], axis='columns')

		# onehot encode remaining categorical variables
		cat_cols = list(set(df.columns) - set(df._get_numeric_data().columns))
		df = pd.get_dummies(df, columns=cat_cols, dtype="int64")
		df['income_gt_50k'] = df['income_gt_50k'].astype(int)

		return df

	train_data = pd.read_csv('data/census_income_census_income_data_adult.data.csv', skipinitialspace=True, comment="|")
	test_data = pd.read_csv('data/census_income_census_income_data_adult.test.csv', skipinitialspace=True, comment="|")

	train_data = preprocess(train_data)
	test_data = preprocess(test_data)

	cols = train_data.columns
	train_features = list(set(cols) - set(["income_gt_50k"]))
	X_train, y_train = train_data.loc[:, train_data.columns.isin(train_features)], np.array(train_data["income_gt_50k"])
	X_test, y_test = test_data.loc[:, test_data.columns.isin(train_features)], np.array(test_data["income_gt_50k"])

	for dummy_col in list(set(train_features) - set(X_test.columns)):
		X_test[dummy_col] = 0

	# EDA
	X_train.describe()

	# Modeling
	model = XGBClassifier()
	model.fit(X_train, y_train)
	# TODO do cross-validation

	# Evaluation
	model.score(X_test, y_test)

	# Serializing
	model.save_model(filename)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Output model somewhere')
	parser.add_argument('--filename', dest='filename', default="model.pkl", required=False,
                    help='name of the model output file (default: model.pkl)')

	args = parser.parse_args()
	print(f"arg={args.filename}")
	create_model(args.filename)