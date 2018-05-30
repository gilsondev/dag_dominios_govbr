#!/usr/bin/env python
# -*- coding: utf-8 -*-

import responses

from pathlib import Path

from dag_dominios_govbr.processors import (
    DownloadFileProcessor,
    ImportDataProcessor
)
from dag_dominios_govbr.models import Domain


FILENAME = 'Dominios_GovBR_basico.csv'
DESTINATION_PATH = '/tmp/'
DESTINATION_FILE = f'{DESTINATION_PATH}/{FILENAME}'
DOMAINS_CSV_URL = f'http://dominios.governoeletronico.gov.br/dados-abertos/{FILENAME}'  # noqa


def open_domain_csvfile():
    csv_file = Path('./tests/data/Dominios_GovBR_basico.csv')
    return open(csv_file, encoding='latin-1')


def download_csvfile():
    responses.add(
        method=responses.GET,
        url=DOMAINS_CSV_URL,
        body=open_domain_csvfile().read(),
        content_type="text/csv",
        headers={
            "Content-Disposition": f'attachment;filename={FILENAME}'
        }
    )

    download_processor = DownloadFileProcessor(
        url=DOMAINS_CSV_URL,
        filename=FILENAME,
        path=DESTINATION_PATH
    )
    download_processor.run()


@responses.activate
def test_download_csv_file():
    """Should should csv data and save in temporary folder"""
    download_csvfile()

    assert Path(DESTINATION_FILE).is_file(), "File is not exists"


@responses.activate
def test_import_domain_data(session):
    download_csvfile()

    import_processor = ImportDataProcessor(
        source=DESTINATION_FILE,
        session=session
    )
    import_processor.run()

    total = session.query(Domain).count()

    assert total > 0
