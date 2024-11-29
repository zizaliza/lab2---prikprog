from dataclasses import asdict
import json
import re
from typing import List

from requests import RequestException, get
from record_manager import RecordRepository
from record import Record



PATTERN = r'^\d{2}.\d{2}.\d{4}$'

class RegexService:
    def init(self, record_repository: RecordRepository):
        self.record_repository = record_repository
        pass

    def _find_snils(self, text: str) -> List[str]:
        return re.findall(PATTERN, text)
    
    def get_snils_in_file(self):
        record_data = self.record_repository.get_all()
        record_str = ", ".join([str(asdict(record)) for record in record_data])
        date = self._find_snils(record_str)
        return Record(link="jsonFile", date=date)

    def get_dates_in_web(self, url: str):
        try:
            response = get(url)
            if response.status_code == 200:
                dates = self._find_dates(response.text)
                self.record_repository.add(Record(link=url, dates=dates))
                return Record(link=url, dates=dates)
            else:
                print(f"Error: Unable to fetch URL {url}, Status Code: {response.status_code}")
                return Record(link=url, dates=[])
        except RequestException as e:
            print(f"Error: {e}")
            return Record(link=url, dates=[])

    def get_snils_in_text(self, text: str = "") -> List[str]:
        dates = self._find_dates(text)
        self.record_repository.add(Record(link='text', dates=dates))
        return dates
s