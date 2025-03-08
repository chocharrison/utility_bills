import google.generativeai as genai
import json
import fitz  # PyMuPDF
import pandas as pd
import os

# Configure Gemini API
#genai.configure(api_key="YOUR_GEMINI_API_KEY")
print(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def extract_text(path):
    doc = open(path)
    text = doc.read()
    return text

def call_gemini_api(text):
    """Use the Gemini API to extract structured data"""
    model = genai.GenerativeModel("gemini-pro")
    
    prompt = f"""
here is some info from a billing document:

{text}

I want to extract the information to a json: BillNumber,IssueDate,Address,CurrentCharges,ConsumptionValue,OffpeakCharges,OffpeakConsumption,MidpeakCharges,MidpeakConsumption,PeakCharges,PeakConsumption,PrevMonPeriod_1,PrevMonConsumption_1,PrevMonPeriodOffpeak_1,PrevMonConsumptionOffpeak_1,PrevMonPeriodMidpeak_1,PrevMonConsumptionMidpeak_1,PrevMonPeriodPeak_1,PrevMonConsumptionPeak_1,PrevMonPeriod_2,PrevMonConsumption_2,PrevMonPeriodOffpeak_2,PrevMonConsumptionOffpeak_2,PrevMonPeriodMidpeak_2,PrevMonConsumptionMidpeak_2,PrevMonPeriodPeak_2,PrevMonConsumptionPeak_2 till n.


Here are some rules:

1. the total charges is ELECTRIC charges not TOTAL charges.

2. only give the info, no extra text is required.

3. Leave blank if that data is not available. no assumptions.

4. Only extract the electricity information, no other utilites.

5. No header is needed, only the data.

6. it should follow the previous format so it can be storable in csv.

7. date should be in MM-DD-YYYY format in numbers.

8. should follow the format above, no mixup.

    """
    response = model.generate_content(prompt)
    return response.text if response else ""

def save_to_csv(extracted_data, output_csv):
    """Save the extracted JSON data to an existing CSV file"""
    
    # Load existing CSV if available, otherwise create a new one
    if os.path.exists(output_csv):
        df = pd.read_csv(output_csv)
    else:
        df = pd.DataFrame()

    # Ensure the extracted JSON data matches the CSV columns
    if df.empty:
        headers = extracted_data.keys()  # Use keys as headers if file is empty
    else:
        headers = df.columns  # Use existing headers

    # Convert extracted JSON data to DataFrame and append it
    extracted_df = pd.DataFrame([extracted_data], columns=headers)

    if "Address" in extracted_df.columns:
        extracted_df["Address"] = extracted_df["Address"].str.replace("\n", " ", regex=False)
        
    df = pd.concat([df, extracted_df], ignore_index=True)

    # Save back to CSV
    df.to_csv(output_csv, index=False)

def main():
    pdf_path = "sample.txt"  # Replace with your PDF file path
    output_csv = "extracted_data.csv"

    # Extract raw text from PDF
    extracted_text = extract_text(pdf_path)
    
    # Call Gemini API to process and extract structured data
    structured_data = json.loads(call_gemini_api(extracted_text))
    print(structured_data)
    # Save extracted structured data into CSV
    save_to_csv(structured_data, output_csv)

    print(f"Extracted data saved to {output_csv}")

if __name__ == "__main__":
    print("Current Directory:", os.getcwd())
    print("Files in Directory:", os.listdir())
    main()