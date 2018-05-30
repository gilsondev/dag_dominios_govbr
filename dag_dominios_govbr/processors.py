import requests
import rows

from pathlib import Path

from dag_dominios_govbr.models import DOMAIN_CSV_FIELDS, Domain


class DownloadFileProcessor:
    def __init__(self, url: str, filename: str, path: str):
        self.url = url
        self.filename = filename
        self.path = path

    def _download(self):
        destination_path = f'{self.path}/{self.filename}'
        response = requests.get(self.url, stream=True)

        with open(Path(destination_path), 'w') as file:
            file.write(response.text)

    def run(self):
        self._download()


class ImportDataProcessor:
    def __init__(self, source: str, session):
        self.source = source
        self.session = session

    def _load_file(self):
        domains = rows.import_from_csv(
            self.source,
            encoding='latin-1',
            fields=DOMAIN_CSV_FIELDS
        )

        return domains

    def _is_domain_exits(self, domain):
        return self.session.query(Domain).filter_by(
            domain=domain.domain).count()

    def _insert(self, domains):
        objects = []
        for domain in domains:
            if not self._is_domain_exits(domain):
                objects.append(Domain(**domain._asdict()))

        self.session.bulk_save_objects(objects)
        self.session.commit()
        self.session.close()

    def run(self):
        domains = self._load_file()
        self._insert(domains)
