from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField, SubmitField
from wtforms.validators import ValidationError

ALLOWED_EXTENSIONS = {'docx', 'pdf'}


def allowed_file(filename):
    """
    Проверяет на что файл допустимого формата
    :param filename: имя файла
    :return: bool
    """
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


class ResumeFileForm(FlaskForm):
    """
    Форма для загрузки файла резюме
    """
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Load Resume')

    def validate_file(self, field):
        """
        Валидирует поля загрузки файла
        :param field: файл
        """
        if not allowed_file(field.data.filename):
            raise ValidationError('Недопустимый формат файла. Разрешены только файлы с расширениями .docx и .pdf')
