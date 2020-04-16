SETTINGS="--runtime python37 --memory=1024MB --timeout=180s"
#gcloud functions deploy  bitdotioinc-pa-covid-data-ingest 
gcloud functions deploy  bitdotioinc-pa-covid-data-ingest-instantaneous ${SETTINGS} --entry-point=instantaneous_pubsub --trigger-topic=trigger-pa-data-ingestion-instantaneous-cloud-function
gcloud functions deploy  bitdotioinc-pa-covid-data-ingest-historical ${SETTINGS} --entry-point=historical_pubsub --trigger-topic=trigger-pa-data-ingestion-historical-cloud-function

