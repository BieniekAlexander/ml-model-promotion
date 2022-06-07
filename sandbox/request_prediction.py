# source: https://cloud.google.com/vertex-ai/docs/predictions/online-predictions-custom-models#online_predict_custom_trained-python
# imports
from google.cloud import aiplatform
import argparse
import json

# constants
SCHEMA = ['age',
	'workclass',
	'fnlwgt',
	'education',
	'education-num',
	'marital-status',
	'occupation',
	'relationship',
	'race',
	'sex',
	'capital-gain',
	'capital-loss',
	'hours-per-week',
	'native-country']


def request_prediction(project_id, endpoint_id, region, request_json):
	"""Get a prediction from vertexAI

	Args:
			project_id
			endpoint_id
			region
			json
	"""
	request_input = [request_json[k] for k in SCHEMA]
	aiplatform.init(project=project_id, location=region)
	endpoint = aiplatform.Endpoint(endpoint_id)
	prediction = endpoint.predict(instances=[request_input])
	print(prediction)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Request a prediction from a model in VertexAI')
	parser.add_argument('--project-id', dest='project_id', required=True,
                    help='project containing the VertexAI endpoint')
	parser.add_argument('--endpoint-id', dest='endpoint_id', required=True,
                    help='id of the endpoint we want to hit')
	parser.add_argument('--region', dest='region', default='us-east1',
                    help='region where the endpoint lives')
	parser.add_argument('--json-path', dest='json_path', default='test_sample.json',
                    help='path where our request JSON lives')

	args = parser.parse_args()
	request_json = json.load(open(args.json_path, "r"))
	request_prediction(args.project_id, args.endpoint_id, args.region, request_json)