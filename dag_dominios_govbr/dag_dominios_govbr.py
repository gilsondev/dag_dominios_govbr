import airflow

from datetime import timedelta

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from dag_dominios_govbr.processor import DownloadFileProcessor


FILENAME = 'dominios.csv'
DESTINATION_PATH = f'/tmp/'


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id='dominios_govbr',
    default_args=args,
    dagrun_timeout=timedelta(minutes=60)
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

download_processor = DownloadFileProcessor(
    url='http://dominios.governoeletronico.gov.br/dados-abertos/Dominios_GovBR_basico.csv',  # noqa
    filename=FILENAME,
    path=DESTINATION_PATH
)
download = PythonOperator(
    task_id='download_csv',
    python_callable=download_processor.run,
    dag=dag
)
download.set_upstream(start)

import_data = DummyOperator(
    task_id='import_data',
    dag=dag
)
import_data.set_upstream(download)
