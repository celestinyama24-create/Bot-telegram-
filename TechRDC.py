import telebot
import random
from groq import Groq
import os
import threading
import time
from datetime import datetime

TOKEN = "8734755653:AAFPEWLDBYzvrbcZZdeRSr21AalcfFU9ekA"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

bot = telebot.TeleBot(TOKEN)
user_en_attente = {}

def menu_principal():
    clavier = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    clavier.row("Astuce", "Raccourci")
    clavier.row("Flutter", "Python")
    clavier.row("Opportunite", "Question")
    clavier.row("Partager", "A propos")
    return clavier

def demander_ia(prompt):
    try:
        variation = random.randint(1, 10000)
        jour = random.choice(["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"])
        niveau = random.choice(["débutant", "intermédiaire", "avancé"])
        langue = random.choice(["Python", "Dart", "JavaScript", "Kotlin"])
        sujet = random.choice(["performance", "sécurité", "lisibilité", "productivité", "débogage", "architecture"])
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"Tu es TechRDC Bot, un assistant tech pour les developpeurs africains. Tu reponds toujours en francais. IMPORTANT : Aujourd'hui c'est {jour}, variation #{variation}. Concentre-toi sur le sujet : {sujet}. Niveau : {niveau}. Ne repete JAMAIS une reponse precedente."
                },
                {
                    "role": "user",
                    "content": f"{prompt} (contexte: {langue}, {sujet}, variation #{variation})"
                }
            ],
            max_tokens=300,
            temperature=1.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur : {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    prenom = message.from_user.first_name
    texte = "Bienvenue " + prenom + " sur TechRDC Bot! 🇨🇩🚀\n\n"
    texte += "Je suis votre compagnon tech propulse par l'IA!\n\n"
    texte += "Utilisez les boutons en bas 👇"
    bot.reply_to(message, texte, reply_markup=menu_principal())

@bot.message_handler(commands=['partager'])
def partager(message):
    texte = "📤 INVITEZ VOS AMIS!\n\n"
    texte += "Partagez ce lien :\n"
    texte += "👉 https://t.me/TechRDC_bot\n\n"
    texte += "Merci de nous soutenir! 💪"
    bot.reply_to(message, texte, reply_markup=menu_principal())

@bot.message_handler(commands=['apropos'])
def apropos(message):
    texte = "ℹ️ A PROPOS\n\n"
    texte += "🇨🇩 Créé par Célestin Yama\n"
    texte += "📱 Whatsapp : +243814054212\n"
    texte += "@ Email : celestinyama24@gmail.com\n"
    texte += "🎯 Mission : Democratiser la tech en RDC\n\n"
    texte += "💪 Ensemble, faisons grandir la tech en Afrique!"
    bot.reply_to(message, texte, reply_markup=menu_principal())

@bot.message_handler(commands=['astuce'])
def astuce(message):
    bot.reply_to(message, "⏳ Generation en cours...")
    reponse = demander_ia("Donne une astuce de programmation unique pour debutant. Sois court et pratique.")
    bot.reply_to(message, "💡 ASTUCE\n\n" + reponse, reply_markup=menu_principal())

@bot.message_handler(commands=['flutter'])
def flutter(message):
    bot.reply_to(message, "⏳ Generation en cours...")
    reponse = demander_ia("Donne un conseil pratique sur Flutter pour debutant avec exemple de code.")
    bot.reply_to(message, "🐦 CONSEIL FLUTTER\n\n" + reponse, reply_markup=menu_principal())

@bot.message_handler(commands=['python'])
def python(message):
    bot.reply_to(message, "⏳ Generation en cours...")
    reponse = demander_ia("Donne un conseil pratique sur Python pour debutant avec exemple de code.")
    bot.reply_to(message, "🐍 CONSEIL PYTHON\n\n" + reponse, reply_markup=menu_principal())

@bot.message_handler(commands=['raccourci'])
def raccourci(message):
    bot.reply_to(message, "⏳ Generation en cours...")
    reponse = demander_ia("Donne un raccourci Windows utile et explique comment il ameliore la productivite.")
    bot.reply_to(message, "⌨️ RACCOURCI WINDOWS\n\n" + reponse, reply_markup=menu_principal())

@bot.message_handler(commands=['opportunite'])
def opportunite(message):
    bot.reply_to(message, "⏳ Generation en cours...")
    reponse = demander_ia("Donne une opportunite tech reelle pour developpeur africain debutant avec lien ou plateforme.")
    bot.reply_to(message, "🌍 OPPORTUNITE TECH\n\n" + reponse, reply_markup=menu_principal())

@bot.message_handler(commands=['question'])
def question(message):
    user_en_attente[message.chat.id] = True
    texte = "❓ Posez votre question tech!\n\n"
    texte += "Ecrivez simplement votre question\n"
    texte += "et j'y reponds immediatement! 💬"
    bot.reply_to(message, texte, reply_markup=menu_principal())

@bot.message_handler(func=lambda m: m.text is not None and m.text in ["Astuce", "Raccourci", "Flutter", "Python", "Opportunite", "Question", "Partager", "A propos"])
def gerer_boutons(message):
    texte = message.text
    if texte == "Astuce":
        astuce(message)
    elif texte == "Raccourci":
        raccourci(message)
    elif texte == "Flutter":
        flutter(message)
    elif texte == "Python":
        python(message)
    elif texte == "Opportunite":
        opportunite(message)
    elif texte == "Question":
        user_en_attente[message.chat.id] = True
        bot.reply_to(message, "❓ Posez votre question tech!\n\nEcrivez simplement votre question et j'y reponds! 💬", reply_markup=menu_principal())
    elif texte == "Partager":
        partager(message)
    elif texte == "A propos":
        apropos(message)

@bot.message_handler(func=lambda message: True)
def inconnu(message):
    if user_en_attente.get(message.chat.id):
        user_en_attente[message.chat.id] = False
        question_text = message.text
        bot.reply_to(message, "⏳ Reflexion en cours...")
        reponse = demander_ia("Reponds a cette question tech de maniere claire et simple : " + question_text)
        bot.reply_to(message, "🤖 REPONSE TECHRDC\n\n" + reponse + "\n\nAppuyez sur Question pour une autre ❓", reply_markup=menu_principal())
    else:
        bot.reply_to(message, "❓ Je n'ai pas compris.\nUtilisez les boutons en bas! 👇", reply_markup=menu_principal())

print("TechRDC Bot demarre! 🇨🇩🤖")

# ================================
# PUBLICATION AUTOMATIQUE
# ================================

CANAL_ID = "@techrdc_cm"
VOTRE_ID = 6786514592

def publier_astuces():
    while True:
        now = datetime.now()
        # Publier à 8h du matin
        if now.hour == 8 and now.minute == 0:
            
            # Astuce du jour
            astuce = demander_ia("Donne une astuce de programmation unique pour aujourd'hui")
            bot.send_message(CANAL_ID, f"💡 ASTUCE DU JOUR\n\n{astuce}")
            time.sleep(60)
            
            # Raccourci du jour
            raccourci = demander_ia("Donne un raccourci Windows utile du jour")
            bot.send_message(CANAL_ID, f"⌨️ RACCOURCI DU JOUR\n\n{raccourci}")
            time.sleep(60)
            
            # Opportunite du jour
            opp = demander_ia("Donne une opportunite tech pour developpeurs africains")
            bot.send_message(CANAL_ID, f"🌍 OPPORTUNITE DU JOUR\n\n{opp}")
            
        time.sleep(30)

# Lancer la publication en arriere plan
thread = threading.Thread(target=publier_astuces)
thread.daemon = True
thread.start()
bot.polling()
