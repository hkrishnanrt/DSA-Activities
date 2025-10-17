import streamlit as st
import pickle

model=pickle.load(open('model/model_final.pkl','rb'))

st.header("Iris Species Prediction")

predictions={0:"setosa",
             1:"vericolor",
             2:"virginica"}

with st.form("iris_app_form"):
    pl=st.text_input("Enter Petal length:")
    pw=st.text_input("Enter Petal width:")
    sl=st.text_input("Enter Sepal length:")
    sw=st.text_input("Enter Sepal width:")
    submitted=st.form_submit_button("Predict")

if submitted:
    prediction= model.predict([[sl,sw,pl,pw]])
    species = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    predicted_species = species[prediction[0]]
    st.success(f"Predicted Species: **{predicted_species}**")