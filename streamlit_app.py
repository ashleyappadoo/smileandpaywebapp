# streamlit_app.py
import os
import base64
import streamlit as st
import requests
from bs4 import BeautifulSoup

API_URL = "https://europe-west1-smileandpay-1d455.cloudfunctions.net/test_paymentWeb-1"

st.set_page_config(layout="wide")

# Header (logo à la racine du repo)
col_logo, col_title = st.columns([1, 8])
with col_logo:
    if os.path.exists("logosp.jpg"):
        st.image("logosp.jpg", width=80)
    else:
        st.warning("Logo introuvable : placez 'logosp.jpg' à la racine du repo (même dossier que streamlit_app.py)")
with col_title:
    st.title("Test API WEB PAY - Smile and Pay")
    st.caption("Environnement de test — génère la page de paiement et simule les callbacks (webhooks).")

# state
if "html_response" not in st.session_state:
    st.session_state.html_response = None
if "form_inputs" not in st.session_state:
    st.session_state.form_inputs = None
if "action_url" not in st.session_state:
    st.session_state.action_url = None
if "last_callback_history" not in st.session_state:
    st.session_state.last_callback_history = []  # list of dicts

# Layout: left = form, right = preview/actions
col1, col2 = st.columns([2, 3])

with col1:
    st.header("Entrées")
    ilot = st.text_input("Ilot", "026279")
    vendeur = st.text_input("Vendeur", "026279.aappadoo")
    amount = st.number_input("Montant (centimes)", min_value=1, value=100)
    private_data = st.text_input("Private Data", "orderId=ABCD-1234")

    st.markdown("---")
    st.subheader("Webhooks (URLs publiques)")
    url_success = st.text_input("URL Success", "https://hook.eu2.make.com/ry8pjf4dhv5w36a4fb6v6gvx4hyh1wmi")
    url_error = st.text_input("URL Error", "https://hook.eu2.make.com/gfmk9t9xmqq8j4ekum6cdgbtwtnv18ab")
    url_refused = st.text_input("URL Refused", "https://hook.eu2.make.com/llzdi8cqv4sd9n2fzqj4w85yq6khig9t")
    url_cancel = st.text_input("URL Cancel", "https://hook.eu2.make.com/iq9azdcvqxgieczm7r79t27ok35cetvy")

    st.markdown("---")
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

        try:
            resp = requests.post(API_URL, json=payload, timeout=30)
        except Exception as e:
            st.error(f"Erreur réseau lors de l'appel à l'API : {e}")
            resp = None

        if resp is None:
            pass
        elif resp.status_code != 200:
            st.error(f"Erreur API {resp.status_code} : {resp.text}")
        else:
            # stocke la réponse HTML
            st.session_state.html_response = resp.text
            # parse le form
            soup = BeautifulSoup(st.session_state.html_response, "html.parser")
            form = soup.find("form")
            if form:
                st.session_state.action_url = form.get("action")
                st.session_state.form_inputs = {i.get("name"): i.get("value") for i in form.find_all("input")}
            else:
                st.session_state.action_url = None
                st.session_state.form_inputs = None

            # Génère (optionnel) payment.html sauvegardé temporairement - utile pour debug local
            try:
                with open("payment.html", "w", encoding="utf-8") as f:
                    f.write(st.session_state.html_response)
            except Exception:
                # pas critique — Streamlit Cloud n'expose pas le fichier
                pass

            st.success("Réponse API reçue et analysée.")

with col2:
    st.header("Aperçu / Actions")

    if st.session_state.html_response:
        st.subheader("Réponse HTML de l'API (brute)")
        st.code(st.session_state.html_response, language="html")

    if st.session_state.form_inputs:
        st.subheader("Formulaire extrait")
        st.write("**Action URL:**", st.session_state.action_url)
        st.json(st.session_state.form_inputs)

        # Actions pour ouvrir la page de paiement
        st.markdown("---")
        st.write("### Ouvrir la page de paiement (sans hébergement externe)")

        # 1) Download button (fallback fiable)
        st.download_button(
            label="💾 Télécharger la page de paiement (payment.html)",
            data=st.session_state.html_response,
            file_name="payment.html",
            mime="text/html"
        )

        # 2) Lien data:base64
        try:
            b64 = base64.b64encode(st.session_state.html_response.encode("utf-8")).decode("ascii")
            data_url = f"data:text/html;base64,{b64}"
            st.markdown(
                f'<a href="{data_url}" target="_blank">👉 Ouvrir la page de paiement dans un nouvel onglet (data URL)</a>',
                unsafe_allow_html=True
            )
            st.caption(f"Longueur data (base64) : {len(b64)} caractères (si trop grande, utilisez le téléchargement ou hébergez le HTML).")
        except Exception as e:
            st.error(f"Impossible de générer lien data: {e}")

        st.markdown("---")
        st.write("### Simulation callbacks (envoi vers les URLs renseignées)")

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

            # choisit la cible
            if callback_type == "Success":
                target_url = url_success
            elif callback_type == "Error":
                target_url = url_error
            elif callback_type == "Refused":
                target_url = url_refused
            else:
                target_url = url_cancel

            try:
                r = requests.post(target_url, data=simulated_post, headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=15)
                st.success(f"Callback envoyé vers {target_url} — HTTP {r.status_code}")
                st.json(simulated_post)
                # ajout historique session
                st.session_state.last_callback_history.insert(0, {
                    "type": callback_type,
                    "target": target_url,
                    "status_code": r.status_code,
                    "body": simulated_post
                })
                # limite de stockage
                if len(st.session_state.last_callback_history) > 50:
                    st.session_state.last_callback_history = st.session_state.last_callback_history[:50]
            except Exception as e:
                st.error(f"Erreur en envoyant le callback : {e}")

    else:
        st.info("Après 'Lancer paiement', le formulaire extrait et les actions apparaîtront ici.")

    # historique
    if st.session_state.last_callback_history:
        st.markdown("---")
        st.subheader("Historique des callbacks simulés (session)")
        for h in st.session_state.last_callback_history[:10]:
            st.write(f"- **{h['type']}** → {h['target']} (HTTP {h['status_code']})")

# bas de page
st.markdown("---")
st.caption("Note : en environnement de qualification (qualif.nepting.com) certains callbacks peuvent ne pas être réellement envoyés par Nepting. Utilisez les simulations ci-dessus ou Make/webhook.site pour vérifier le traitement côté serveur.")
