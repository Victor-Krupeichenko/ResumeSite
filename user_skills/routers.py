from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app_database.connect import session_maker
from .forms import SkillForm
from app_database.models import Skill
from app_utils.utils import messages_errors_field, messages_errors_conn_db, set_path_upload_folder, remove_images
from sqlalchemy import select


skills = Blueprint('skills', __name__, template_folder='templates', static_folder='static')


@skills.route('/create-skill', methods=['GET', 'POST'])
@login_required
def create_skill():
    """
    Добавление нового навыка
    """

    form = SkillForm()
    response = {
        'skills': True
    }
    if form.validate_on_submit():
        form_data = form.data
        img = form_data['img']
        if img:
            img_url = set_path_upload_folder(img)
        else:
            img_url = None
        try:
            with session_maker() as conn:
                new_skill = Skill(
                    title=form_data['title'],
                    img=img_url,
                    description=form_data['description'],
                    published=form_data['published'],
                    user_fk=current_user.id
                )
                conn.add(new_skill)
                conn.commit()
                return redirect(url_for('skills.all_skills'))
        except Exception as err:
            messages_errors_conn_db(err, conn, 'error')
    else:
        messages_errors_field(form, 'error')
    return render_template('create_or_login_user.html', form=form, response=response)


@skills.route('/all-skills', methods=['GET'])
@login_required
def all_skills():
    """
    Показать все навыки
    """
    try:
        with session_maker() as conn:
            query = select(Skill).filter_by(user_fk=current_user.id)
            res = conn.execute(query)
            result = res.scalars().all()
            is_empty = False if result else True
    except Exception as err:
        messages_errors_conn_db(err, conn, 'error')
    return render_template('all_skills.html', result=result, is_empty=is_empty)


@skills.route('/update_skill/<int:skill_id>', methods=['GET', 'POST'])
@login_required
def update_skill(skill_id):
    """
    Обновляет новык
    :param skill_id: id записи в базе данных
    """

    response = {
        'update_skill': True
    }
    try:
        with session_maker() as conn:
            query = select(Skill).filter_by(id=skill_id)
            res = conn.execute(query)
            old_skill = res.scalars().first()
            form = SkillForm(obj=old_skill)
            if form.validate_on_submit():
                form_data = form.data
                img = form_data['img']
                img_url = set_path_upload_folder(img) if img else None
                if img_url:
                    remove_images(old_skill)  # Удаляет старый файл изображеня
                else:
                    img_url = old_skill.img
                old_skill.title = form_data['title'],
                old_skill.description = form_data['description'],
                old_skill.published = form_data['published']
                old_skill.img = img_url
                conn.commit()
                flash(message='Update Skill Successful', category='success')
                return redirect(url_for('skills.all_skills'))
            else:
                messages_errors_field(form, 'erro')
    except Exception as err:
        messages_errors_conn_db(err, conn, 'error')
    return render_template('create_or_login_user.html', form=form, response=response)


@skills.route('/delete-skill/<int:skill_id>', methods=['GET'])
@login_required
def delete_skill(skill_id):
    """
    Удаляет навык
    :param skill_id: id записи в базе данных
    """
    try:
        with session_maker() as conn:
            query = select(Skill).filter_by(id=skill_id)
            res = conn.execute(query)
            remove_skill = res.scalars().first()

            if remove_skill.img:
                remove_images(remove_skill)   # Удаления файла изображения из хранилища

            conn.delete(remove_skill)
            conn.commit()

            return redirect(url_for('skills.all_skills'))
    except Exception as err:
        messages_errors_conn_db(err, conn, 'error')
