FROM gcr.io/deeplearning-platform-release/tf2-cpu.2-6
WORKDIR /

# set up python environment
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy scripts and data and training
COPY model.py /model.py

# Set up the entry point to invoke the trainer
# MODEL_OBJECT_NAME needs to have the name MODEL.<ext>, per Vertex AI
ARG MODEL_FILENAME=model.pkl
ARG MODEL_OBJECT_NAME=model.pkl
ARG MODEL_BUCKET_PATH
CMD python model.py --filename $MODEL_FILENAME && gsutil cp $MODEL_FILENAME $MODEL_BUCKET_PATH/$MODEL_OBJECT_NAME