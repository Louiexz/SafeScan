# ai_model.py
import joblib
import pandas as pd

def make_prediction(software):
    # Defina a ordem das features conforme sua lista

    feature_order = [
        "ACCESS_COARSE_LOCATION", "ACCESS_FINE_LOCATION", "BLUETOOTH", "CHANGE_NETWORK_STATE", 
        "DISABLE_KEYGUARD", "GET_TASKS", "KILL_BACKGROUND_PROCESSES", "READ_SMS", 
        "RECEIVE_BOOT_COMPLETED", "RECEIVE_SMS", "SEND_SMS", "SYSTEM_ALERT_WINDOW", 
        "VIBRATE", "WAKE_LOCK", "WRITE_EXTERNAL_STORAGE", "Ljava/lang/System;->load", 
        "Ldalvik/system/DexClassLoader;->loadClass", "Ljava/lang/System;->loadLibrary", 
        "Ljava/net/URL;->openConnection", "Landroid/telephony/SmsManager;->sendMultipartTextMessage", 
        "Landroid/media/AudioRecord;->startRecording", "Landroid/telephony/TelephonyManager;->getCellLocation", 
        "Landroid/location/LocationManager;->getLastKgoodwarewnLocation", 
        "Landroid/content/pm/PackageManager;->getInstalledPackages", "Landroid/telephony/TelephonyManager;->getNetworkOperator", 
        "Landroid/telephony/TelephonyManager;->getNetworkOperatorName", "Landroid/telephony/TelephonyManager;->getNetworkCountryIso", 
        "Landroid/telephony/TelephonyManager;->getSimOperator", "Landroid/telephony/TelephonyManager;->getSimOperatorName", 
        "Landroid/telephony/TelephonyManager;->getSimCountryIso"
    ]

    # Reorganize 'software' para que as chaves sigam a ordem definida em 'feature_order'
    software_ordered = {feature: software.get(feature, 0) for feature in feature_order}

    # Carregar o modelo treinado (exemplo usando joblib)
    model = joblib.load('ml_model/best_model_dt.pkl')

    # Preparar os dados para a predição
    features_array = pd.DataFrame([software_ordered])
    
    #features_array = np.array(features).reshape(1, -1)
    # Fazer a predição
    prediction = model.predict(features_array)

    # Retornar a previsão (como 'Malware' ou 'Goodware')
    return 'Malware' if prediction[0] == 1 else 'Goodware'

