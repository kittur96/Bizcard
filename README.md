# Bizcard text extraction.

Introduction
Fetching text from an image using Streamlit and EasyOCR involves creating a web application with Streamlit that allows users to upload multiple images and then using EasyOCR to extract text from that image.

Project Overview:

Import Libraries: Begin by importing the required libraries, including Streamlit ,re and EasyOCR.

Set Up Streamlit Application: Create a Streamlit application with a title and an image uploader widget. This widget will enable users to upload an image for text extraction.

Image Processing: When a user uploads an image, the application will process the image using EasyOCR. The library will recognize the text in the image based on the language data and return the extracted text.

Regular expressions: used regular expressions to fetch the text from the image and then convert that into dataframe and moved to mysql database.

Mysql databaase:Used mysql database to stroe the extracted text from the images and then prformed CRUD operation thru streamlit only.

Display Results: Show the extracted text on the web application for users to view and along with view user can perform update read and delete the records from the database thru streamlit frontend only.

Conclusion:
By combining Streamlit's simple web application development capabilities ,MYSQL database and EasyOCR's powerful text extraction functionality, I built an interactive web application that allows users to upload images and extract text from them and store them into mysql database. The application will be useful for tasks that involve digitizing documents, processing images with textual content, or creating custom OCR-based solutions. The project demonstrates the power of Python libraries in streamlining OCR tasks and making them accessible to a wider audience through web applications.


