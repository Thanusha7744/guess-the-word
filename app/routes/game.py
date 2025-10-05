from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from ..models import User, Word, Game, Guess, db
from ..utils import check_guess
import random
from datetime import datetime, date, time

game_bp = Blueprint('game', __name__)

# -----------------------------
# Start / Play Game Page
# -----------------------------
@game_bp.route('/game', methods=['GET', 'POST'])
@login_required
def play_game():
    # optional guard (login_required should handle this)
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    # Check daily game limit (3 games/day)
    today = date.today()
    day_start = datetime.combine(today, time.min)  # midnight today
    games_today = Game.query.filter(
        Game.user_id == current_user.id,
        Game.date >= day_start
    ).count()

    if games_today >= 3:
        flash("You have reached your daily limit of 3 games.")
        return render_template('game.html', game_over=True)

    # If session already has a game, continue it
    game = None
    if 'current_game_id' in session:
        try:
            game_id = int(session.get('current_game_id'))
            game = Game.query.get(game_id)
            # if the game doesn't exist or belongs to different user, clear it
            if not game or game.user_id != current_user.id:
                session.pop('current_game_id', None)
                game = None
        except Exception:
            session.pop('current_game_id', None)
            game = None

    # Start a new game if none in session
    if not game:
        all_words = Word.query.all()
        if not all_words:
            flash("No words available in database.")
            return render_template('game.html', game_over=True)
        word_obj = random.choice(all_words)
        new_game = Game(user_id=current_user.id, word_id=word_obj.id, win=False)
        db.session.add(new_game)
        db.session.commit()
        session['current_game_id'] = new_game.id
        game = new_game
    else:
        word_obj = Word.query.get(game.word_id)

    # Handle guess submission
    if request.method == 'POST':
        guess_word = request.form.get('guess', '').upper().strip()

        # Validate guess length
        if len(guess_word) != 5:
            flash("Guess must be a 5-letter word.")
            return redirect(url_for('game.play_game'))

        # Check number of guesses so far
        guesses_count = Guess.query.filter_by(game_id=game.id).count()
        if guesses_count >= 5:
            flash("You have used all 5 guesses for this game.")
            return render_template('game.html', game_over=True)

        # Compute colors and correctness
        colors = check_guess(guess_word, word_obj.word)
        is_correct = (guess_word == word_obj.word)

        # Save guess
        new_guess = Guess(game_id=game.id, guess_word=guess_word, is_correct=is_correct)
        db.session.add(new_guess)

        # If correct, mark game as win and end session game
        if is_correct:
            game.win = True
            db.session.commit()
            session.pop('current_game_id', None)
            flash("Congratulations! You guessed the word correctly.")
            return render_template('game.html', game_over=True, word=word_obj.word)

        db.session.commit()

        # If 5 guesses used, end game
        if guesses_count + 1 >= 5 and not is_correct:
            session.pop('current_game_id', None)
            flash(f"Better luck next time! The word was {word_obj.word}")
            return render_template('game.html', game_over=True, word=word_obj.word)

        # Redirect to GET to avoid duplicate form submission
        return redirect(url_for('game.play_game'))

    # Prepare previous guesses for template: list of rows where each row is [(letter,color),...]
    previous_guess_objs = Guess.query.filter_by(game_id=game.id).order_by(Guess.id).all()
    display_guesses = []
    for g in previous_guess_objs:
        letters = list(g.guess_word)
        colors = check_guess(g.guess_word, word_obj.word)
        row = list(zip(letters, colors))
        display_guesses.append(row)

    return render_template(
        'game.html',
        game_over=False,
        previous_guesses=display_guesses
    )
