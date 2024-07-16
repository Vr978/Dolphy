from flask import Flask, request, render_template
from flask_cors import CORS
from flask_cors import CORS, cross_origin
import requests
import pandas as pd
import google.generativeai as genai
import jsonify
from IPython.display import Markdown,display

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"






df = pd.read_csv('/Users/vrajchaudhari/Desktop/Dolphy/dolphy/Training.csv')
unique_diseases = df['prognosis'].unique()
disease_dict = {index: disease for index, disease in enumerate(unique_diseases)}

GOOGLE_API_KEY = 'AIzaSyBB0D8alzICGChXB62i8B68UqwlKrIiOh4'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

symptoms_dict = {
    "itching": 0,
    "skin_rash": 0,
    "nodal_skin_eruptions": 0,
    "continuous_sneezing": 0,
    "shivering": 0,
    "chills": 0,
    "joint_pain": 0,
    "stomach_pain": 0,
    "acidity": 0,
    "ulcers_on_tongue": 0,
    "muscle_wasting": 0,
    "vomiting": 0,
    "burning_micturition": 0,
    "spotting_urination": 0,
    "fatigue": 0,
    "weight_gain": 0,
    "anxiety": 0,
    "cold_hands_and_feets": 0,
    "mood_swings": 0,
    "weight_loss": 0,
    "restlessness": 0,
    "lethargy": 0,
    "patches_in_throat": 0,
    "irregular_sugar_level": 0,
    "cough": 0,
    "high_fever": 0,
    "sunken_eyes": 0,
    "breathlessness": 0,
    "sweating": 0,
    "dehydration": 0,
    "indigestion": 0,
    "headache": 0,
    "yellowish_skin": 0,
    "dark_urine": 0,
    "nausea": 0,
    "loss_of_appetite": 0,
    "pain_behind_the_eyes": 0,
    "back_pain": 0,
    "constipation": 0,
    "abdominal_pain": 0,
    "diarrhoea": 0,
    "mild_fever": 0,
    "yellow_urine": 0,
    "yellowing_of_eyes": 0,
    "acute_liver_failure": 0,
    "fluid_overload": 0,
    "swelling_of_stomach": 0,
    "swelled_lymph_nodes": 0,
    "malaise": 0,
    "blurred_and_distorted_vision": 0,
    "phlegm": 0,
    "throat_irritation": 0,
    "redness_of_eyes": 0,
    "sinus_pressure": 0,
    "runny_nose": 0,
    "congestion": 0,
    "chest_pain": 0,
    "weakness_in_limbs": 0,
    "fast_heart_rate": 0,
    "pain_during_bowel_movements": 0,
    "pain_in_anal_region": 0,
    "bloody_stool": 0,
    "irritation_in_anus": 0,
    "neck_pain": 0,
    "dizziness": 0,
    "cramps": 0,
    "bruising": 0,
    "obesity": 0,
    "swollen_legs": 0,
    "swollen_blood_vessels": 0,
    "puffy_face_and_eyes": 0,
    "enlarged_thyroid": 0,
    "brittle_nails": 0,
    "swollen_extremeties": 0,
    "excessive_hunger": 0,
    "extra_marital_contacts": 0,
    "drying_and_tingling_lips": 0,
    "slurred_speech": 0,
    "knee_pain": 0,
    "hip_joint_pain": 0,
    "muscle_weakness": 0,
    "stiff_neck": 0,
    "swelling_joints": 0,
    "movement_stiffness": 0,
    "spinning_movements": 0,
    "loss_of_balance": 0,
    "unsteadiness": 0,
    "weakness_of_one_body_side": 0,
    "loss_of_smell": 0,
    "bladder_discomfort": 0,
    "foul_smell_of_urine": 0,
    "continuous_feel_of_urine": 0,
    "passage_of_gases": 0,
    "internal_itching": 0,
    "toxic_look_typhos": 0,
    "depression": 0,
    "irritability": 0,
    "muscle_pain": 0,
    "altered_sensorium": 0,
    "red_spots_over_body": 0,
    "belly_pain": 0,
    "abnormal_menstruation": 0,
    "dischromic_patches": 0,
    "watering_from_eyes": 0,
    "increased_appetite": 0,
    "polyuria": 0,
    "family_history": 0,
    "mucoid_sputum": 0,
    "rusty_sputum": 0,
    "lack_of_concentration": 0,
    "visual_disturbances": 0,
    "receiving_blood_transfusion": 0,
    "receiving_unsterile_injections": 0,
    "coma": 0,
    "stomach_bleeding": 0,
    "distention_of_abdomen": 0,
    "history_of_alcohol_consumption": 0,
    "fluid_overload.1": 0,
    "blood_in_sputum": 0,
    "prominent_veins_on_calf": 0,
    "palpitations": 0,
    "painful_walking": 0,
    "pus_filled_pimples": 0,
    "blackheads": 0,
    "scurring": 0,
    "skin_peeling": 0,
    "silver_like_dusting": 0,
    "small_dents_in_nails": 0,
    "inflammatory_nails": 0,
    "blister": 0,
    "red_sore_around_nose": 0,
    "yellow_crust_ooze": 0
}

@app.route('/', methods=['POST'])
@cross_origin()
def index():
    prediction = None
    response = None

    data = request.json  # Assuming JSON data like { "symptoms": "symptom1, symptom2" }
    symptoms = data.get('symptoms', '')

    symptoms_to_update = [symptom.strip() for symptom in symptoms.split(',')]
    updated_symptoms = {symptom: 1 if symptom in symptoms_to_update else 0 for symptom in symptoms_dict.keys()}

    url = "http://127.0.0.1:47334/api/projects/mindsdb/models/hue/predict"
    payload = {"data": [updated_symptoms]}
    headers = {"Content-Type": "application/json"}
        
    response = requests.post(url, json=payload, headers=headers)
    answer = response.text.split("predicted_value")[1][4:6]
    if answer[1] == ",":
        answer = answer[0]

    new_ans = int(answer)
    predicted_dis = disease_dict[new_ans]
    prediction = predicted_dis
    model_response = model.generate_content( f"""
                    You are a healthcare expert. User will tell you about his/her {prediction}, based on that give precaution for it. The Precautions must be in the format like:

                    1. Precaution for the diet:
                    a. Food items to include
                    b. Food items to avoid
                    c. Provide Wikipedia or other sites link related to diet for particular {prediction}.

                    2. Precaution for maintaining hygiene:
                    a. To do activities like sanitizing, handwashing or any other
                    b. Provide Wikipedia or other sites link related to hygiene for particular {prediction}.

                    3. Precaution for physical activities:
                    a. Emphasizing to do required exercise
                    b. Avoid some exercise for disease (if user doesn't have any serious ailment, avoid this part).

                    Try to include emojis as much as possible.
                    """)
    response = model_response.text 

    return {'prediction': prediction, 'response': response}

if __name__ == '__main__':
    app.run(debug=True)
