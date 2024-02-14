from flask import Blueprint, render_template, redirect, url_for, flash
from app_database.models import Experience
from .forms import ExpirienceForm
from app_database.connect import session_maker
from flask_login import login_required, current_user
from app_utils.utils import messages_errors_conn_db, messages_errors_field
from sqlalchemy import select, delete

expirience = Blueprint('expirience', __name__, template_folder='templates', static_folder='static')


@expirience.route('/create-expirience', methods=['GET', 'POST'])
@login_required
def create_expirience():
    """
    Создает новый раздел опыта
    """

    form = ExpirienceForm()
    response = {
        'expirience': True
    }
    if form.validate_on_submit():
        form_data = form.data
        if form_data['year_finish'] == 0:
            year_finish = None
        else:
            year_finish = form_data['year_finish']
        try:
            with session_maker() as conn:
                new_experience = Experience(
                    year_start=form_data['year_start'],
                    year_finish=year_finish,
                    company=form_data['company'],
                    job=form_data['job'],
                    description=form_data['description'],
                    user_fk=current_user.id,
                    published=form_data['published']
                )
                conn.add(new_experience)
                conn.commit()
                flash(message='Successfully added', category='success')
                return redirect(url_for('expirience.create_expirience'))
        except Exception as err:
            messages_errors_conn_db(err, conn, 'error')
    else:
        messages_errors_field(form, 'error')
    return render_template('create_or_login_user.html', form=form, response=response)


@expirience.route('/all-expirience', methods=['GET'])
@login_required
def all_expirience():
    """
    Показать все разделы опыта
    """

    try:
        with session_maker() as conn:
            query = select(Experience).filter_by(user_fk=current_user.id)
            res = conn.execute(query)
            result = res.scalars().all()
            is_empty = False if result else True
            return render_template('all_expirience.html', result=result, is_empty=is_empty)
    except Exception as err:
        messages_errors_conn_db(err, conn, 'error')


@expirience.route('/update-experience/<int:expirience_id>', methods=['GET', 'POST'])
@login_required
def update_expirience(expirience_id):
    """
    Обновляет конкретный раздел опыта
    :param expirience_id: id записи в базе данных
    """

    response = {
        'update_expirience': True
    }
    try:
        with session_maker() as conn:
            query = select(Experience).filter_by(id=expirience_id)
            res = conn.execute(query)
            old_exp = res.scalars().first()
            form = ExpirienceForm(obj=old_exp)
            if form.validate_on_submit():
                form_data = form.data
                old_exp.year_start = form_data['year_start'],
                old_exp.year_finish = form_data['year_finish'],
                old_exp.company = form_data['company'],
                old_exp.job = form_data['job'],
                old_exp.description = form_data['description'],
                old_exp.published = form_data['published']
                conn.commit()
                flash(message='Updated successfully', category='success')
                return redirect(url_for('expirience.all_expirience'))
            else:
                messages_errors_field(form, 'error')
    except Exception as err:
        messages_errors_conn_db(err, conn, 'error')
    return render_template('create_or_login_user.html', form=form, response=response)


@expirience.route('/delete_expirience/<int:expirience_id>', methods=['GET'])
@login_required
def delete_expirience(expirience_id):
    """
    Удаление раздела опыта
    :param expirience_id: id записи в базе данных
    """

    try:
        with session_maker() as conn:
            query = delete(Experience).filter_by(id=expirience_id)
            conn.execute(query)
            conn.commit()
            return redirect(url_for('expirience.all_expirience'))
    except Exception as err:
        messages_errors_conn_db(err, conn, 'error')
