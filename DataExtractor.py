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

    def transform(self):
        invoices_data, expired_data = self._load_dataset()
        print(invoices_data)
        invoices = []

        for invoice in invoices_data:
            try:
                invoice_id = int(invoice['id'].replace('O', '0'))
            except AttributeError:
                invoice_id = int(invoice['id'])
            created_on = pd.to_datetime(invoice['created_on'])
            invoice_total = sum(item['unit_price'] * quantity for item, quantity in invoice['items'])
            if 'items' in invoice:
                for item, quantity in invoice['items']:
                    invoiceitem_id = item['id']
                    invoiceitem_name = item['name']
                    types = {0: 'Material', 1: 'Equipment', 2: 'Service', 3: 'Other'}
                    type = types.get(item['type'])
                    unit_price = item['unit_price']
                    total_price = item['unit_price'] * item['quantity']
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
