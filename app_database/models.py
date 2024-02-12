from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin


class Base(DeclarativeBase):
    """Базовая модель"""
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base, UserMixin):
    """Модель таблицы User"""

    __tablename__ = "users"
    username: Mapped[str]
    password: Mapped[str]
    about_me: Mapped[str]
    # experiences: Mapped[list['Experience']] = relationship(back_populates='user', lazy='joined')
    # skills: Mapped[list['Skill']] = relationship(back_populates='user', lazy='joined')
    experiences: Mapped[list['Experience']] = relationship(
        back_populates='user',
        # lazy='joined', # Лучше указать в самом запросе (чтобы было явно)
        # primaryjoin='and_(User.id == Experience.user_fk, Experience.published == True)'
    )
    skills: Mapped[list['Skill']] = relationship(
        back_populates='user',
        # lazy='joined', # Лучше указать в самом запросе (чтобы было явно)
        # primaryjoin='and_(User.id == Skill.user_fk, Skill.published == True)'
    )


class Experience(Base):
    """Модель таблицы Experience"""

    __tablename__ = "experience"
    year_start: Mapped[int]
    year_finish: Mapped[int | None]
    company: Mapped[str]
    job: Mapped[str]
    description: Mapped[str]
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    user: Mapped['User'] = relationship(back_populates='experiences')
    published: Mapped[bool] = mapped_column(default=False)


class Skill(Base):
    """Модель таблицы Skill"""

    __tablename__ = "skills"
    title: Mapped[str]
    img: Mapped[str | None]
    description: Mapped[str]
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    user: Mapped['User'] = relationship(back_populates='skills')
    published: Mapped[bool] = mapped_column(default=False)
