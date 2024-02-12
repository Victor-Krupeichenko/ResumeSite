import os
from flask import flash, session, current_app
from werkzeug.utils import secure_filename


def messages_errors_conn_db(error, conn, category_error='error'):
    """
    Сообщение об ошибке при взаимодействии с базой данных
    :param error: ошибка
    :param conn: открытая сессия
    :param category_error: категория ошибки
    """
    conn.rollback()
    flash(message=f'Error: {error}', category=category_error)


def messages_errors_field(form, category_error='error'):
    """
    Сообщение об ошибке при зполнении полей формы
    :param form: форма в которой возникла ошибка
    :param category_error: категория ошибки
    """
    for field, errors in form.errors.items():
        flash(message=f'Error: field {errors.pop(0)}', category=category_error)


def set_username(form):
    """
    Сохраняем имя пользователя в сесии
    :param form:  форма из которой берем имя пользователя
    """
    username = form.username.data
    session['username'] = username


def set_path_upload_folder(img):
    """
    Устанавливает маршрут для сохранения файла
    :param img: файл из формы
    :return: строку маршрута для сохранения файла
    """
    my_path = current_app.config['UPLOAD_FOLDER'] = f'static/images/icon/skills-icon/{session.get("username")}'

    if not os.path.exists(my_path):  # Проверка существования папки, и создание, если не существует
        os.mkdir(my_path)

    filename = secure_filename(img.filename)
    img.save(os.path.join(my_path, filename))
    img_url = f'/{my_path}/{filename}'
    return img_url


def remove_images(old_image):
    """
    Удаляет старый файл изображения если изображение было обновлено на другое
    :param old_image: путь к старому изображению
    """
    filename = f'{old_image.img}'.split('/')[-1]
    my_path = current_app.config['UPLOAD_FOLDER'] = f'static/images/icon/skills-icon/{session.get("username")}'
    if os.path.exists(os.path.join(my_path, filename)):
        os.remove(os.path.join(my_path, filename))


def upload_file_resume(my_path, file):
    """
    Сохраняет файл по указанному пути
    :param my_path: путь для сохранения файла
    :param file: файл
    """

    if not os.path.exists(my_path):
        os.mkdir(my_path)
    file.save(os.path.join(my_path, file.filename))


def download_file_resume(my_path):
    """
    Загружает файл резюме
    :param my_path: путь к папке с резюме
    :return: файл резюме
    """
    for filename in os.listdir(my_path):
        if filename:
            return filename
        return {'error': 'No file'}
