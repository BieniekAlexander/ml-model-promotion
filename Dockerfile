FROM gcr.io/deeplearning-platform-release/tf2-cpu.2-6
WORKDIR /

# set up python environment
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy scripts and data and training
COPY model.py /model.py

# set entrypoint
ENTRYPOINT ["python", "model.py"]
CMD ["--help"]