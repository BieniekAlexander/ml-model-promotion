PROJECT_ID=mw-ds-model-promotion-poc-dev
ENDPOINT_ID=4716218787903307776
REGION=us-east1
INPUT_DATA_FILE=test_sample.json

INSTANCES=$(python  <<EOF
import json

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

request_json = json.load(open('$INPUT_DATA_FILE', "r"))
request_input = [request_json[k] for k in SCHEMA]
print({"instances": [request_input]})
EOF
)

curl -X POST \
	-H "Authorization: Bearer $(gcloud auth print-access-token)" \
	-H "Content-Type: application/json; charset=utf-8" \
	-d "$INSTANCES" \
	https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/endpoints/${ENDPOINT_ID}:predict
