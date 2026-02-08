import streamlit as st
import pandas as pd
import joblib

# Load your model and column list
model = joblib.load('car_price_model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.set_page_config(page_title="Car Price Predictor")
st.title("🚗 Car Resale Price Estimator")

# 1. Numerical Inputs
age = st.number_input("Vehicle Age (Years)", value=5)
km = st.number_input("Kilometers Driven", value=40000)
mileage = st.number_input("Mileage (kmpl)", value=18.0)
engine = st.number_input("Engine (CC)", value=1200)
power = st.number_input("Max Power (bhp)", value=80.0)

# 2. Categorical Inputs (You can add more brands/models here)
brand = st.selectbox("Select Brand", ["Maruti", "Hyundai", "Ford", "Toyota", "BMW"])
fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
trans = st.selectbox("Transmission", ["Manual", "Automatic"])

if st.button("Predict Selling Price"):
    # Create a template of 0s for all 160+ columns
    data_dict = {col: [0] for col in model_columns}
    
    # Fill in the numerical values
    data_dict['vehicle_age'] = [age]
    data_dict['km_driven'] = [km]
    data_dict['mileage'] = [mileage]
    data_dict['engine'] = [engine]
    data_dict['max_power'] = [power]
    
    # Logic for One-Hot Encoding: Set the selected category to 1
    # Example: if brand is "BMW", set "brand_BMW" column to 1
    brand_col = f"brand_{brand}"
    fuel_col = f"fuel_type_{fuel}"
    trans_col = f"transmission_type_{trans}"
    
    if brand_col in data_dict: data_dict[brand_col] = [1]
    if fuel_col in data_dict: data_dict[fuel_col] = [1]
    if trans_col in data_dict: data_dict[trans_col] = [1]
    
    # Convert to DataFrame and predict
    input_df = pd.DataFrame(data_dict)
    res = model.predict(input_df)[0]
    
    st.success(f"Estimated Price: ₹ {res:,.2f}")