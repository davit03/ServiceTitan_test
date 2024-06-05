import zipfile
import os
import pickle
import pandas as pd


class DataExtractor:
    def __init__(self, data_dir, destination_folder_name='data', is_zip = True, ):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if is_zip:
            destination_folder = os.path.join(current_dir, destination_folder_name)
            os.makedirs(destination_folder, exist_ok=True)
            zip_path = os.path.join(current_dir, data_dir)

            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                zip_file.extractall(destination_folder)
            self.data_dir = destination_folder
        else:
            self.data_dir = os.path.join(current_dir, data_dir)

    def _load_dataset(self):
        with open(os.path.join(self.data_dir, 'invoices_new.pkl'), 'rb') as file:
            invoices_data = pickle.load(file)
        with open(os.path.join(self.data_dir, 'expired_invoices.txt'), 'r') as file:
            expired_data = set(int(i) for i in file.read().split(','))

        return invoices_data, expired_data

    def _word_to_number(self, number):
        mapping = {'ten': 10}
        if isinstance(number, str):
            number = mapping[number.lower()]
        return number

    def transform(self):
        i, j = 0, 0
        invoices_data, expired_data = self._load_dataset()
        for k, invoice in enumerate(invoices_data):
            print(k, invoice)
        invoices = []

        for invoice in invoices_data:
            if 'items' not in invoice:
                continue
            i += 1
            j = 0
            print("big", i)
            try:
                invoice_id = int(invoice['id'].replace('O', '0'))
            except AttributeError:
                invoice_id = int(invoice['id'])
            created_on = pd.to_datetime(invoice['created_on'])
            invoice_total = sum(item['item']['unit_price'] * self._word_to_number(item['quantity']) for item in invoice['items'])
            for item in invoice['items']:
                j+=1
                print(j)
                quantity = self._word_to_number(item['quantity'])
                item = item['item']
                invoiceitem_id = int(item['id'])
                invoiceitem_name = item['name']
                types = {0: 'Material', 1: 'Equipment', 2: 'Service', 3: 'Other'}
                try:
                    item_type = int(item['type'])
                except ValueError:
                    item_type = int(item['type'].replace('O', '0'))
                type = types.get(item_type, 'Other')
                unit_price = item['unit_price']
                total_price = item['unit_price'] * quantity
                percentage_in_invoice = total_price / invoice_total if invoice_total != 0 else 0
                is_expired = invoice_id in expired_data
                invoices.append({
                    'invoice_id': invoice_id,
                    'created_on': created_on,
                    'invoiceitem_id': invoiceitem_id,
                    'invoiceitem_name': invoiceitem_name,
                    'type': type,
                    'unit_price': unit_price,
                    'total_price': total_price,
                    'percentage_in_invoice': percentage_in_invoice,
                    'is_expired': is_expired
                })
        df = pd.DataFrame(invoices)
        df = df.sort_values(by=['invoice_id', 'invoiceitem_id']).reset_index(drop=True)

        return df[
            ['invoice_id', 'created_on', 'invoiceitem_id', 'invoiceitem_name', 'type', 'unit_price', 'total_price',
             'percentage_in_invoice', 'is_expired']]


data_extractor = DataExtractor("data.zip")
data_extractor.transform()
