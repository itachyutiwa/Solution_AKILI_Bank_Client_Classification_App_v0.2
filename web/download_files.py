import pandas as pd
from io import BytesIO
import base64

def download_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_file_download_link(processed_data, file_name, file_label):
    b64 = base64.b64encode(processed_data)
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{file_name}">{file_label}</a>'
    return href