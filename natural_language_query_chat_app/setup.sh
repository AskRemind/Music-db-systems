#!/bin/bash

# Add Google Cloud SDK to PATH
export PATH="/Users/$USER/google-cloud-sdk/bin:$PATH"

# Enable required Google Cloud services
gcloud services enable aiplatform.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable bigquerydatatransfer.googleapis.com

# Create and copy your dataset
bq mk --force=true --dataset song_dataset
bq mk \
  --transfer_config \
  --data_source=cross_region_copy \
  --target_dataset=song_dataset \
  --display_name='Music DB' \
  --schedule_end_time="$(date -v+5M -u +%Y-%m-%dT%H:%M:%SZ)" \
  --params='{
      "source_project_id":"music-db-445310",
      "source_dataset_id":"song_dataset",
      "overwrite_destination_table":"true"
      }'

# Install Python
export PYTHON_PREFIX=~/miniforge
curl -Lo ~/miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.sh
bash ~/miniforge.sh -fbp ${PYTHON_PREFIX}
rm -rf ~/miniforge.sh

# Install packages
${PYTHON_PREFIX}/bin/pip install -r requirements.txt
