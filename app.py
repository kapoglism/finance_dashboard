import streamlit as st
import plotly.express as px
import pandas as pd
import os as os

if "kiniseis" not in st.session_state:
    if os.path.exists("pinakas.csv"):
        arxeio=pd.read_csv("pinakas.csv")
        st.session_state["kiniseis"]=arxeio.to_dict("records")
    else:
        st.session_state["kiniseis"]= []


st.title("Τα οικονομικά μου")
st.write("Καλωσήρθατε στην εφαρμογή \"Τα οικονομικά μου\"! Αυτή η εφαρμογή σας βοηθά να παρακολουθείτε τα οικονομικά σας και να διαχειρίζεστε τον προϋπολογισμό σας.")
name = st.text_input("Παρακαλώ δώστε το όνομα σας")
if name: 
    st.write("Γεια σου", name, "! Είμαι εδώ για να σε βοηθήσω να παρακολουθείς τα οικονομικά σου.")


st.subheader("Νέα κίνηση-Καταχώρηση Εσόδων και Εξόδων")
epil=st.selectbox("Δώσε επιλογή",["Έσοδο", "Έξοδο"])


poso= st.number_input("Δώσε ποσό καταχώρησης", min_value=0.0 )  
kat=st.selectbox("Δώσε κατηγορία συναλλαγής", ["Φαγητό", "Ενοίκιο", "Μεταφορές", "Διασκέδαση", "Μισθός", "Άλλο"])
hm= st.date_input("Δώσε ημερομηνία συναλλαγής")
per= st.text_area("Περιέγραψε τη συναλλαγή")

koumpi= st.button("ΠΡΟΣΘΗΚΗ")
if koumpi:
    sunal= {
        "ΕΠΙΛΟΓΗ":epil,
        "ΠΟΣΟ":poso,
        "ΚΑΤΗΓΟΡΙΑ": kat,
        "ΗΜΕΡΟΜΗΝΙΑ": hm,
        "ΠΕΡΙΓΡΑΦΗ": per,
    } 
    if sunal["ΠΕΡΙΓΡΑΦΗ"]:
        keimeno= f" Προστέθηκε: {epil}  - {poso:.2f}€  - {kat}-  {hm.strftime("%d/%m/%y")}- {per}"
    else:
        keimeno= f" Προστέθηκε: {epil}  - {poso:.2f}€  - {kat}-  {hm.strftime("%d/%m/%y")}-  'Δεν υπάρχει περιγραφή'"
    st.success(keimeno, icon="✅" )
    st.session_state["kiniseis"].append(sunal) 
    pinakas=pd.DataFrame(st.session_state["kiniseis"])
    pinakas.to_csv("pinakas.csv",index=False) 
    
    
    
es=0
ej=0
yp=0
for i in st.session_state["kiniseis"]:
    if i["ΕΠΙΛΟΓΗ"]=="Έσοδο":
        es=es+i["ΠΟΣΟ"]
        yp=yp+i["ΠΟΣΟ"]
    else:
        ej=ej+i["ΠΟΣΟ"]
        yp=yp-i["ΠΟΣΟ"]


lej={
    "ΣΥΝ. ΕΣΟΔΑ": f"{es:.2f} €",
    "ΣΥΝ. ΕΞΟΔΑ": f"{ej:.2f} €",
    "ΤΡΕΧ. ΥΠΟΛΟΙΠΟ": f"{yp:.2f} €"
}
st.subheader("Στοιχεία λογαριασμού")


aristera, mesh, dexia= st.columns(3)
with aristera: 
    st.metric("ΣΥΝ. ΕΣΟΔΑ💰",lej["ΣΥΝ. ΕΣΟΔΑ"])
with mesh:
    st.metric("ΣΥΝ. ΕΞΟΔΑ💸",lej["ΣΥΝ. ΕΞΟΔΑ"])
with dexia:
    st.metric("ΤΡΕΧ. ΥΠΟΛΟΙΠΟ🏦",lej["ΤΡΕΧ. ΥΠΟΛΟΙΠΟ"])

if yp<0:
    st.warning("ΠΡΟΣΟΧΉ, ΕΧΕΙΣ ΑΡΝΗΤΙΚΟ ΥΠΟΛΟΙΠΟ", icon="⚠️")

if st.session_state["kiniseis"]:
    st.subheader("Οι κινήσεις μου")
    st.table(st.session_state["kiniseis"])
else:
    st.write("-Δεν βρέθηκαν κινήσεις")

pita={"Φαγητό": 0,               #διαγραμμα πίτας εξόδων
    "Ενοίκιο": 0,
    "Μεταφορές": 0,
    "Διασκέδαση": 0,
    "Άλλο": 0
}

for i in st.session_state["kiniseis"]:
    if i["ΕΠΙΛΟΓΗ"]== "Έξοδο":
        if i["ΚΑΤΗΓΟΡΙΑ"]=="Φαγητό":
            pita["Φαγητό"]=pita["Φαγητό"]+i["ΠΟΣΟ"]
        elif i["ΚΑΤΗΓΟΡΙΑ"]=="Ενοίκιο":
            pita["Ενοίκιο"]=pita["Ενοίκιο"]+i["ΠΟΣΟ"]
        elif i["ΚΑΤΗΓΟΡΙΑ"]=="Μεταφορές":
            pita["Μεταφορές"]=pita["Μεταφορές"]+i["ΠΟΣΟ"]
        elif i["ΚΑΤΗΓΟΡΙΑ"]=="Διασκέδαση":
            pita["Διασκέδαση"]=pita["Διασκέδαση"]+i["ΠΟΣΟ"]
        elif i["ΚΑΤΗΓΟΡΙΑ"]=="Άλλο":
            pita["Άλλο"]=pita["Άλλο"]+i["ΠΟΣΟ"]

onomata=["Φαγητό","Ενοίκιο", "Μεταφορές", "Διασκέδαση","Άλλο"]
times=[pita["Φαγητό"], pita["Ενοίκιο"], pita["Μεταφορές"], pita["Διασκέδαση"], pita["Άλλο"]]
pita_px=px.pie(names=onomata, values=times)

if ej>0:
    st.subheader("Γράφημα εξόδων")
    st.write("Στο παρακάτω διάγραμμα πίτας φαίνεται η κατανομή των εξόδων σας στις διάφορες κατηγορίες")
    st.write(pita_px)   
else: 
    st.write("-Το διάγραμμα θα εμφανιστεί μόλις προσθέσετε τα έξοδα σας")