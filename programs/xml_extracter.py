import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
import os
import re

def xml_extractor(root):
    rows = {}

    invdoc = root.find("invdoc")
    rows["BillNumber"] = int(invdoc.attrib.get("ContractAccount"))

    date = root.attrib['date']
    rows["IssueDate"] = datetime.strptime(date, "%Y%m%d").strftime("%m-%d-%Y")

    i = 0
    service = list(root.iter("Service"))[0]
    for usage in service.iter("Usage"):
        date = usage.attrib['date']
        rows[f'PrevMonPeriod_{i}'] = datetime.strptime(date, "%Y%m%d").strftime("%m-%d-%Y")
        rows[f'PrevMonConsumption_{i}'] = float(usage.attrib['Consumption'])
        
        for tou in usage.iter("Tou"):
            peak_type = tou.attrib.get("Peak")
            consumption = float(tou.attrib.get("Consumption"))
            
            # Assign consumption based on the peak type
            if peak_type == "on":
                rows[f'PrevMonPeak_{i}'] = consumption
            elif peak_type == "mid":
                rows[f'PrevMonMidpeak_{i}'] = consumption
            elif peak_type == "off":
                rows[f'PrevMonOffpeak_{i}'] = consumption
        i += 1
    return rows

def save_to_csv(extracted_data, output_csv):
    """Save the extracted data (list of dictionaries) to an existing CSV file"""
    
    # Load existing CSV if available, otherwise create a new DataFrame
    if os.path.exists(output_csv):
        df = pd.read_csv(output_csv)
    else:
        df = pd.DataFrame()

    # Ensure extracted data matches the CSV columns
    if df.empty:
        headers = extracted_data[0].keys()  # Use keys as headers if file is empty
    else:
        headers = df.columns  # Use existing headers

    # Convert extracted data to DataFrame
    extracted_df = pd.DataFrame(extracted_data, columns=headers)

    # Append new data to the existing DataFrame
    df = pd.concat([df, extracted_df], ignore_index=True)

    # Save back to CSV
    df.to_csv(output_csv, index=False)

    print(f"Extracted data saved to {output_csv}")


def main():
    output_csv = "extracted_data.csv"
    rows = []
    with open("SAP_20190122201654_utility.xml") as f:
        xml = f.read()
    tree = ET.fromstring(re.sub(r"(<\?xml[^>]+\?>)", r"\1<root>", xml) + "</root>")

    root = tree.getroot()
    extracts = list(root.iter("invextract"))
    for i in extracts:
        rows.append(xml_extractor(i))
    save_to_csv(rows, output_csv)

if __name__ == "__main__":
    main()