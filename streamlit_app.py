import streamlit as st
import requests
from bs4 import BeautifulSoup

API_URL = "https://europe-west1-smileandpay-1d455.cloudfunctions.net/test_paymentWeb-1"

st.set_page_config(layout="wide")

st.title("Test API Smile&Pay - Parcours Complet")

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

                # Ajout affichage page paiement dans la colonne de droite
                with col2:
                    st.subheader("Page de paiement Nepting")
                    st.markdown(
                        f'<iframe src="{action_url}" width="100%" height="600"></iframe>',
                        unsafe_allow_html=True
                    )

                # Simulation interne des callbacks
                st.subheader("Simulation callbacks (back)")
                callback_type = st.selectbox("Simuler un retour", ["Success", "Error", "Refused", "Cancel"])

                if st.button("Exécuter simulation callback"):
                    simulated_post = {
                        "nep_Result": callback_type,
                        "nep_TransactionID": inputs.get("nep_TransactionID", "TEST123"),
                        "nep_MerchantID": inputs.get("nep_MerchantID", "SMILEPAY_TEST"),
                        "nep_Amount": inputs.get("nep_Amount", str(amount)),
                        "nep_APIVersion": "03.12",
                        "nep_MerchantPrivateData": private_data
                    }

                    # Déterminer l'URL cible en fonction du type de callback
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

        else:
            st.error(f"Erreur {response.status_code}: {response.text}")
