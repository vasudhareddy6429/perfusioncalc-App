import math

def calculate_bsa(height_cm, weight_kg):
    return math.sqrt((height_cm * weight_kg) / 3600)

def calculate_flow_rate(bsa, cardiac_index=2.4):
    return bsa * cardiac_index

def calculate_complete_blood_flow(bsa):
    return bsa * 2.4

def calculate_average_blood_flow(bsa):
    return bsa * 1.6

def calculate_ebv(weight_kg, patient_type):
    if patient_type.lower() == 'female':
        return weight_kg * 60
    elif patient_type.lower() == 'male':
        return weight_kg * 70
    elif patient_type.lower() == 'pediatric':
        return weight_kg * 80
    else:
        return weight_kg * 70  # Default adult

def calculate_rbc_patient(ebv, hct_percent):
    return ebv * (hct_percent / 100)

def calculate_cardioplegia_dose(weight_kg, patient_type):
    if patient_type.lower() == 'adult':
        return (weight_kg * 20) / 5
    elif patient_type.lower() == 'pediatric':
        return (weight_kg * 30) / 5
    else:
        raise ValueError("Invalid patient type: choose 'adult' or 'pediatric'")
