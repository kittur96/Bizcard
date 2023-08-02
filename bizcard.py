import streamlit as st
from PIL import Image
import easyocr
import re
import numpy as np
import pandas as pd
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="card"
)

cursor = connection.cursor()
# Create a MySQL database connection
database_connection_url = 'mysql+pymysql://{username}:{password}@{host}/{database_name}'
connection_string = database_connection_url.format(
username = 'root',
password = '12345',
host = 'localhost',
database_name = 'card'
)
engine = sqlalchemy.create_engine(connection_string)

Session = sessionmaker(bind=engine)
session = Session()

# function to extract text from images.

def perform_ocr(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    return result


# function to extract relevant informations

def extract_information(ocr_result):
    
    name = ""
    phone_number = ""
    email = ""
    pincode = ""
    company_name = ""
    state = ""
    city = ""

    for detection in ocr_result:
        text = detection[1]

        # Extract Name (Assuming name is the first text in the OCR result)
        if not name:
            name = text

        # Extract Phone Number
        if re.findall(r'\b\+\d{2,3}-\d{2,4}-\d{4,}|\d{3}-\d{4}-\d{3}|\b\+\d{3}-\d{3}-\d{4}\b', text):
            phone_number = text

        # Extract Email ID
        if re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
            email = text

        # Extract Pincode (Assuming pincode is a number with 6 digits)
        if re.findall(r'\d{7}|\d{6}', text):
            pincode = text

        # Extract Company Name
        if re.findall(r'\b(?:\w+\s*){1,3}(?:Pvt\.|Ltd\.)?\b', text, re.IGNORECASE):
            company_name = text

        # Extract State (Assuming state name is in the text TamilNadu)
        # states = ["TamilNadu", "Karnataka", "Andhra Pradesh", "Maharashtra", "Delhi", "Rajasthan"]
        # for s in states:
            if re.findall(r"\btamilnadu\b", text, re.IGNORECASE):
                state = text
        # Extract City (Assuming city name is present in the OCR result)
        city_match = re.search(r',\s*(\w+)', text)
        if city_match:
            city = city_match.group(1)

    return name, phone_number, email, pincode, company_name, state, city



# main function ...
def app():
    # ===========-----------------======================
    # if st.button("alter table"):
    #      cursor.execute("ALTER TABLE bizcard ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY;")
    st.title("EasyOCR Text Extraction")
    st.write("Upload an image and extract the text!")

    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Convert uploaded image to PIL Image
        image = Image.open(uploaded_image)

        # Convert PIL Image to NumPy array
        image_np = np.array(image)

        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Extract text from an image and move it to the database"):
            with st.spinner("Performing OCR..."):
                ocr_result = perform_ocr(image_np)
            st.success("OCR Completed! and data moved to database")

            name, phone_number, email, pincode, company_name, state, city = extract_information(ocr_result)

            data = {
                "name": [name],
                "phone_number": [phone_number],
                "email": [email],
                "pincode": [pincode],
                "company_name": [company_name],
                "state": [state],
                "city": [city]
                    }

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(data)
            st.table(df)
        
            # going to create the table if it doent exist else update the table data...
            df.to_sql('bizcard',con=engine , if_exists='append',index=True)
            engine.dispose() 
            # altering the table to add id column
    if st.sidebar.button("alter table"):
         cursor.execute("ALTER TABLE bizcard ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY;")              
    st.sidebar.title("CRUD Operations")
    selected_option = st.sidebar.selectbox(
        "Select an operation",
        ["None","Read", "Update", "Delete"]
    )
    if selected_option == None:
       pass
    elif selected_option == "Read":
        st.subheader("Read Records")
        cursor.execute("SELECT * FROM bizcard")
        records = cursor.fetchall()
        for record in records:
            st.write(record)
        connection.commit()    
        
    elif selected_option == "Update":
        st.subheader("Update Record")
        id = st.number_input("Enter Record ID")
        name = st.text_input("update name")
        phone_number = st.number_input("Ph number update ")
        email = st.text_input("Updated email")
        pincode = st.number_input("Updated pincode")
        company_name = st.text_input("Updated company_name")
        state = st.text_input("Updated state")
        city = st.text_input("Updated city")
        if st.button("update records"):
            cursor.execute("UPDATE bizcard SET name = %s, phone_number = %s, email = %s, pincode = %s, company_name = %s , state = %s , city = %s WHERE id = %s", (name, phone_number, email, pincode, company_name, state, city,id))
            connection.commit()
            st.success("records updated successfully...")

    elif selected_option == "Delete":
        id = st.number_input("Enter email to be deleted")
        if st.button("delete a record"):
            cursor.execute("DELETE FROM bizcard WHERE id = %s", (id,))
            connection.commit()
            st.success("Record id to be deleted successfully...")    

#  Main function program starts from here only                   
if __name__ == "__main__":
    app()
