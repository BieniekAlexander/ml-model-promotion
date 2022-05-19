FROM gcr.io/deeplearning-platform-release/tf2-cpu.2-6
WORKDIR /

# set up python environment
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy scripts and data and training
COPY model.py /model.py

# Set up the entry point to invoke the trainer
# MODEL_OBJECT_NAME needs to have the name MODEL.<ext>, per Vertex AI
ENV MODEL_FILENAME model.joblib
ENV MODEL_BUCKET_PATH gs://mw-ds-model-promotion-poc-res/census_model
ENV MODEL_REPORT_NAME report.json
ENV MODEL_OBJECT_NAME model.joblib

CMD python model.py --model-filepath=$MODEL_FILENAME --report-filepath=$MODEL_REPORT_NAME \
  && gsutil cp $MODEL_FILENAME $MODEL_BUCKET_PATH/$MODEL_OBJECT_NAME \
  && gsutil cp $MODEL_REPORT_NAME $MODEL_BUCKET_PATH/$MODEL_REPORT_NAME