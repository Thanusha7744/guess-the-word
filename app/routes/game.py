from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from ..models import User, Word, Game, Guess, db
from ..utils import check_guess
import random
from datetime import datetime, date, time
from sqlalchemy import or_

game_bp = Blueprint('game', __name__)

# -----------------------------
# Play Game Route
# -----------------------------
@game_bp.route('/game', methods=['GET', 'POST'])
@login_required
def play_game():
    today = date.today()
    day_start = datetime.combine(today, time.min)

    # -----------------------------
    # Count only COMPLETED games today
    # Completed = win=True or 5 guesses used
    # -----------------------------
    completed_games_today = 0
    games_today_list = Game.query.filter(Game.user_id == current_user.id, Game.date >= day_start).all()
    for g in games_today_list:
        guesses_count = Guess.query.filter_by(game_id=g.id).count()
        if g.win or guesses_count >= 5:
            completed_games_today += 1

    if completed_games_today >= 3:
        return render_template(
            'game.html',
            game_over=True,
            limit_reached=True,
            result_message="You have reached your daily limit of 3 words.",
            result_category="warning",
            previous_guesses=[]
        )

    # -----------------------------
    # Continue existing game or start new
    # -----------------------------
    game = None
    if 'current_game_id' in session:
        game = Game.query.get(session['current_game_id'])
        if not game or game.user_id != current_user.id:
            session.pop('current_game_id', None)
            game = None

    if not game:
        all_words = Word.query.all()
        if not all_words:
            return render_template(
                'game.html',
                game_over=True,
                limit_reached=True,
                result_message="No words available in database.",
                result_category="error",
                previous_guesses=[]
            )
        word_obj = random.choice(all_words)
        game = Game(user_id=current_user.id, word_id=word_obj.id, win=False)
        db.session.add(game)
        db.session.commit()
        session['current_game_id'] = game.id
    else:
        word_obj = Word.query.get(game.word_id)

    game_over = False
    game_won = False
    result_message = None
    result_category = None

    # -----------------------------
    # Handle guess submission
    # -----------------------------
    if request.method == 'POST' and 'guess' in request.form:
        guess_word = request.form.get('guess', '').upper().strip()

        if len(guess_word) != 5:
            result_message = "Guess must be a 5-letter word."
            result_category = "error"
        else:
            guesses_count = Guess.query.filter_by(game_id=game.id).count()
            colors = check_guess(guess_word, word_obj.word)
            is_correct = (guess_word == word_obj.word)
            new_guess = Guess(game_id=game.id, guess_word=guess_word, is_correct=is_correct)
            db.session.add(new_guess)
            db.session.commit()

            if is_correct:
                game.win = True
                db.session.commit()
                game_over = True
                game_won = True
                result_message = f"🎉 Congratulations! You guessed correctly: {word_obj.word}"
                result_category = "success"
                session.pop('current_game_id', None)
            elif guesses_count + 1 >= 5:
                game_over = True
                result_message = f"Your guess was wrong. The correct word was: {word_obj.word}"
                result_category = "warning"
                session.pop('current_game_id', None)

    # -----------------------------
    # Prepare previous guesses
    # -----------------------------
    previous_guess_objs = Guess.query.filter_by(game_id=game.id).order_by(Guess.id).all()
    display_guesses = []
    for g in previous_guess_objs:
        letters = list(g.guess_word)
        colors = check_guess(g.guess_word, word_obj.word)
        display_guesses.append(list(zip(letters, colors)))

    return render_template(
        'game.html',
        game_over=game_over,
        game_won=game_won,
        previous_guesses=display_guesses,
        result_message=result_message,
        result_category=result_category,
        limit_reached=False
    )


# -----------------------------
# Finish Game (OK Button)
# -----------------------------
@login_required
@game_bp.route('/game/finish', methods=['POST'])
def finish_game():
    session.pop('current_game_id', None)
    return redirect(url_for('home.dashboard'))