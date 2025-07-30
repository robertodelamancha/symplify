# 📘 Notebok Colab - Vulgarisation CR Endoscopie & Imagerie

# Étape 1 : Installer les bibliothèques nécessaires (si ce n'est pas déjà fait)
#!pip install openai
#!pip install streamlit

# Étape 2 : Importer les bibliothèques
import openai
import os
import streamlit as st
from IPython.display import display, HTML
import ipywidgets as widgets

# Étape 3 : Configurer la clé API OpenAI
client = "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"  # 🔒 Remplacez par votre clé API personnelle

# Étape 4 : Fonction de génération du résumé avec GPT

def vulgariser_texte(texte_brut, contexte):
    system_prompt = (
        "Tu es un assistant médical expert en gastro-entérologie et en imagerie."
        " Ton objectif est de vulgariser un compte rendu médical technique pour le rendre clair, compréhensible et rassurant pour un patient."
        " Le texte provient d’un rapport de {contexte}."
    )

    response = client.chat.completions.create(
        model="gpt-4",
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

st.markdown("Collez un compte rendu **d'endoscopie digestive** ou **d'imagerie médicale**.")

type_cr = st.selectbox("Type de compte rendu :", ["Endoscopie digestive", "Imagerie médicale"])
texte_cr = st.text_area("Compte rendu médical :", height=300)

if st.button("Générer la version vulgarisée"):
    if texte_cr.strip() == "":
        st.warning("Veuillez coller un texte médical.")
    else:
        with st.spinner("⏳ Analyse et vulgarisation en cours..."):
            try:
                resultat = vulgariser_texte(texte_cr, type_cr)
                st.success("✅ Résumé prêt !")
                st.markdown(f"### 🩺 Résultat :\n\n{resultat}")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
