from flask import Blueprint, render_template, url_for, request, flash, abort, redirect
from flask_login import login_required, current_user
from . import db
from .models import User
from .models import Workout

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(email=current_user.email).first_or_404()
        workouts = Workout.query.filter_by(author=user).paginate(page=page, per_page=3)
        return render_template('main/index.html', workouts=workouts, user=user)
    return render_template('main/index.html')

@main.route('/new_workout')
@login_required
def new_workout():
    return render_template('main/new_workout.html')

@main.route('/new_workout', methods=['POST'])
@login_required
def new_workout_post():
    pushups = request.form.get('pushups')
    comment = request.form.get('comment')
    workout = Workout(pushups=pushups, comment=comment, author=current_user)
    
    db.session.add(workout)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/workout/<int:workout_id>/update', methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.pushups = request.form['pushups']
        workout.comment = request.form['comment']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/update_workout.html', workout=workout)

@main.route('/workout/<int:workout_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.index'))