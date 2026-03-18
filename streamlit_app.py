import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

API_URL = "https://europe-west1-smileandpay-1d455.cloudfunctions.net/test_paymentWeb_PROD"

st.set_page_config(layout="wide")

# Logo et titre
col_logo, col_title = st.columns([1, 5])
with col_logo:
    if os.path.exists("logosp.jpg"):
        st.image("logosp.jpg", width=80)
    else:
        st.warning("Logo introuvable : placez 'logosp.jpg' à la racine du repo")
with col_title:
    st.title("Test API WEB PAY - Smile and Pay")

# Stockage de l'état
if "html_response" not in st.session_state:
    st.session_state.html_response = None
if "form_inputs" not in st.session_state:
    st.session_state.form_inputs = None
if "action_url" not in st.session_state:
    st.session_state.action_url = None

# Formulaire utilisateur
col1, col2 = st.columns([2, 3])
with col1:
    # Lien vers la doc Postman au-dessus du formulaire
    st.markdown(
        "[📖 Consulter la documentation API (Postman)](https://documenter.getpostman.com/view/43527348/2sB3QQHSSx)",
        unsafe_allow_html=True
    )
    ilot = st.text_input("N° de compte", "Numéro client : 010000")
    vendeur = st.text_input("Vendeur", "Compte vendeur : 010000.identifiant")
    amount = st.number_input("Montant (centimes)", min_value=1, value=100)
    private_data = st.text_input("Private Data", "orderId=ABCD-1234")

    url_success = st.text_input("URL Success", "Saissisez votre url")
    url_error = st.text_input("URL Error", "Saissisez votre url")
    url_refused = st.text_input("URL Refused", "Saissisez votre url")
    url_cancel = st.text_input("URL Cancel", "Saissisez votre url")

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
                st.session_state.form_inputs = {
                    i.get("name"): i.get("value") for i in form.find_all("input")
                }

            st.success("Réponse HTML générée avec succès")
        else:
            st.error(f"Erreur {response.status_code}: {response.text}")

with col2:
    if st.session_state.html_response:
        # Bloc téléchargement
        with st.container():
            st.subheader("Télécharger la page de paiement générée")
            st.info("Cliquez pour récupérer le fichier HTML et l’ouvrir sur votre PC.")
            st.download_button(
                label="💾 Télécharger payment.html",
                data=st.session_state.html_response,
                file_name="payment.html",
                mime="text/html"
            )

        # Séparation
        st.markdown("---")

        st.subheader("Réponse HTML de l’API")
        st.code(st.session_state.html_response, language="html")

    if st.session_state.form_inputs:
        st.subheader("Formulaire Nepting (entrée)")
        st.info("⚠️ Ceci correspond uniquement aux données envoyées pour ouvrir la page de paiement. "
                "Le résultat du paiement (Succès / Annulé / Refusé / Erreur) sera renvoyé via le webhook.")

        entree = {
            k: v for k, v in st.session_state.form_inputs.items()
            if k.startswith("nep_") and not k in [
                "nep_Result", "nep_ExtendedResult",
                "nep_Ticket", "nep_AuthorizationCode",
                "nep_CardToken", "nep_MaskedPan",
                "nep_EndOfValidity"
            ]
        }
        st.json(entree)
