
import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66, format="%.2f")
product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027, format="%.3f")
product_mrp = st.number_input("Product MRP", min_value=0.0, value=117.08, format="%.2f")
store_size = st.selectbox("Store Size", ["Medium", "High", "Small"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
store_age_years = st.number_input("Store Age (Years)", min_value=0, value=17)
product_type_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])
product_id_char = st.selectbox("Product ID Characters", ["FD", "NC", "DR"])

# Convert user input into a Dictionary payload
input_data = {
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_mrp,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Store_Age_Years': store_age_years,
    'Product_Type_Category': product_type_category,
    'Product_Id_char': product_id_char
}

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data)  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Sales']
        st.success(f"Predicted Sales (in dollars): {prediction:.2f}")
    else:
        st.error(f"Unable to connect to the prediction API. Error: {response.status_code} - {response.text}")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        # Format the file object expected by requests and Flask
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)  # Corrected endpoint URL
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")

            # Display formatted DataFrame output
            pred_df = pd.DataFrame(list(predictions.items()), columns=["Product ID", "Predicted Sales"])
            st.dataframe(pred_df)
        else:
            st.error(f"Unable to connect to the prediction API. Error: {response.status_code} - {response.text}")
