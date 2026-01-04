def classify_complaint(text):
    text = text.lower()

    if any(word in text for word in ["harassment", "fight", "unsafe", "assault"]):
        return "Safety", "High"
    elif any(word in text for word in ["wifi", "internet", "network"]):
        return "IT", "Medium"
    elif any(word in text for word in ["fan", "ac", "light", "electricity"]):
        return "Infrastructure", "Medium"
    else:
        return "General", "Low"
