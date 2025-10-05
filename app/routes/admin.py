from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models import User, Game, Guess, db
from datetime import date, datetime, time

# register blueprint under /admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required():
    return current_user.is_authenticated and getattr(current_user, "is_admin", False)

# -----------------------------
# Daily report: number of users who played today + number of correct guesses today
# URL: /admin/daily
# -----------------------------
@admin_bp.route('/daily', methods=['GET'])
@login_required
def daily_report():
    if not admin_required():
        flash("Access denied: Admins only.")
        return redirect(url_for('auth.login'))

    today = date.today()
    day_start = datetime.combine(today, time.min)

    # distinct users who played today (count user_ids in Game)
    users_today = db.session.query(Game.user_id).filter(Game.date >= day_start).distinct().count()

    # correct guesses today: join Guess -> Game and filter by Game.date
    correct_guesses_today = db.session.query(Guess).join(Game, Guess.game_id == Game.id).filter(
        Guess.is_correct == True,
        Game.date >= day_start
    ).count()

    return render_template('admin.html',
                           report_type='daily',
                           daily_users=users_today,
                           daily_correct=correct_guesses_today,
                           today=today.strftime("%Y-%m-%d"))

# -----------------------------
# User report: admin can enter a username and get per-game stats
# URL: /admin/user
# -----------------------------
@admin_bp.route('/user', methods=['GET', 'POST'])
@login_required
def user_report():
    if not admin_required():
        flash("Access denied: Admins only.")
        return redirect(url_for('auth.login'))

    report_data = None
    username = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User not found.")
            return render_template('admin.html', report_type='user')

        # gather each game for this user
        games = Game.query.filter_by(user_id=user.id).order_by(Game.date.desc()).all()
        report_data = []
        for g in games:
            guesses_count = Guess.query.filter_by(game_id=g.id).count()
            correct_count = Guess.query.filter_by(game_id=g.id, is_correct=True).count()
            report_data.append({
                'game_id': g.id,
                'date': g.date.strftime("%Y-%m-%d %H:%M:%S"),
                'words_tried': guesses_count,
                'correct_guesses': correct_count,
            })

    return render_template('admin.html', report_type='user', report_data=report_data, username=username)

