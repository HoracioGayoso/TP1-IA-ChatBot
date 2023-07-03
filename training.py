import random
import json
import pickle
import numpy as np
import spacy
import re
from tensorflow.keras.models import load_model
from googletrans import Translator

nlp = spacy.load('en_core_web_sm')
ignore_tokens = ['?', '!', '.', ',']


with open('./intents.json') as file:
    intents = json.load(file)

words = pickle.load(open('./words.pkl', 'rb'))
classes = pickle.load(open('./classes.pkl', 'rb'))
model = load_model('./chatbot_model.h5')

translator = Translator()
state = "initial"
amount_hours = 0
modality = ""
last_entry = []
locations = []
holidays = []
expected_salary = []
job = ""
candidate_profile = {
    "job": "",
    "modality": "",
    "hours": "",
    "location": "",
    "expected_salary": "",
    "holidays": ""
}
def calculate_percentage_of_coincidence(arr1, arr2):
    common_elements = set(arr1).intersection(arr2)
    percentage = len(common_elements) / len(arr1) * 100
    return percentage
def clean_up_sentence(sentence):
    global last_entry
    global locations
    global holidays
    doc_es = nlp(sentence)
    sentence = translator.translate(sentence, src="es", dest='en')
    print(sentence)
    doc = nlp(str(sentence.text))
    for entity in doc.ents:
        print(entity.text, entity.label_)
        if entity.label_ == 'DATE':
            holidays.clear()
            holidays.append(entity.text)
        if entity.label_ == 'MONEY':
            expected_salary.clear()
            expected_salary.append(entity.text)
        if entity.label_ == 'GPE' and entity.text != "sysadmin":
            locations.clear()
            locations.append(entity.text)
            print("Location:", locations)
    sentence_words = [token.text.lower() for token in doc if token.text.lower() not in ignore_tokens]
    last_entry = sentence_words
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    porcentajes_formateados = ["{:.2%}".format(valor) for valor in res]
    print(porcentajes_formateados)
    ERROR_TRESHOLD = 0.1
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_TRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def reply(message):
    global job
    global state
    global amount_hours
    global locations
    global modality
    global holidays
    global expected_salary
    tecnologia_front_end = ["html", "css", "react", "javascript", "angular", "typescript", "flutter", "Vue"]
    tecnologia_back_end = ["java", "python", "ruby", "c", "kotlin", "php", "node", "swift"]
    tecnologias_db = ["sql", "not", "mongo", "mongodb", "postgre", "postgresql", "apache", "oracle"]
    roles = ["sysadmin", "sys admin","ithelpdesk", "it", "helpdesk", "help", "desk", "front", "end", "back", "full", "stack",
             "dba", "team", "leader", "software", "engineer", "manager", "ct", "cto", "chief", "technology", "officer",
             "data", "base", "analyst", "backend", "frontend", "fullstack"]
    ints = predict_class(message)
    print("Regla seleccionada:", ints)
    res = get_response(ints, intents)
    #Solicitud basica de trabajo
    if ints[0]['intent'] == "servicio" and state != "area-aceptada":
        state = "solicito-servicio"
        print("Nuevo Estado: ", state)
        return res + " Tienes pensado algun puesto de preferencia?"

    #Solicitud de trabajo media jornada
    if ints[0]['intent'] == "servicio-media-jornada" and state != "area-aceptada":
        amount_hours = 4
        state = "solicito-servicio"
        print("Nuevo Estado: ", state)
        return res + " Tienes pensado algun puesto de preferencia?"

    #Solicitud de trabajo jornada completa
    if ints[0]['intent'] == "servicio-jornada-completa" and state != "area-aceptada":
        amount_hours = 8
        print("Estado viejo:", state)
        state = "solicito-servicio"
        print("Nuevo Estado:", state)
        return res + " Tienes pensado algun puesto de preferencia?"
    #Solicitud de trabajo modalidad remota
    if ints[0]['intent'] == "modalidad-remoto" and state != "area-aceptada":
        modality = "remoto"
        print("Estado viejo:", state)
        state = "solicito-servicio"
        print("Nuevo Estado: ", state)
        return res + " Tienes pensado algun puesto de preferencia?"
    # Solicitud de trabajo modalidad presencial
    if ints[0]['intent'] == "modalidad-presencial" and state != "area-aceptada":
        modality = "presencial"
        print("Estado viejo:", state)
        state = "solicito-servicio"
        print("Nuevo Estado: ", state)
        return res + " Tienes pensado algun puesto de preferencia?"
    if ints[0]['intent'] == "modalidad-hibrida"and state != "area-aceptada":
        modality = "hibrida"
        print("Estado viejo:", state)
        state = "solicito-servicio"
        print("Nuevo Estado: ", state)
        return res + " Tienes pensado algun puesto de preferencia?"
    if ints[0]['intent'] == "afirmacion":
        if state == "oferta-encontrada":
            return "Muchas gracias, nos vemos!"
        if state == "solicito-servicio":
            elementos_comunes = list(set(last_entry).intersection(roles))
            if "back" in elementos_comunes or "backend" in elementos_comunes:
                print("Estado viejo:", state)
                state = "area-oferta"
                print("Nuevo Estado: ", state)
                job = "Back End"
                return "Veo que buscas un trabajo como BackEnd Developer. Es de tu agrado un puesto asi?"
            if "front" in elementos_comunes or "front" in elementos_comunes:
                print("Estado viejo:", state)
                state = "area-oferta"
                print("Nuevo Estado: ", state)
                job = "Front End"
                return "Veo que buscas un trabajo como FrontEnd Developer. Es de tu agrado un puesto asi?"
            if "full" in elementos_comunes or "stack" in elementos_comunes or "fullstack" in elementos_comunes:
                print("Estado viejo:", state)
                state = "area-oferta"
                print("Nuevo Estado: ", state)
                job = "Full Stack"
                return "Veo que buscas un trabajo como FullStack Developer. Es de tu agrado un puesto asi?"
            if "dba" in elementos_comunes or "data" in elementos_comunes or "base" in elementos_comunes or \
                    "analyst" in elementos_comunes:
                print("Estado viejo:", state)
                state = "area-oferta"
                print("Nuevo Estado: ", state)
                job = "DBA"
                return "Veo que buscas un trabajo como DBA. Es de tu agrado un puesto asi?"
            if "it" in elementos_comunes or "help" in elementos_comunes or "desk" in elementos_comunes:
                print("Estado viejo:", state)
                state = "area-oferta"
                print("Nuevo Estado: ", state)
                job = "IT Helpdesk"
                return "Veo que buscas un trabajo como IT Helpdesk. Es de tu agrado un puesto asi?"
            if "sys" in elementos_comunes or "admin" in elementos_comunes or "sysadmin" in elementos_comunes:
                print("Estado viejo:", state)
                state = "area-oferta"
                print("Nuevo Estado: ", state)
                job = "Sysadmin"
                return "Veo que buscas un trabajo como Sysadmin. Es de tu agrado un puesto asi?"
            if "team" in elementos_comunes or "leader" in elementos_comunes:
                print("Estado viejo:", state)
                state = "area-oferta"
                print("Nuevo Estado: ", state)
                job = "Team Leader"
                return "Veo que buscas un trabajo como Team Leader. Es de tu agrado un puesto asi?"
            if "software" in elementos_comunes or "engineer" in elementos_comunes or "manager" in elementos_comunes:
                print("Estado viejo:", state)
                state = "area-oferta"
                print("Nuevo Estado: ", state)
                job = "Software Engineer Manager"
                return "Veo que buscas un trabajo como Software Engineer Manager. Es de tu agrado un puesto asi?"
            if "ct" in elementos_comunes or "chief" in elementos_comunes or "cto" in elementos_comunes\
                    or "technology" in elementos_comunes:
                print("Estado viejo:", state)
                state = "area-oferta"
                print("Nuevo Estado: ", state)
                job = "CTO"
                return "Veo que buscas un trabajo como CTO. Es de tu agrado un puesto asi?"

        #Si al inicio el chat no entiende, ofrece buscar trabajo. si responden si, se ejecuta este
        if state == "initial":
            print("Estado viejo:", state)
            state = "solicito-servicio"
            print("Nuevo Estado: ", state)
            return res + " Tienes pensado algun puesto de preferencia?"

        #Si el usuario acepta la oferta ofrecida se ejecuta este
        if state == "area-oferta":
            print("Estado viejo:", state)
            state = "area-aceptada"
            print("Nuevo Estado: ", state)
            if modality == "":
                return res + " Confirmada el area de trabajo. " \
                             "Que tipo de trabajo prefieres, remoto, presencial, hibrido...?"
            if amount_hours == 0:
                return res + " Confirmada el area de trabajo. " \
                                 "Cuantas horas consideras apropiadas en tu jornada laboral?"
            if len(locations) == 0:
                return " En que ciudad/pais te gustaria trabajar?"
    if ints[0]['intent'] == "negacion":
        if state == "oferta-encontrada":
            print("Estado viejo: ", state)
            state = "initial"
            print("Nuevo Estado: ", state)
            return res + "Hola, en que puedo ayudarte? Soy Chaty, tu asistente inteligente. Comencemos con las " \
                         "preguntas. Dime que quieres saber y te respondo."
        if state == "initial":
            return "Muchas gracias, nos vemos!"

        if state == "solicito-servicio":
            return res + " Para comenzar...podrias enumerarme tecnologias en las que tengas conocimiento/experiencia" \
                         " o bien habilidades relacionadas con las areas de Infraestructura o Gerencia"
        if state == "area-oferta":
            print("Estado viejo: ", state)
            state = "solicito-servicio"
            print("Nuevo Estado: ", state)
            return res + "...podrias enumerarme tecnologias en las que tengas conocimiento/experiencia" \
                         " o bien habilidades relacionadas con las areas de Infraestructura o Gerencia"
    if ints[0]['intent'] == "tecnologias" and state != "area-aceptada":
        percentages = {
            "Front End": calculate_percentage_of_coincidence(tecnologia_front_end, last_entry),
            "Back End": calculate_percentage_of_coincidence(tecnologia_back_end, last_entry),
            "DBA": calculate_percentage_of_coincidence(tecnologias_db, last_entry)
        }
        print(percentages)
        count = sum(1 for percentage in percentages.values() if percentage >= 50)
        # Ordenar los nombres de los arreglos por el porcentaje de mayor a menor
        sorted_data = sorted(percentages, key=percentages.get, reverse=True)
        if count > 1:
            print("Estado viejo: ", state)
            state = "area-oferta"
            print("Nuevo Estado: ", state)
            job = "Full Stack"
            return res + " Por lo visto tu perfil se ajusta mas al desarrollo Full Stack." \
                         " Es de tu agrado un puesto asi?"
        if count == 1:
            print("Estado viejo: ", state)
            state = "area-oferta"
            print("Nuevo Estado: ", state)
            job = sorted_data[0]
            return res + " Por lo visto tu perfil se ajusta mas al desarrollo "+ sorted_data[0] + \
                   ". Es de tu agrado un puesto asi?"
        else:
            if percentages["Front End"] == 0.0 and percentages["Back End"] == 0.0 and percentages["DBA"] == 0.0:
                return "No te entendi. Si gustas, como tu asistente virtual de RRHH puedo ayudarte a buscar un nuevo " \
                       "trabajo. Quieres comenzar el proceso?"
            return "Parece que el area de desarrollo no es la que mas se adecua a tu perfil. Cuales consideras tus " \
                   "habilidades relacionadas con las areas de Infraestructura o Gerencia"
    if ints[0]['intent'] == "IT-Helpdesk":
        job = "IT Helpdesk"
        print("Estado viejo: ", state)
        state = "area-oferta"
        print("Nuevo Estado: ", state)
        return res + " Es de tu agrado un puesto asi?"
    if ints[0]['intent'] == "Sys-Admin":
        job = "Sysadmin"
        print("Estado viejo: ", state)
        state = "area-oferta"
        print("Nuevo Estado: ", state)
        return res + " Es de tu agrado un puesto asi?"
    if ints[0]['intent'] == "Team-Leader":
        job = "Team Leader"
        print("Estado viejo: ", state)
        state = "area-oferta"
        print("Nuevo Estado: ", state)
        return res + " Es de tu agrado un puesto asi?"
    if ints[0]['intent'] == "SEM":
        job = "Software Engineer Manager"
        print("Estado viejo: ", state)
        state = "area-oferta"
        print("Nuevo Estado: ", state)
        return res + " Es de tu agrado un puesto asi?"
    if ints[0]['intent'] == "CTO":
        job = "CTO"
        print("Estado viejo: ", state)
        state = "area-oferta"
        print("Nuevo Estado: ", state)
        return res + " Es de tu agrado un puesto asi?"

    #Una vez que se acepta la oferta, se completan la modalidad, las horas y la localizacion
    if state == "area-aceptada":
        print("Llegue: ", state)
        print("Modalidad:", modality)
        print("Horas:", amount_hours)
        print("Lugar:", locations)
        if ints[0]['intent'] == "servicio-media-jornada":
            amount_hours = 4
            return res + "En que ciudad/pais te gustaria trabajar?"
            # Solicitud de trabajo jornada completa
        if ints[0]['intent'] == "servicio-jornada-completa":
            amount_hours = 8
            if len(locations)==0:
                return res + "En que ciudad/pais te gustaria trabajar?"
            else:
                return res + " Durante nuestra conversacion tome nota de que te gustaria trabajar en la siguiente " \
                             "ubicacion: " + locations[0] + ". En caso de ser correcto indicame una nueva ubicacion. " \
                                "Faltaria definir algunas condiciones que te gustaria que " \
                           "tenga tu nuevo trabajo...podrias comentarme que esperas en cuanto a temas como " \
                           "vacaciones y sueldo (mensual)"
            # Solicitud de trabajo modalidad remota
        if ints[0]['intent'] == "modalidad-remoto":
            modality = "remoto"
            return res + " Cuantas horas consideras apropiadas en tu jornada laboral?"
            # Solicitud de trabajo modalidad presencial
        if ints[0]['intent'] == "modalidad-presencial":
            modality = "presencial"
            return res + " Cuantas horas consideras apropiadas en tu jornada laboral?"
        if ints[0]['intent'] == "modalidad-hibrida":
            modality = "hibrida"
            return res + " Cuantas horas consideras apropiadas en tu jornada laboral?"
        if modality != "":
            if amount_hours != 0:
                if len(locations) > 0:
                    print("Estado viejo: ", state)
                    state = "condiciones_laborales_pendientes"
                    print("Nuevo Estado: ", state)
                    return "Genial, ya falta poco. Faltaria definir algunas condiciones que te gustaria que " \
                           "tenga tu nuevo trabajo...podrias comentarme que esperas en cuanto a temas como " \
                           "vacaciones y sueldo (mensual)"
                else:
                    return "En que ciudad/pais te gustaria trabajar?"
            else:
                return "Cuantas horas consideras apropiadas en tu jornada laboral?"

        else:
            return "Que tipo de trabajo prefieres, remoto, presencial, hibrido...?"
            # Solicitud de trabajo media jornada
    if state == "condiciones_laborales_pendientes":
        if ints[0]['intent'] == "vacaciones":
            if len(holidays) == 0:
                holidays.append("No quiere vacaciones")
                if len(expected_salary) != 0:
                    return "Entiendo...tendre en cuenta que no deseas vacaciones"
                else:
                    return "Entiendo...tendre en cuenta que no deseas vacaciones. Que expectativas tienes respecto" \
                           "a tu proximo salario"
        if ints[0]['intent'] == "vacaciones" or ints[0]['intent'] == "salario" or ints[0]['intent'] == "obra-social":
            print("Vacaciones:", holidays)
            print("Salario:", expected_salary)
            if len(holidays) > 0:
                if len(expected_salary)==0:
                    return res + " Que preferencias tienes respecto a tu salario?"
            if len(expected_salary) > 0:
                if len(holidays) == 0:
                    return res + " Que preferencias tienes respecto a tus vacaciones?"
            if len(holidays) > 0 and len(expected_salary) > 0:
                print("Estado viejo: ", state)
                state = "looking_offers"
                print("Nuevo Estado: ", state)
            else:
                return res + "Desafortunadamente no pude entender cual es tu preferencia. " \
                             "Podrias redactarlo nuevamente?"
    if state == "looking_offers":
        global candidate_profile
        candidate_profile["job"] = job
        candidate_profile["hours"] = amount_hours
        candidate_profile["modality"] = modality
        candidate_profile["location"] = locations[0]
        candidate_profile["holidays"] = holidays[0]
        candidate_profile["expected_salary"] = extraer_numero(expected_salary[0])
        ofertas = filtrar_json(candidate_profile)
        state = "oferta-encontrada"
        return convert_data_to_string(ofertas) + "\nPor Favor indica si alguna opcion es de tu agrada, e indica el" \
                                                 " Nro de la misma. En caso de no estar conforme, indica con una " \
                                                 "respuesta negativa."
    #Esta seccion es mas que nada para cuando no se entiende algo, deberia venir por aca
    else:
        if state == "initial":
            return "No te entendi. Si gustas, como tu asistente virtual de RRHH puedo ayudarte a buscar un " \
                   "nuevo trabajo. Quieres comenzar el proceso?"
        else:
            return "No te entendi, podrias redactarlo de manera diferente por favor!"


def filtrar_json(objeto_x):
    resultados = []

    with open('schemaTP2IACompleto.json') as file:
        data = json.load(file)

        for item in data:
            if int(objeto_x['expected_salary']) <= int(item['expected_salary']) \
                    and objeto_x['job'].lower() == item['job'].lower() \
                    and objeto_x['hours'] == item['hours'] \
                    and objeto_x['modality'].lower() == item['modality'].lower():
                if objeto_x['modality'] in ['presencial', 'hibrido']:
                    if objeto_x['location'] != item['location']:
                        continue

                holidays_x = convertir_a_dias(objeto_x['holidays'])
                holidays_json = convertir_a_dias(item['holidays'])
                if holidays_x <= holidays_json:
                    resultados.append(item)

    return resultados


def convertir_a_dias(holidays):
    if 'semanas' in holidays:
        semanas = int(holidays.split()[0])
        return semanas * 7
    elif 'dias' in holidays:
        return int(holidays.split()[0])
    else:
        return 0

def extraer_numero(cadena):
    numero = re.search(r'\d+', cadena).group()
    return str(numero)

def convert_data_to_string(data):
    result = ""
    for i, item in enumerate(data):
        result += f"Oferta {i+1}: {', '.join([f'{key}: {value}' for key, value in item.items()])}\n\n"
    return result

