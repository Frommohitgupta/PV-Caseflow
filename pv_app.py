import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="PV CaseFlow", layout="wide")

# ================= UI STYLING =================
st.markdown("""
<style>

/* HEADER */
.header {
    background: linear-gradient(90deg,#0f172a,#1e293b);
    color:white;
    padding:14px 24px;
    border-radius:10px;
    font-size:18px;
    font-weight:600;
    margin-bottom:12px;
}

/* INPUTS */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
textarea {
    border: 2px solid #9ca3af !important;
    border-radius: 6px !important;
    background-color: #ffffff !important;
}

div[data-baseweb="input"] > div:hover,
div[data-baseweb="select"] > div:hover,
textarea:hover {
    border: 2px solid #2563eb !important;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within,
textarea:focus {
    border: 2px solid #1d4ed8 !important;
    box-shadow: 0 0 0 1px #1d4ed8 !important;
}

/* SECTION CARD */
.section-card {
    background: #f9fafb;
    padding: 16px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

/* BUTTON */
.stButton > button {
    background-color: #1d4ed8;
    color: white;
    border-radius: 6px;
    padding: 6px 14px;
}

/* COMPACT */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="header">PV Operations | Case Processing Module</div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### PV System")
    st.markdown("**Case Workflow**")
    st.markdown("---")
    st.markdown("• Data Entry")
    st.markdown("• Processing")
    st.markdown("• Review")
    st.markdown("• Submission")

# SESSION
for key in ["products","events","concomitant","reporters","saved_cases"]:
    if key not in st.session_state:
        st.session_state[key] = [{}] if key!="saved_cases" else []

# SLA
def calculate_sla(seriousness, ird):
    if seriousness in ["Death","Life-Threatening"]:
        days=7
    elif seriousness in ["Hospitalization","Medically Significant","Congenital Anomaly"]:
        days=15
    else:
        days=30
    due=ird+timedelta(days=days)
    return due, "Overdue" if date.today()>due else "On Time"

# TABS
tab1,tab2,tab3,tab4,tab5 = st.tabs(["General","Patient","Product","Events","Dashboard"])

# ================= GENERAL =================
with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown(f"### Case ID: {st.session_state.get('case_id','New Case')}")
    c1,c2=st.columns(2)

    with c1:
        case_id=st.text_input("Case ID",key="case_id")
        report_type=st.selectbox("Report Type",["Spontaneous","Non-interventional Study","Literature Spontaneous"])
        case_status=st.selectbox("Case Status",["New","In Progress","QC","Closed"])

    with c2:
        country=st.text_input("Country")
        ird=st.date_input("Initial Receipt Date",value=date.today())

    st.markdown("#### Reporter")

    if st.button("Add Reporter"):
        st.session_state.reporters.append({})

    reporters_data=[]
    for i in range(len(st.session_state.reporters)):
        c1,c2=st.columns(2)
        with c1:
            st.text_input(f"Name {i}",key=f"r_name{i}")
            st.text_input(f"Address {i}",key=f"r_addr{i}")
            st.text_input(f"City {i}",key=f"r_city{i}")
            st.text_input(f"State {i}",key=f"r_state{i}")
        with c2:
            country_r=st.text_input(f"Country {i}",key=f"r_country{i}")
            st.text_input(f"Postal Code {i}",key=f"r_post{i}")
            st.text_input(f"Phone {i}",key=f"r_phone{i}")
            st.text_input(f"Email {i}",key=f"r_email{i}")
            occ=st.selectbox(f"Occupation {i}",["Consumer","HCP","Physician","Nurse"],key=f"r_occ{i}")

        reporters_data.append({"country":country_r,"occupation":occ})

    st.markdown('</div>', unsafe_allow_html=True)

# ================= PATIENT =================
with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    sub1,sub2=st.tabs(["Details","Medical History"])

    with sub1:
        c1,c2=st.columns(2)
        with c1:
            patient_name=st.text_input("Patient Name")
            age=st.number_input("Age",min_value=0)
        with c2:
            gender=st.selectbox("Gender",["Male","Female","Other"])

    with sub2:
        medical_history=st.text_area("Medical History")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= PRODUCT =================
with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    sub1,sub2=st.tabs(["Suspect Drug","Concomitant"])

    with sub1:
        if st.button("Add Product"):
            st.session_state.products.append({})
        products_data=[]
        for i in range(len(st.session_state.products)):
            c1,c2,c3=st.columns(3)
            with c1:
                name=st.text_input(f"Drug {i}",key=f"p{i}")
            with c2:
                dose=st.text_input(f"Dose {i}",key=f"d{i}")
                unit=st.selectbox(f"Unit {i}",["mg","mcg","g","DF"],key=f"u{i}")
            with c3:
                freq=st.selectbox(f"Frequency {i}",["Once daily","Twice daily","Weekly","Other"],key=f"f{i}")
                action=st.selectbox(f"Action {i}",["Dose Increased","Dose Decreased","Stopped","Unknown"],key=f"a{i}")
            sd=st.date_input(f"Start Date {i}",key=f"sd{i}")
            ed=st.date_input(f"Stop Date {i}",key=f"ed{i}")
            products_data.append({"name":name,"dose":dose,"unit":unit,"freq":freq,"action":action,"start":sd,"stop":ed})

    with sub2:
        if st.button("Add Concomitant"):
            st.session_state.concomitant.append({})
        concomitant_data=[]
        for i in range(len(st.session_state.concomitant)):
            c1,c2=st.columns(2)
            with c1:
                name=st.text_input(f"Con Drug {i}",key=f"c{i}")
            with c2:
                dose=st.text_input(f"Con Dose {i}",key=f"cd{i}")
                unit=st.selectbox(f"Unit {i}",["mg","mcg","g","DF"],key=f"cu{i}")
            freq=st.selectbox(f"Frequency {i}",["Once daily","Twice daily","Weekly","Other"],key=f"cf{i}")
            concomitant_data.append({"name":name,"dose":dose,"unit":unit,"freq":freq})

    st.markdown('</div>', unsafe_allow_html=True)

# ================= EVENTS =================
with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    sub1,sub2=st.tabs(["Event Entry","Narrative"])

    with sub1:
        if st.button("Add Event"):
            st.session_state.events.append({})

        events_data=[]
        for i in range(len(st.session_state.events)):
            event=st.text_input(f"Event {i}",key=f"e{i}")
            c1,c2=st.columns(2)
            with c1:
                event_start=st.date_input(f"Event Start Date {i}",key=f"es{i}",value=None)
            with c2:
                event_stop=st.date_input(f"Event Stop Date {i}",key=f"ee{i}",value=None)

            seriousness=st.selectbox(f"Seriousness {i}",
                ["Death","Life-Threatening","Hospitalization","Medically Significant","Congenital Anomaly","Non-serious"],
                key=f"s{i}")

            outcome=st.selectbox(f"Outcome {i}",
                ["Recovered","Not Recovered","Fatal","Unknown"],key=f"o{i}")

            events_data.append({"event":event,"seriousness":seriousness,"outcome":outcome,"start":event_start,"stop":event_stop})

    with sub2:
        case_id=st.session_state.get("case_id","")

        if st.button("🚀 Process Case"):

            if not case_id:
                st.error("Case ID is required")
                st.stop()

            seriousness_value=events_data[0]["seriousness"] if events_data else "Non-serious"
            due_date,sla_status=calculate_sla(seriousness_value,ird)

            reporter_occ=reporters_data[0]["occupation"] if reporters_data else "reporter"
            reporter_country=reporters_data[0]["country"] if reporters_data else ""

            patient_info=f"{age}-year-old {gender.lower()}" if age else "patient"

            narrative=f"This {report_type.lower()} report received from a {reporter_occ.lower()}"
            if reporter_country:
                narrative+=f" from {reporter_country}"
            narrative+=f" concerns a {patient_info}. "

            for p in products_data:
                if p["name"]:
                    start=p["start"].strftime("%d%b%Y") if p["start"] else "an unknown date"
                    stop=p["stop"].strftime("%d%b%Y") if p["stop"] else None
                    narrative+=f"Patient received {p['name']} {p['dose']} {p['unit']} {p['freq']} starting on {start}. "
                    if stop:
                        narrative+=f"The drug was stopped on {stop}. "

            for e in events_data:
                if e["event"]:
                    start=e["start"].strftime("%d%b%Y") if e["start"] else "an unknown date"
                    stop=e["stop"].strftime("%d%b%Y") if e["stop"] else None
                    narrative+=f"On {start}, the patient experienced {e['event']} ({e['seriousness']}). "
                    if stop:
                        narrative+=f"The event resolved on {stop}. "

            for p in products_data:
                if p["name"]:
                    narrative+=f"Action taken with {p['name']} was {p['action'].lower()}. "

            outcome=events_data[0]["outcome"] if events_data else "Unknown"
            narrative+=f"Outcome: {outcome}."

            st.success("Processed")
            edited=st.text_area("Narrative",value=narrative,height=200)

            record={"Case ID":case_id,"Patient":patient_name,"Seriousness":seriousness_value,
                    "Status":case_status,"SLA Status":sla_status,"Due Date":due_date,
                    "Country":country,"Narrative":edited}

            updated=False
            for i,c in enumerate(st.session_state.saved_cases):
                if c["Case ID"]==case_id:
                    st.session_state.saved_cases[i]=record
                    updated=True

            if not updated:
                st.session_state.saved_cases.append(record)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= DASHBOARD =================
with tab5:
    if st.session_state.saved_cases:
        df=pd.DataFrame(st.session_state.saved_cases)
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Total",len(df))
        c2.metric("Serious",len(df[df["Seriousness"]!="Non-serious"]))
        c3.metric("Overdue",len(df[df["SLA Status"]=="Overdue"]))
        c4.metric("Closed",len(df[df["Status"]=="Closed"]))
        st.dataframe(df,use_container_width=True,height=450)
    else:
        st.info("No cases yet")
