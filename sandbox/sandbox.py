# imports
from google.cloud import aiplatform

# constants
PROJECT_ID = "884338362548"
ENDPOINT_ID = "1673755764637827072"
REGION = "us-east1"

input = {
	'age': 25,
	'workclass': 'Private',
	'fnlwgt': 226802,
	'education': '11th',
	'education-num': 7,
	'marital-status': 'Never-married',
	'occupation': 'Machine-op-inspct',
	'relationship': 'Own-child',
	'race': 'Black',
	'sex': 'Male',
	'capital-gain': 0,
	'capital-loss': 0,
	'hours-per-week': 40,
	'native-country': 'United-States'}

aiplatform.init(project=PROJECT_ID, location=REGION)
endpoint = aiplatform.Endpoint(ENDPOINT_ID)
prediction = endpoint.predict(instances=[list(input.values())])

print(prediction)