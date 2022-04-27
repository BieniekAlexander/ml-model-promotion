FROM gcr.io/deeplearning-platform-release/tf2-cpu.2-6
WORKDIR /

# set up python environment
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy scripts and data and training
COPY model.py /model.py

# Set up the entry point to invoke the trainer
CMD python model.py && gsutil cp model.pkl gs://mw-ds-model-promotion-poc-res/census_model/model.pkl