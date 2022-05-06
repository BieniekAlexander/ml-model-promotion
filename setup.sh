#!/bin/bash
echo "#################################################"
echo "### Creating and activating conda environment ###"
echo "#################################################"
export CONDA_ENV_NAME="ml-model-promotion"

if [ -z "$(conda env list | grep $CONDA_ENV_NAME)" ] ; then # create conda env if it doesn't exist
	conda env create --name $CONDA_ENV_NAME
	conda activate $CONDA_ENV_NAME
	pip install -r requirements.txt
	python -m ipykernel install --user --name=$CONDA_ENV_NAME
else
	conda activate $CONDA_ENV_NAME
fi


echo "####################################"
echo "### Making credentials directory ###"
echo "####################################"
mkdir -p creds