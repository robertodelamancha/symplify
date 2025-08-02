# Importer les bibliothèques
from openai import OpenAI
import os
import streamlit as st
#import ipywidgets as widgets

st.set_page_config(
    page_title="Vulgarisation Médicale",
    page_icon="🧬",
    layout="wide",
)

# Étape 3 : Configurer la clé API OpenAI
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"]) # 🔒 Remplacez par votre clé API personnelle

# Étape 4 : Fonction de génération du résumé avec GPT

def get_instruction(langue):
    if langue == "Anglais":
        return "Then, translate the explanation into clear, simple English suitable for a patient."
    elif langue == "Espagnol":
        return "ثم ترجم الشرح إلى العربية المبسطة والواضحة والمناسبة للمريض."
    else:
        return ""  # Français = pas de traduction

def vulgariser_texte(texte_brut, contexte,langue):
    traduction = get_instruction(langue)
    st.write("{type_lang}")
    system_prompt = (
        f"Tu es un assistant médical expert en gastro-entérologie et en radiologie."
        f" Ton objectif est de vulgariser un compte rendu médical technique pour le rendre clair, compréhensible et rassurant pour un patient."
        f" Le texte provient d’un rapport de {contexte}."
        f"{traduction}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": texte_brut}
        ],
        temperature=0.5,
        max_tokens=1000
    )
    return response.choices[0].message.content

# 🎨 Interface Streamlit
st.title("🧪 Vulgarisation de comptes rendus médicaux")

with st.sidebar:
    st.markdown("## ⚙️ Paramètres")
    type_cr = st.selectbox("Type de compte rendu :", ["Endoscopie digestive", "Imagerie médicale"])
    
    langue_options = {
        "Français": "Français",
        "English": "Anglais",
        "العربية": "Arabe"
    }
    langue_affichee = st.selectbox("Langue de vulgarisation :", list(langue_options.keys()))
    type_lang = langue_options[langue_affichee]

intro = {
    "Endoscopie digestive": "Collez un compte rendu **d’endoscopie digestive** (gastroscopie, coloscopie…).",
    "Imagerie médicale": "Collez un compte rendu **d’imagerie médicale** (IRM, scanner, échographie…)."
}
st.markdown(f"📝 {intro[type_cr]}")

texte_cr = st.text_area("Compte rendu médical :", height=300)

if st.button("🧠 Générer la version vulgarisée"):
    if texte_cr.strip() == "":
        st.warning("Veuillez coller un texte médical.")
    else:
        with st.spinner("⏳ Analyse et vulgarisation en cours..."):
            try:
                resultat = vulgariser_texte(texte_cr, type_cr, type_lang)
                st.success("✅ Résumé prêt !")
                st.markdown(f"### 🩺 Résultat :\n\n{resultat}")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
















