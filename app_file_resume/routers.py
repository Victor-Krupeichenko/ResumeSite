import os

from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, flash
from app_file_resume.forms import ResumeFileForm
from flask_login import login_required
from app_utils.utils import upload_file_resume, messages_errors_field, download_file_resume

router_file = Blueprint('files', __name__, template_folder='templates', static_folder='static')

path = f'app_file_resume/'


@router_file.route('/upload-file', methods=['GET', 'POST'])
@login_required
def upload_file():
    """
    Маршрут загрузки файла резюме
    """

    form = ResumeFileForm()
    response = {
        'upload_file': True
    }
    if form.validate_on_submit():
        file = request.files['file']
        type_file = file.filename.split('.')[-1].lower()
        match type_file:
            case 'docx':
                my_path = f'{path}{type_file}'
                upload_file_resume(my_path, file)
                return redirect(url_for('hello_world'))
            case 'pdf':
                my_path = f'{path}{type_file}'
                upload_file_resume(my_path, file)
                return redirect(url_for('hello_world'))
    else:
        messages_errors_field(form, 'error')
    return render_template('create_or_login_user.html', form=form, response=response)


@router_file.route('/download-file/<path:filename>', methods=['GET'])
def download_file(filename):
    """
    Марщрут чтобы скачать файл
    :param filename: путь к файлу
    """
    new_path = os.path.join(path, filename)
    try:
        my_file = download_file_resume(new_path)
        if not isinstance(my_file, dict):
            return send_from_directory(new_path, my_file, as_attachment=True)
    except Exception as e:
        flash(message=f'error: {e}', category='error')
