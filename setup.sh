#!/bin/bash
echo "#################################################"
echo "### Creating and activating conda environment ###"
echo "#################################################"
export CONDA_ENV_NAME="model-promotion"

if [ -z "$(conda env list | grep $CONDA_ENV_NAME)" ] ; then # create conda env if it doesn't exist
	conda env create -f environment.yml
	conda activate $CONDA_ENV_NAME
	python -m ipykernel install --user --name=$CONDA_ENV_NAME
else
	conda activate $CONDA_ENV_NAME
fi


echo "#######################"
echo "### Collecting data ###"
echo "#######################"
# TODO
mkdir -p data
# gsutil -m cp \
#   "gs://amazing-public-data/census_income/census_income_data_adult.data" \
#   "gs://amazing-public-data/census_income/census_income_data_adult.names" \
#   "gs://amazing-public-data/census_income/census_income_data_adult.test" \
#   data