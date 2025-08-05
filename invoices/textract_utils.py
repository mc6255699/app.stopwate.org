# app/invoices/textract_utils.py

import boto3
import decimal

def extract_amount_due(file_path):
    client = boto3.client('textract')
    with open(file_path, 'rb') as f:
        response = client.analyze_expense(Document={'Bytes': f.read()})

    amount_due = None
    for doc in response.get('ExpenseDocuments', []):
        for field in doc.get('SummaryFields', []):
            label = field.get('LabelDetection', {}).get('Text', '').lower()
            if 'total' in label or 'amount due' in label:
                value = field.get('ValueDetection', {}).get('Text')
                try:
                    amount_due = round(decimal.Decimal(value.replace('$', '').replace(',', '')), 2)
                except:
                    pass
                break

    return amount_due, response
