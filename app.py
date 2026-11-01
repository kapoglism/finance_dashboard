#=============================Εισαγωγή βιβλιοθηκών===============================

import streamlit as st
import plotly.express as px
import pandas as pd
import os 


#============================Αρχικοποίηση σταθερών=============================
ARXEIO="pinakas.csv"
KAT_ESODA=[ "Μισθός", "Δώρο", "Πώληση", "Άλλο"]
KAT_EXODA=["Φαγητό", "Ενοίκιο", "Μεταφορές", "Διασκέδαση", "Άλλο"]

#============================Διάβασμα από το αρχείο CSV==================

if "kiniseis" not in st.session_state:
    if os.path.exists(ARXEIO):
        arxeio=pd.read_csv(ARXEIO,keep_default_na=False)
        st.session_state["kiniseis"]=arxeio.to_dict("records")
    else:
        st.session_state["kiniseis"]=[]
        
#==============================Καλωσόρισμα χρήστη=====================

st.title("Τα οικονομικά μου")
st.write("Καλωσήρθατε στην εφαρμογή \"Τα οικονομικά μου\"! Αυτή η εφαρμογή σας βοηθά να παρακολουθείτε τα οικονομικά σας και να διαχειρίζεστε τον προϋπολογισμό σας.")
name = st.text_input("Παρακαλώ δώστε το όνομα σας")
if name: 
    st.write("Γειά σου", name, "! Είμαι εδώ για να σας βοηθήσω να παρακολουθείτε τα οικονομικά σας.")

#=============================Εισαγωγή στοιχείων====================
st.subheader("Νέα κίνηση-Καταχώρηση Εσόδων και Εξόδων")
epil=st.selectbox("Δώστε επιλογή",["Έσοδο", "Έξοδο"])

poso= st.number_input("Δώστε ποσό καταχώρησης", min_value=0.0 )
if epil=="Έσοδο":
    kat=st.selectbox("Δώστε κατηγορία συναλλαγής", KAT_ESODA)
else:
    kat=st.selectbox("Δώστε κατηγορία συναλλαγής", KAT_EXODA)
hm= st.date_input("Δώστε ημερομηνία συναλλαγής", format= "DD/MM/YYYY")
per= st.text_area("Περιγράψτε τη συναλλαγή")


koumpi= st.button("ΠΡΟΣΘΗΚΗ")
if koumpi and poso > 0.0:
    sunal= {
        "ΕΠΙΛΟΓΗ":epil,
        "ΠΟΣΟ":poso,
        "ΚΑΤΗΓΟΡΙΑ": kat,
        "ΗΜΕΡΟΜΗΝΙΑ": hm,
        "ΠΕΡΙΓΡΑΦΗ": per,
    } 
    if sunal["ΠΕΡΙΓΡΑΦΗ"]:
        keimeno= f" Προστέθηκε: {epil}  - {poso:.2f}€  - {kat}-  {hm.strftime("%d/%m/%Y")}- {per}"
    else:
        per="Δεν υπάρχει περιγραφή"
        keimeno= f" Προστέθηκε: {epil}  - {poso:.2f}€  - {kat}-  {hm.strftime("%d/%m/%Y")}-  {per}"
    st.success(keimeno, icon="✅" )
    st.session_state["kiniseis"].append(sunal) 
    pinakas=pd.DataFrame(st.session_state["kiniseis"])
    pinakas.to_csv(ARXEIO,index=False) 
elif koumpi and poso <= 0.0:
    st.error("⚠️ Προσοχή! Προσθέστε έγκυρο ποσό")    
#===============================Διαγραφή εσόδων/εξόδων==========================

etiketes=[]        
k=1 #κρατάω τον αριθμό κ για να ξέρω ποιό στοιχείο να διαγράψω
for i in st.session_state["kiniseis"]:
    etiketes.append(f" Κίνηση: {k}    {i['ΕΠΙΛΟΓΗ']} - {i['ΠΟΣΟ']:.2f}€ - {i['ΚΑΤΗΓΟΡΙΑ']} - {i['ΗΜΕΡΟΜΗΝΙΑ']} - {i['ΠΕΡΙΓΡΑΦΗ']} ")
    k=k+1
if etiketes:
    st.subheader("Διαγραφή εσόδων/εξόδων")
    x=st.selectbox("Επέλεξε έσοδο/έξοδο για διαγραφή", etiketes)
    diagr=st.button("Διαγραφή")
    if diagr:
        pl=0
        j=0
        while j<len(etiketes):
            if x==etiketes[j]:
                pl=j
                break
            j=j+1      
        st.session_state["kiniseis"].pop(pl) 
        st.session_state["minima"]=f"✔️  Διαγράφτηκε η κίνηση με αριθμό: {pl+1}"
       
        pinakas=pd.DataFrame(st.session_state["kiniseis"])
        pinakas.to_csv(ARXEIO, index=False)
        if len(st.session_state["kiniseis"])==0:
            #Διαγράφω τον πίνακα γιατί, όταν διαγράφω την τελευταία κίνηση, το πρόγραμμα θα προσπαθήσει να διαβάσει ένα κενό αρχείο
            os.remove(ARXEIO)     
         # Το κάνω για να ανανεώνει τη σελίδα, ώστε η διαγραμμένη κίνηση να φύγει και από το μενού που βλέπει ο χρήστης χωρίς τη χρήση f5
        st.rerun()   
if "minima" in st.session_state:
    st.success(st.session_state["minima"])    
    del st.session_state["minima"]    
    
#==================================Φίλτρο ανά μηνα=============================================         
st.subheader("Φιλτράρισμα ανά μήνα")
mhnes=["Όλοι","Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"]
mhn=st.selectbox("Επιλέξτε μήνα", mhnes)
ar=mhnes.index(mhn)
lista2=[]
for i in st.session_state["kiniseis"]:             
    y=str(i["ΗΜΕΡΟΜΗΝΙΑ"])
    lista2.append(int(y[5:7]))
metr=0
lista4=[]
for i in st.session_state["kiniseis"]: 
    if ar==0:   #σημαινει οτι η επιλογη ειναι "ολοι"-το εβαλα ξεχωριστα για να παρει ολους τους μηνες
        lista4.append(i) 
    elif ar==lista2[metr]:
        lista4.append(i)        
    metr=metr+1 


#==================================Συνολικά στοιχεία λογαριασμού===============================

es=0
ej=0
yp=0
for i in lista4:
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

if ar!=0:   #η επιλογή αφορά συγκεκριμένο μήνα
    st.write("Τα παρακάτω στοιχεία αφορούν τον μήνα που επιλέξατε")
else:
    st.write("Τα παρακάτω στοιχεία αφορούν όλους τους μήνες")

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
    if ar!=0:   #η επιλογή αφορά συγκεκριμένο μήνα
            st.write("Τα παρακάτω στοιχεία αφορούν τον μήνα που επιλέξατε")
    else:
            st.write("Τα παρακάτω στοιχεία αφορούν όλους τους μήνες")
    st.table(lista4)
else:
    st.write("-Δεν βρέθηκαν κινήσεις")
    
 #=================================== Διάγραμμα πίτας εξόδων======================================

pita={"Φαγητό": 0,              
    "Ενοίκιο": 0,
    "Μεταφορές": 0,
    "Διασκέδαση": 0,
    "Άλλο": 0
}
for i in lista4:
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
    if ar!=0:   #η επιλογή αφορά συγκεκριμένο μήνα
        st.write("Τα παρακάτω στοιχεία αφορούν τον μήνα που επιλέξατε")
    else:
        st.write("Τα παρακάτω στοιχεία αφορούν όλους τους μήνες")
    
    st.write("Στο παρακάτω διάγραμμα πίτας φαίνεται η κατανομή των εξόδων σας στις διάφορες κατηγορίες")
    st.write(pita_px)   
else: 
    st.write("-Το διάγραμμα θα εμφανιστεί μόλις προσθέσετε τα έξοδα σας")
    

#=======================================Πορεία υπολοίπου=======================================================
    
st.subheader("Πορεία υπολοίπου")

zevgaria=[]
hmeromhnies=[]
for i in st.session_state["kiniseis"]:
    zevgaria.append([str(i["ΗΜΕΡΟΜΗΝΙΑ"]),i["ΠΟΣΟ"], i["ΕΠΙΛΟΓΗ"]])
zevgaria.sort()             

yp=0
ypoloipo=[]

for i in zevgaria:
    hmeromhnies.append(i[0])
    if i[2]=="Έσοδο":
        yp=yp+i[1]
        ypoloipo.append(yp)
    else:
        yp=yp-i[1]
        ypoloipo.append(yp)

if hmeromhnies and ypoloipo:
    grafhma=px.line(x=hmeromhnies,y=ypoloipo)
    st.write(grafhma)
else:
    st.write("Το γράφημα πορείας υπολοίπου θα εμφανιστεί μόλις προσθέσετε τις κινήσεις σας")

    
