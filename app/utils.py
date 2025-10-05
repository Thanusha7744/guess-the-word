import re
from .models import Word, db

# Validate username: at least 5 letters
def validate_username(username):
    return bool(re.match(r'^[A-Za-z]{5,}$', username))

# Validate password: at least 5 chars, alpha + numeric + special ($,% ,* ,@)
def validate_password(password):
    return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$%*@])[A-Za-z\d$%*@]{5,}$', password))

# Check guess vs word and return colors
def check_guess(guess, actual):
    colors = ['grey']*5
    actual_letters = list(actual)
    
    # First pass: green
    for i in range(5):
        if guess[i] == actual[i]:
            colors[i] = 'green'
            actual_letters[i] = None
    
    # Second pass: orange
    for i in range(5):
        if colors[i] == 'grey' and guess[i] in actual_letters:
            colors[i] = 'orange'
            actual_letters[actual_letters.index(guess[i])] = None
    return colors

# Insert initial 20 words into DB
def insert_initial_words():
    words_list = [
        "APPLE","BRAVE","CRANE","DREAM","ELITE",
        "FLAME","GRAPE","HOUSE","INPUT","JOKER",
        "KNIFE","LEMON","MONEY","NURSE","OCEAN",
        "PLANT","QUEEN","ROBOT","SUGAR","TIGER"
    ]
    for w in words_list:
        if not Word.query.filter_by(word=w).first():
            db.session.add(Word(word=w))
    db.session.commit()
