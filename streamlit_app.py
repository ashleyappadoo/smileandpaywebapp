import streamlit as st
import requests
from bs4 import BeautifulSoup

#API DEV
#API_URL = "https://europe-west1-smileandpay-1d455.cloudfunctions.net/test_paymentWeb-1"

#API PROD
https://europe-west1-smileandpay-1d455.cloudfunctions.net/test_paymentWeb_PROD

st.title("Test API Smile&Pay - Parcours Complet")

# Formulaire utilisateur
ilot = st.text_input("Ilot", "026279")
vendeur = st.text_input("Vendeur", "026279.aappadoo")
amount = st.number_input("Montant (centimes)", min_value=1, value=100)
private_data = st.text_input("Private Data", "orderId=ABCD-1234")

url_success = st.text_input("URL Success", "https://merchant.example/success")
url_error = st.text_input("URL Error", "https://merchant.example/error")
url_refused = st.text_input("URL Refused", "https://merchant.example/refused")
url_cancel = st.text_input("URL Cancel", "https://hook.eu2.make.com/ry8pjf4dhv5w36a4fb6v6gvx4hyh1wmi")

if st.button("Lancer paiement"):
    payload = {
        "ilot": ilot,
        "vendeur": vendeur,
        "amount": amount,
        "privateData": private_data,
        "urlSuccess": url_success,
        "urlError": url_error,
        "urlRefused": url_refused,
        "urlCancel": url_cancel
    }

    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        html = response.text
        st.subheader("Réponse HTML de l’API")
        st.code(html, language="html")

        # Parse du formulaire
        soup = BeautifulSoup(html, "html.parser")
        form = soup.find("form")
        if form:
            action_url = form.get("action")
            inputs = {i.get("name"): i.get("value") for i in form.find_all("input")}
            
            st.subheader("Formulaire extrait")
            st.write("**Action URL:**", action_url)
            st.json(inputs)

            # Lien cliquable pour ouvrir la page de paiement
            st.markdown(f"[Accéder à la page de paiement]({action_url})", unsafe_allow_html=True)
    else:
        st.error(f"Erreur {response.status_code}: {response.text}")
