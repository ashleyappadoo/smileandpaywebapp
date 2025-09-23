import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

API_URL = "https://europe-west1-smileandpay-1d455.cloudfunctions.net/test_paymentWeb-1"

st.set_page_config(layout="wide")

# Vérifie si le logo existe à la racine
logo_path = "logosp.jpg"

col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=80)
    else:
        st.warning("Logo introuvable : placez 'logosp.jpg' à la racine du repo (même dossier que streamlit_app.py)")
with col_title:
    st.title("Test API WEB PAY - Smile and Pay")

# Stockage de l'état pour éviter le reset
if "html_response" not in st.session_state:
    st.session_state.html_response = None
if "form_inputs" not in st.session_state:
    st.session_state.form_inputs = None
if "action_url" not in st.session_state:
    st.session_state.action_url = None

# Formulaire utilisateur
col1, col2 = st.columns([2, 3])
with col1:
    ilot = st.text_input("Ilot", "026279")
    vendeur = st.text_input("Vendeur", "026279.aappadoo")
    amount = st.number_input("Montant (centimes)", min_value=1, value=100)
    private_data = st.text_input("Private Data", "orderId=ABCD-1234")

    url_success = st.text_input("URL Success", "https://hook.eu2.make.com/ry8pjf4dhv5w36a4fb6v6gvx4hyh1wmi")
    url_error = st.text_input("URL Error", "https://hook.eu2.make.com/gfmk9t9xmqq8j4ekum6cdgbtwtnv18ab")
    url_refused = st.text_input("URL Refused", "https://hook.eu2.make.com/llzdi8cqv4sd9n2fzqj4w85yq6khig9t")
    url_cancel = st.text_input("URL Cancel", "https://hook.eu2.make.com/iq9azdcvqxgieczm7r79t27ok35cetvy")

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
            st.session_state.html_response = response.text
            soup = BeautifulSoup(st.session_state.html_response, "html.parser")
            form = soup.find("form")
            if form:
                st.session_state.action_url = form.get("action")
                st.session_state.form_inputs = {i.get("name"): i.get("value") for i in form.find_all("input")}
        else:
            st.error(f"Erreur {response.status_code}: {response.text}")

# Affichage du HTML et du formulaire extrait
if st.session_state.html_response:
    st.subheader("Réponse HTML de l’API")
    st.code(st.session_state.html_response, language="html")

if st.session_state.form_inputs:
    st.subheader("Formulaire extrait")
    st.write("**Action URL:**", st.session_state.action_url)
    st.json(st.session_state.form_inputs)

    with col2:
        st.subheader("Page de paiement Nepting")
        st.info("⚠️ L’iframe est bloquée par Nepting (X-Frame-Options). Utilisez le lien ci-dessous pour ouvrir la page dans un nouvel onglet.")
        st.markdown(f"<a href='{st.session_state.action_url}' target='_blank'>👉 Ouvrir la page de paiement Nepting</a>", unsafe_allow_html=True)

    # Simulation interne des callbacks
    st.subheader("Simulation callbacks (back)")
    callback_type = st.selectbox("Simuler un retour", ["Success", "Error", "Refused", "Cancel"])

    if st.button("Exécuter simulation callback"):
        simulated_post = {
            "nep_Result": callback_type,
            "nep_TransactionID": st.session_state.form_inputs.get("nep_TransactionID", "TEST123"),
            "nep_MerchantID": st.session_state.form_inputs.get("nep_MerchantID", "SMILEPAY_TEST"),
            "nep_Amount": st.session_state.form_inputs.get("nep_Amount", str(amount)),
            "nep_APIVersion": "03.12",
            "nep_MerchantPrivateData": private_data
        }

        if callback_type == "Success":
            target_url = url_success
        elif callback_type == "Error":
            target_url = url_error
        elif callback_type == "Refused":
            target_url = url_refused
        else:
            target_url = url_cancel

        try:
            resp = requests.post(target_url, data=simulated_post, headers={"Content-Type": "application/x-www-form-urlencoded"})
            st.write(f"Callback simulé envoyé vers {target_url} :")
            st.json(simulated_post)
            st.success(f"Réponse du webhook ({resp.status_code}): {resp.text}")
        except Exception as e:
            st.error(f"Erreur lors de l'envoi du callback : {e}")
