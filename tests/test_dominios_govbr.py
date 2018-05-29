#!/usr/bin/env python
# -*- coding: utf-8 -*-

import responses

from pathlib import Path

from dag_dominios_govbr.processor import DownloadFileProcessor


def open_domain_csvfile():
    csv_file = Path('./tests/data/Dominios_GovBR_basico.csv')
    return open(csv_file, encoding='latin-1')


@responses.activate
def test_download_csv_file():
    """Should should csv data and save in temporary folder"""
    filename = 'Dominios_GovBR_basico.csv'
    destination_path = '/tmp/'
    destination_file = f'{destination_path}/{filename}'
    domains_csv_url = f'http://dominios.governoeletronico.gov.br/dados-abertos/{filename}'  # noqa

    responses.add(
        method=responses.GET,
        url=domains_csv_url,
        body=open_domain_csvfile().read(),
        content_type="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=Dominios_GovBR_basico.csv"
        }
    )

    download_processor = DownloadFileProcessor(
        url=domains_csv_url,
        filename=filename,
        path=destination_path
    )
    download_processor.run()

    assert Path(destination_file).is_file(), "File is not exists"
