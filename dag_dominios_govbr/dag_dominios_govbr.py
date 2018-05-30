import airflow

from datetime import timedelta

from airflow.models import DAG, Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


from dag_dominios_govbr.core.database import (
    database_connect,
    create_session,
    create_tables
)
from dag_dominios_govbr.processors import (
    DownloadFileProcessor,
    ImportDataProcessor
)


FILENAME = 'dominios.csv'
DESTINATION_PATH = f'/tmp/'
DESTINATION_FILE = f'{DESTINATION_PATH}/{FILENAME}'


args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

db_url = Variable.get(
    "OPENDATABR_DATABASE_URL",
    "postgresql://opendata:opendata@localhost:5432/opendatabr"
)
engine = database_connect(
    database_url=db_url
)
create_tables(engine)
session = create_session(engine)

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

import_processor = ImportDataProcessor(
    source=DESTINATION_FILE,
    session=session
)
import_data = PythonOperator(
    task_id='import_data',
    python_callable=import_processor.run,
    dag=dag
)
import_data.set_upstream(download)
