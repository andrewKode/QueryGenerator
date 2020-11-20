import pandas
import pathlib
import pyperclip
import json

class QueryGenerator:
    def __init__(self, file_list_path):
        self.file_list_path = file_list_path

    def get_documents_from_file(self) -> list:
        def file_is_csv() -> bool:
            if '.csv' in self.file_list_path:
                return True
            else:
                return False
        def file_is_txt() -> bool:
            if '.txt' in self.file_list_path:
                return True
            else:
                return False

        documents = []
        if file_is_csv():
            print('The file is a .csv file.')
            documents = self.get_list_csv(self.file_list_path)
        elif file_is_txt():
            print('The file is a .txt file.')
            documents = self.get_list_txt(self.file_list_path)
        return documents

    def get_list_txt(self, txt_path: str) -> list:
        with open(txt_path, 'r') as fileList:
            documents = fileList.readlines()
        documents = [x.strip() for x in documents]
        return documents

    def get_list_csv(self, csv_path: str) -> list:
        documents = []
        documents_pd = pandas.read_csv(csv_path)
        # convert pandas series to standard list for identical return type
        for document in documents_pd['_id']:
            documents.append(document)
        return documents

    def generate_query(self, documents_list: list) -> object:
        documents_to_match = []
        for document in documents_list:
            matcher = {
                "match_phrase": {
                    "_id": document
                }
            }
            documents_to_match.append(matcher)

        query = {
            "query": {
                "bool": {
                    "should": documents_to_match,
                    "minimum_should_match": 1
                }
            }
        }

        pyperclip.copy(json.dumps(query))
        print("The query syntax for Kibana filter is ready. Paste it in the DSL query option.")

    def run(self):
        self.generate_query(self.get_documents_from_file())