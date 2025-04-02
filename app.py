# Importing Our Classes
from Person import *
from Doctor import *
from Nurse import *
from Patient import *
from Operation import *
from Hospital import *


# Importing Libraries
import pandas as pd
import numpy as np
import os
from PIL import Image
from time import sleep
import datetime


import pandas as pd
import numpy as np
import streamlit as st
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu
import warnings

import pickle
import os

# Load models from saved files
working_dir = os.path.dirname(os.path.abspath(__file__))
diabetes_model = pickle.load(open(f'{working_dir}/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open(f'{working_dir}/parkinsons_model.sav', 'rb'))


st.set_page_config(
    page_title="Hospita App",
    page_icon="👨‍⚕️",
    layout="wide"
)

warnings.simplefilter(action='ignore', category=FutureWarning)

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False


def callback():
    st.session_state.button_clicked = True


hospital = Hospital("Salama", "Assiut")

st.markdown(
    """
    <style>
         .main {
            text-align: center; 
         }

         div.block-containers{
            padding-top: 0.5rem
         }

         .st-emotion-cache-z5fcl4{
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 2.8rem;
            overflow-x: hidden;
         }

         .st-emotion-cache-16txtl3{
            padding: 2.7rem 0.6rem
         }
         div.st-emotion-cache-1r6slb0{
            padding: 15px 5px;
            background-color: #111;  
            border-radius: 5px;
            border: 3px solid #5E0303;
            opacity: 0.9;
         }
        div.st-emotion-cache-1r6slb0:hover{
            transition: all 0.5s ease-in-out;
            background-color: #000;  
            border: 3px solid red;
            opacity: 1;
         }

         .plot-container.plotly{
            border: 4px solid #333;
            border-radius: 7px;
         }

         div.st-emotion-cache-1r6slb0 span.st-emotion-cache-10trblm{
            font: bold 24px tahoma;
         }
         div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)


sub_options_style = styles = {
    "container": {"padding": "8!important", "background-color": '#101010', "border": "2px solid darkcyan"},
    "nav-link": {"color": "white", "padding": "10px", "font-size": "15px", "text-align": "center", "margin": "10px 0px", },
    "nav-link-selected": {"background-color": "#0CB9B9"},

}


@st.cache_data
def is_valid_first_name(fname):
    return len(fname) > 3 and (fname != "")


@st.cache_data
def is_valid_last_name(lname):
    return len(lname) > 3 and (lname != "")


@st.cache_data
def is_valid_full_name(fullname):
    return len(fullname) > 6 and (fullname != "") and fullname.__contains__(" ")


@st.cache_data
def is_valid_age(age):
    if age.isnumeric():
        if (int(age) >= 18) and (int(age) <= 90):
            return True
        return False
    return False


@st.cache_data
def is_valid_phone(phone):
    if (len(phone) <= 13) and (phone[0:3] in ["010", "011", "012", "015", "+91"]):
        return True
    return False


@st.cache_data
def is_valid_patient_id(patient_id):
    if patient_id.startswith("PID_"):
        return True
    return False


@st.cache_data
def is_valid_operation_name(operation_name):
    return len(operation_name) > 5 and (operation_name != "")


header = st.container()
content = st.container()

with st.sidebar:
    st.title("EHRM Hospital")
    page = option_menu(
        menu_title='Menu',
        options=['Doctor', "Nurse", "Patient", "Operation"],
        menu_icon='chat-text-fill',
        default_index=0,
        styles={
            "container": {"padding": "10!important", "background-color": '#000'},
            "icon": {"color": "white", "font-size": "22px"},
            "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin": "0px", },
            "nav-link-selected": {"background-color": "#0CB9B9"},

        }

    )
    st.write("***")

    # Doctor Page
    if page == 'Doctor':
        with header:
            st.title('Doctors 👨‍⚕️')
            doctor_option = option_menu(menu_title=None, options=["Add Doctor", 'Add Existing Nurse', 'Add Patient', "Doctors Info"],
                                        icons=[" "]*4, menu_icon="cast", default_index=0,
                                        orientation="horizontal", styles=sub_options_style)

        with content:
            if doctor_option == "Add Doctor":
                st.text(f'Adding New Doctor'.title())
                with st.form('input'):
                    [c1, c2] = st.columns(2)
                    with c1:
                        first_name = st.text_input(
                            label="First Name", placeholder="Aditya").strip()

                        age = st.text_input(
                            label="Age", placeholder=23, max_chars=2).strip()

                        specialization = st.text_input(
                            label="Specialization", placeholder="Dermatology").strip()

                    with c2:
                        last_name = st.text_input(
                            label="Last Name", placeholder="Ardak").strip()

                        phone = st.text_input(
                            label="Phone Number", placeholder="9890377972", max_chars=11).strip()

                        st.write(
                            '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)

                        gender = st.radio(
                            "Gender",
                            ["Male", "Female"],

                        )

                    add_doctor = st.form_submit_button(label='Add Doctor')
                    save_doctor = st.form_submit_button(label='Save Doctors')

                    if add_doctor:
                        # Get The Output of Validation
                        flag_fname = is_valid_first_name(first_name)
                        flag_lname = is_valid_last_name(last_name)
                        flag_age = is_valid_age(age)
                        flag_phone = is_valid_phone(phone)

                        if flag_fname == False:
                            st.warning(
                                'First Name Must Be Greater Than 3 Characters!!')

                        if flag_lname == False:
                            st.warning(
                                'Last Name Must Be Greater Than 3 Characters!!')

                        if flag_age == False:
                            st.warning(
                                'Please Enter a Valid Age, Must Be A Numerical Value!!')

                        if flag_phone == False:
                            st.warning(
                                'Please Enter a Valid Phone Number Starts With [010/ 012/ 015/ 011]!')

                        if flag_fname and flag_lname and flag_age and flag_phone:
                            # Create Instance of Doctor Class
                            the_doctor = Doctor(
                                f"{first_name} {last_name}", age, gender, f"'{phone}'", specialization)

                            with st.spinner(text='Adding User…'):
                                sleep(1)
                                if hospital.add_doctor(the_doctor) == False:
                                    st.warning(
                                        f'This Doctor With Phone Number ({phone}) Already Existed Before!!.')
                                else:
                                    st.success(
                                        f'The Doctor With Name {first_name} {last_name}, Added Successfully.')

                        else:
                            st.error(
                                'Can Not Add This Doctor :x:.\nPlease, Check All Input Fields')

                    elif save_doctor:
                        with st.spinner(text='Saving All Doctors...'):
                            sleep(1)
                            if hospital.save_doctor() == 0:
                                st.info(
                                    'You Have To Add Doctor First In Correct Way, Then Save The Doctor Info.')
                            else:
                                st.success(
                                    'Doctor(s) Saved Successfully :white_check_mark:')

            if doctor_option == "Add Existing Nurse":
                st.text(F"Adding Nurse To Doctor's Team".title())
                st.info(
                    "Be sure that the nurse or doctor must be in the hospital already!!")
                with st.form('adding_existing_nurse'):

                    col_1, col_2 = st.columns(2)
                    with col_1:
                        doctor_name = st.text_input(
                            label="Doctor Name", placeholder="Aditya Ardak").strip()

                        st.write("***")

                        nurse_name = st.text_input(
                            label="Nurse Name", placeholder="Shravani").strip()

                    with col_2:
                        doctor_phone = st.text_input(
                            label="Doctor Phone", placeholder="01020487XXX", max_chars=11).strip()

                        st.write("***")

                        nurse_phone = st.text_input(
                            label="Nurse Phone", placeholder="01520487XXX", max_chars=11).strip()

                    add_nurse_to_team = st.form_submit_button(
                        label='Add Nurse To The Team')

                    if add_nurse_to_team:
                        # Get The Output of Validation
                        flag_doctor_name = is_valid_full_name(doctor_name)
                        flag_doctor_phone = is_valid_phone(doctor_phone)

                        flag_nurse_name = is_valid_full_name(nurse_name)
                        flag_nurse_phone = is_valid_phone(nurse_phone)

                        if flag_doctor_name == False:
                            st.warning(
                                'Please Enter Right Doctor Name')

                        if flag_doctor_phone == False:
                            st.warning(
                                'Please Enter a Valid Phone Number!!')

                        if flag_nurse_name == False:
                            st.warning(
                                'Please Enter Right Nurse Name')

                        if flag_nurse_phone == False:
                            st.warning(
                                'Please Enter a Valid Phone Number!!')

                        if flag_doctor_name and flag_doctor_phone and flag_nurse_name and flag_nurse_phone:
                            # Create Empty Instance of Doctor Class
                            temp_doctor = Doctor.empty_Doctor_constructor()

                            with st.spinner(text='Adding Nurse To The Team…'):
                                sleep(1)
                                adding_nurse = temp_doctor.add_nurse_to_team(
                                    doctor_name, doctor_phone, nurse_name, nurse_phone)
                                if adding_nurse == False:
                                    st.error(
                                        f"Can Not Add This Nurse to {doctor_name}\'s Team :x:.\nPlease, Check All Input Fields")
                                    st.warning(
                                        f"Ensure That!!  Doctor Phone Number belongs to Doctor {doctor_name}\n\
                                            And The Nurse Phone Number belongs to Nurse {nurse_name}")
                                elif adding_nurse == -1:
                                    st.warning(
                                        f"Nurse ({nurse_name}) Already Existed In {doctor_name}'s Team.")
                                else:
                                    st.success(
                                        f"Nurse ({nurse_name}) Added To {doctor_name}'s Team.")

                        else:
                            st.error(
                                'The Operation Corrupted :x:.\nPlease, Check All Input Fields')

            if doctor_option == "Add Patient":
                st.text(F"Adding Patients To Doctor's List".title())
                st.info(
                    "Be sure that the Patient or Doctor Must Be in the hospital already!!")
                if len(hospital.get_all_doctors()) > 0 and len(hospital.get_all_patients()) > 0:
                    with st.form('adding_existing_patient'):
                        col_1, col_2 = st.columns(2)
                        with col_1:
                            doctor_name = st.selectbox(
                                "Select Doctor Name:", options=(hospital.get_all_doctors()["Name"].tolist())).strip()

                            st.write("***")

                            patient_name = st.selectbox(
                                "Select Patient Name:", options=(hospital.get_all_patients()["Name"].tolist())).strip()

                        with col_2:
                            doctor_phone = st.text_input(
                                label="Doctor Phone", placeholder="01020487XXX", max_chars=11).strip()

                            st.write("***")
                            patient_id = st.selectbox("Select Patient ID:", options=(
                                hospital.get_all_patients()["Patient_ID"].tolist())).strip()

                        add_patient_to_doctor = st.form_submit_button(
                            label='Add Patient To The Doctor')

                        if add_patient_to_doctor:
                            # Get The Output of Validation
                            flag_doctor_name = is_valid_full_name(doctor_name)
                            flag_doctor_phone = is_valid_phone(doctor_phone)

                            flag_patient_name = is_valid_full_name(
                                patient_name)

                            if flag_doctor_name == False:
                                st.warning(
                                    'Please Enter Right Doctor Name')

                            if flag_doctor_phone == False:
                                st.warning(
                                    'Please Enter a Valid Phone Number!!')

                            if flag_patient_name == False:
                                st.warning(
                                    'Please Enter Right Patient Name')

                            if flag_doctor_name and flag_doctor_phone and flag_patient_name:
                                # Create Empty Instance of Doctor Class
                                temp_doctor = Doctor.empty_Doctor_constructor()

                                with st.spinner(text='Adding Nurse To The Team…'):
                                    sleep(1)
                                    adding_patient = temp_doctor.add_patient_to_doctor(
                                        doctor_name, doctor_phone, patient_id, patient_name)
                                    if adding_patient == False:
                                        st.error(
                                            f"Can Not Add This Patient to {doctor_name}\'s List :x:.\nPlease, Check All Input Fields")
                                        st.warning(
                                            f"Ensure That!! Doctor Phone Number belongs to Doctor {doctor_name}\n\
                                                And The Patient ID belongs to {patient_name}")
                                    elif adding_patient == -1:
                                        st.warning(
                                            f"Patient ({patient_name}) Already Existed In {doctor_name}'s List.")
                                    else:
                                        st.success(
                                            f"Patient ({patient_name}) Added To {doctor_name}'s List.")

                            else:
                                st.error(
                                    'The Operation Corrupted :x:.\nPlease, Check All Input Fields')

                else:
                    st.warning(
                        "Please You Have To Add Doctors & Patients First To Hospital!!!")
            if doctor_option == "Doctors Info":
                st.text(
                    f'All Doctors in "{hospital.name} Hospital" 🏥'.title())

                df = hospital.get_all_doctors()

                st.table(df)

    # Nurse Page
    elif page == 'Nurse':
        with header:
            st.title('Nurses 👩‍⚕️'.title())

            nurse_option = option_menu(menu_title=None,
                                       options=["Add Nurse", 'Nurses Info'],
                                       icons=[" "]*2,
                                       default_index=0, orientation="horizontal", styles=sub_options_style)

        with content:
            if nurse_option == "Add Nurse":
                st.text(f'Adding New Nurse'.title())
                with st.form("Adding_New_Nurse"):
                    [c1, c2] = st.columns(2)
                    with c1:
                        first_name = st.text_input(
                            label="First Name", placeholder="Shravani").strip()

                        age = st.text_input(
                            label="Age", placeholder=35, max_chars=2).strip()

                        shift_type = st.text_input(
                            label="Shift Type", placeholder="Night Shift").strip()

                    with c2:
                        last_name = st.text_input(
                            label="Last Name", placeholder="Aditya").strip()

                        phone = st.text_input(
                            label="Phone Number", placeholder="0157896xxxx", max_chars=11).strip()

                        st.write(
                            '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)

                        gender = st.radio(
                            "Gender",
                            ["Male", "Female"],

                        )

                    add_nurse = st.form_submit_button(label='Add Nurse')
                    save_nurse = st.form_submit_button(label='Save Nurse')

                    if add_nurse:
                        # Get The Output of Validation
                        flag_fname = is_valid_first_name(first_name)
                        flag_lname = is_valid_last_name(last_name)
                        flag_age = is_valid_age(age)
                        flag_phone = is_valid_phone(phone)

                        if flag_fname == False:
                            st.warning(
                                'First Name Must Be Greater Than 3 Characters!!')

                        if flag_lname == False:
                            st.warning(
                                'Last Name Must Be Greater Than 3 Characters!!')

                        if flag_age == False:
                            st.warning(
                                'Please Enter a Valid Age, Must Be A Numerical Value!!')

                        if flag_phone == False:
                            st.warning(
                                'Please Enter a Valid Phone Number Starts With [010/ 012/ 015/ 011]!')

                        if flag_fname and flag_lname and flag_age and flag_phone:
                            # Create Instance of Doctor Class
                            the_nurse = Nurse(
                                f"{first_name} {last_name}", age, gender, f"'{phone}'", shift_type)

                            with st.spinner(text='Adding Nurse....'):
                                sleep(1)
                                if hospital.add_nurse(the_nurse) == False:
                                    st.warning(
                                        f'This Nurse With Phone Number ({phone}) Already Existed Before!!.')
                                else:
                                    st.success(
                                        f'The Nurse With Name {first_name} {last_name}, Added Successfully.')
                        else:
                            st.error(
                                'Can Not Add This Nurse :x:.\nPlease, Check All Input Fields')

                    elif save_nurse:
                        with st.spinner(text='Saving All Nurses...'):
                            sleep(1)
                            if hospital.save_nurse() == 0:
                                st.info(
                                    'You Have To Add Nurse First In Correct Way, Then Save The Nurse Info.')
                            else:
                                st.success(
                                    'Nurse(s) Saved Successfully :white_check_mark:')

            if nurse_option == "Nurses Info":
                st.text(
                    f'All Nurses in "{hospital.name} Hospital" 🏥'.title())

                df = hospital.get_all_nurses()

                st.table(df)

    # Patient Page
    elif page == "Patient":
        with header:
            st.title('Patients 🤒'.title())

            patient_option = option_menu(menu_title=None,
                                         options=["Add Patient",
                                                  'Assigning to Doctor',
                                                  'Patients Info'],
                                         icons=[" "]*3,
                                         default_index=0, orientation="horizontal", styles=sub_options_style)

        with content:
            if patient_option == "Add Patient":
                st.text(f'Adding New Patient'.title())
                with st.form("Adding_New_patient"):
                    [c1, c2] = st.columns(2)
                    with c1:
                        first_name = st.text_input(
                            label="First Name", placeholder="Dexter").strip()

                        age = st.text_input(
                            label="Age", placeholder=35, max_chars=2).strip()

                    with c2:
                        last_name = st.text_input(
                            label="Last Name", placeholder="Morgan").strip()

                        phone = st.text_input(
                            label="Phone Number", placeholder="0117896xxxx", max_chars=11).strip()
                    st.write(
                        '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: left;} </style>', unsafe_allow_html=True)

                    gender = st.selectbox(
                        "Gender",
                        ["Male", "Female"],)

                    add_patient = st.form_submit_button(label='Add Patient')
                    save_patient = st.form_submit_button(label='Save Patient')

                    if add_patient:
                        # Get The Output of Validation
                        flag_fname = is_valid_first_name(first_name)
                        flag_lname = is_valid_last_name(last_name)
                        flag_age = is_valid_age(age)
                        flag_phone = is_valid_phone(phone)

                        if flag_fname == False:
                            st.warning(
                                'First Name Must Be Greater Than 3 Characters!!')

                        if flag_lname == False:
                            st.warning(
                                'Last Name Must Be Greater Than 3 Characters!!')

                        if flag_age == False:
                            st.warning(
                                'Please Enter a Valid Age, Must Be A Numerical Value!!')

                        if flag_phone == False:
                            st.warning(
                                'Please Enter a Valid Phone Number Starts With [010/ 012/ 015/ 011/091/0]!')

                        if flag_fname and flag_lname and flag_age and flag_phone:
                            # Create Instance of Doctor Class
                            the_patient = Patient(
                                f"{first_name} {last_name}", age, gender, f"'{phone}'")

                            with st.spinner(text='Adding Patient....'):
                                sleep(1)
                                if hospital.add_patient(the_patient) == False:
                                    st.warning(
                                        f'This Patient With Phone Number ({phone}) Already Existed Before!!.')
                                else:
                                    st.success(
                                        f'The Patient With Name {first_name} {last_name}, Added Successfully.')
                                    st.success(
                                        f'Patient ID {the_patient.get_patient_id()}')
                        else:
                            st.error(
                                'Can Not Add This Nurse :x:.\nPlease, Check All Input Fields')

                    elif save_patient:
                        with st.spinner(text='Saving All Nurses...'):
                            sleep(1)
                            if hospital.save_patient() == 0:
                                st.info(
                                    'You Have To Add Patient Data In Correct Way, Then Save The Nurse Info.')
                            else:
                                st.success(
                                    'Patient(s) Saved Successfully :white_check_mark:')

            if patient_option == "Assigning to Doctor":
                if len(hospital.get_all_doctors()) > 0 and len(hospital.get_all_patients()) > 0:
                    st.text(F'Assigning To Doctor'.title())

                    with st.form('assign_patient_to_dr'):
                        patient_id = st.selectbox("Select Patient ID:", options=(
                            hospital.get_all_patients()["Patient_ID"].tolist())).strip()
                        st.write("***")
                        c1, c2 = st.columns(2)
                        with c1:

                            doctor_name = st.selectbox(
                                "Select Doctor Name:", options=(hospital.get_all_doctors()["Name"].tolist())).strip()

                        with c2:
                            doctor_phone = st.text_input(
                                label="Doctor Phone", placeholder="01020487XXX", max_chars=11).strip()

                        assign_doctor = st.form_submit_button(
                            label='Assign Patient to Doctor')

                        if assign_doctor:
                            flag_doctor_name = is_valid_full_name(doctor_name)

                            if flag_doctor_name == False:
                                st.warning(
                                    'Choose Doctor From List !..')

                            if flag_doctor_name:
                                with st.spinner(text='Deleting The Book…'):
                                    # Get Patient Name
                                    patient_df = hospital.get_all_patients()
                                    filt = (
                                        patient_df["Patient_ID"] == patient_id)
                                    patient_name = patient_df.loc[filt]["Name"].values[0]

                                    temp_patient = Patient.empty_patient_constructor()

                                    assigning_doctor = temp_patient.assign_doctor_to_pateint(
                                        doctor_name, doctor_phone, patient_id, patient_name)

                                    sleep(1)
                                    if assigning_doctor == False:
                                        st.error(
                                            f"Can Not Assigning Doctor ({doctor_name}) to Patirnt ({patient_id}):x:.\nPlease, Check All Input Fields")
                                        st.warning(
                                            f"Ensure That!! Doctor Phone Number belongs to Doctor {doctor_name}\n\
                                                    And The Patient ID {patient_id}")
                                    elif assigning_doctor == -1:
                                        st.warning(
                                            f"Patient ({patient_id}) Already Existed In {doctor_name}'s List.")
                                    else:
                                        st.success(
                                            f"Patient ({patient_id}) Added To {doctor_name}'s List.")
                else:
                    st.warning(
                        "Please Add Doctors & Patients First To Hospital!!\nIn Order To Assigning Doctors")
            if patient_option == "Patients Info":
                st.text(
                    f'All Patients in "{hospital.name} Hospital" 🏥'.title())

                df = hospital.get_all_patients()

                st.table(df)

    # Operation Page

    # Paste this modified code inside your 'Operation' menu of App 1




    elif page == "Operation":

        with header:
            st.title('Operations 💉🩺')
            operation_option = option_menu(menu_title=None,
                                        options=["Add Operation",
                                                    'All Operations',
                                                    'Predict Disease'],
                                        icons=[" "]*3,
                                        default_index=0, orientation="horizontal", styles=sub_options_style)

        with content:
            temp_operation = Operation.empty_operation_constructor()

            if operation_option == "Add Operation":
                # Existing Add Operation code remains unchanged
                pass

            elif operation_option == "All Operations":
                # Existing All Operations code remains unchanged
                pass

            elif operation_option == 'Predict Disease':
                disease_selected = st.selectbox('Select Disease to Predict:', ['Diabetes', 'Heart Disease', 'Parkinsons'])

                if disease_selected == 'Diabetes':
                    st.header('Diabetes Prediction')

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        Pregnancies = st.text_input('Number of Pregnancies', value="3.85")
                        SkinThickness = st.text_input('Skin Thickness value', value="20.54")
                        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value', value="0.47")
                    with col2:
                        Glucose = st.text_input('Glucose Level', value="120.89")
                        Insulin = st.text_input('Insulin Level', value="79.80")
                        Age = st.text_input('Age of the Person', value="33.24")
                    with col3:
                        BloodPressure = st.text_input('Blood Pressure value', value="69.11")
                        BMI = st.text_input('BMI value', value="31.99")

                    if st.button('Predict Diabetes'):
                        user_input = [float(x) for x in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]]
                        diab_prediction = diabetes_model.predict([user_input])
                        result = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
                        st.success(result)

                elif disease_selected == 'Heart Disease':
                    st.header('Heart Disease Prediction')

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        age = st.text_input('Age', value="54.37")
                        trestbps = st.text_input('Resting Blood Pressure', value="131.69")
                        restecg = st.text_input('Resting ECG results', value="0.53")
                        oldpeak = st.text_input('ST Depression', value="1.04")
                        thal = st.text_input('Thalassemia status', value="2.31")
                    with col2:
                        sex = st.text_input('Sex', value="0.68")
                        chol = st.text_input('Serum Cholesterol', value="246.26")
                        thalach = st.text_input('Max Heart Rate', value="149.65")
                        slope = st.text_input('Slope of ST Segment', value="1.40")
                    with col3:
                        cp = st.text_input('Chest Pain types', value="0.97")
                        fbs = st.text_input('Fasting Blood Sugar >120 mg/dl', value="0.15")
                        exang = st.text_input('Exercise Induced Angina', value="0.33")
                        ca = st.text_input('Major vessels colored', value="0.73")

                    if st.button('Predict Heart Disease'):
                        user_input = [float(x) for x in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
                        heart_prediction = heart_disease_model.predict([user_input])
                        result = 'The person has heart disease' if heart_prediction[0] == 1 else 'The person does not have heart disease'
                        st.success(result)

                elif disease_selected == 'Parkinsons':
                    st.header("Parkinson's Prediction")

                    default_values = [145.75, 179.94, 107.34, 0.00622, 0.00006, 0.00314, 0.00391, 0.00941, 0.03027, 0.28224,
                                    0.01300, 0.01574, 0.01791, 0.03899, 0.02217, 22.00, 0.46, 0.72, -5.55, 0.23, 2.38, 0.21]

                    labels = ['MDVP: Fo (Hz)', 'MDVP: Fhi (Hz)', 'MDVP: Flo (Hz)', 'MDVP: Jitter (%)', 'MDVP: Jitter (Abs)',
                            'MDVP: RAP', 'MDVP: PPQ', 'Jitter: DDP', 'MDVP: Shimmer', 'MDVP: Shimmer (dB)',
                            'Shimmer: APQ3', 'Shimmer: APQ5', 'MDVP: APQ', 'Shimmer: DDA', 'NHR', 'HNR', 'RPDE', 'DFA',
                            'Spread1', 'Spread2', 'D2', 'PPE']

                    inputs = []
                    cols = st.columns(5)
                    for i, label in enumerate(labels):
                        inputs.append(cols[i % 5].text_input(label, value=str(default_values[i])))

                    if st.button("Predict Parkinson's"):
                        user_input = [float(x) for x in inputs]
                        parkinsons_prediction = parkinsons_model.predict([user_input])
                        result = "The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "The person does not have Parkinson's disease"
                        st.success(result)