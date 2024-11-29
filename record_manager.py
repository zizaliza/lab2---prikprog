from abc import ABC, abstractmethod
from dataclasses import asdict
import json
from typing import List
from record import Record


class RecordRepository(ABC):
    @abstractmethod
    def add(self, record: Record) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Record]:
        pass

class JsonRecordRepository(RecordRepository):
    def __init__(self, file_path: str = "records.json"):
        self.file_path = file_path

    def _load_record_from_file(self) -> List[Record]:
        try:
            with open(self.file_path, "r") as f:
                data = f.read().strip() 
                if not data: 
                    return []
                return [Record(**record) for record in json.loads(data)]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
            return []

    def _save_record_to_file(self, records: List[Record]) -> None:
        with open(self.file_path, "w") as f:
            json.dump([asdict(record) for record in records], f, indent=4)

    def add(self, record: Record):
        try:
            records = self._load_record_from_file()  
            records.append(record)  
            self._save_record_to_file(records) 
        except Exception as e:
            print(f"Ошибка при добавлении результата: {e}")

    def get_all(self) -> List[Record]:
        return self._load_record_from_file()
