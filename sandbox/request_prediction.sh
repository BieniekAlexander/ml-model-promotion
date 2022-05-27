PROJECT_ID=mw-ds-model-promotion-poc-prod
ENDPOINT_ID=6467556092997009408
REGION=us-east1
INPUT_DATA_FILE=test_sample.json

curl -X POST \
	-H "Authorization: Bearer $(gcloud auth print-access-token)" \
	-H "Content-Type: application/json; charset=utf-8" \
	-d "@${INPUT_DATA_FILE}" \
	https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/endpoints/${ENDPOINT_ID}:predict
