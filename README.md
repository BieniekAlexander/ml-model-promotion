# Introduction
Modeling repo for ML model environment promotion experiment. The goal is to find a pattern for promoting a model from DEV to QA and then serving the model in PROD.

## Useful Links
- [Brainstorming Diagram](https://lucid.app/lucidchart/bf843b9a-b1f1-45e6-8ac7-1637a36f76c9/edit?invitationId=inv_a75f6b54-dc7c-490b-a8d8-651dfa3727eb&page=0_0#)
- [MW DS Onboarding Outline](https://docs.google.com/document/d/12k1U13-MLPN6bblY-Mc6R4WXSqYeq4EKTecMMbcBqeM/edit)
- [Census Data](https://console.cloud.google.com/storage/browser/amazing-public-data/census_income;tab=objects?project=data-describe&pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&prefix=&forceOnObjectsSortingFiltering=false)

# Environment Management
## Initial Setup
```
# preconditions: installed conda, python 3.9, ... 
source setup.sh
```

## Updating Conda Environment
```
conda env export > environment.yml
conda list -e > requirements.txt
```
