PROJECT_ID=884338362548
ENDPOINT_ID=1673755764637827072
REGION=us-east1
INPUT_DATA_FILE=test_sample.json

curl -X POST \
	-H "Authorization: Bearer $(gcloud auth print-access-token)" \
	-H "Content-Type: application/json; charset=utf-8" \
	-d "@${INPUT_DATA_FILE}" \
	https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/endpoints/${ENDPOINT_ID}:predict
