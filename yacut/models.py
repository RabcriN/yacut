import random
import re
import string
from datetime import datetime

from yacut import db

from .constants import (GET_UNIQUE_SHORT_ID_LENGHT, URL_PATTERN,
                        USER_CUSTOM_ID_LENGHT)
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Преобразует данные из полей и значений модели в dict"""
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data):
        """Преобразует данные из dict в поля и значения модели"""
        for field in ['url', 'custom_id']:
            if field in data:
                if field == 'url':
                    model_field = 'original'
                if field == 'custom_id':
                    model_field = 'short'
                setattr(self, model_field, data[field])

    def check_url(obj):
        """Проверяет URL на соответствие паттерну и длине,
        иначе возвращает ошибку"""
        if not re.match(URL_PATTERN, obj) or len(obj) > USER_CUSTOM_ID_LENGHT:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400
            )

    def get_unique_short_id():
        """Генерирует случайный короткий URL"""
        return ''.join(
            random.choice(string.ascii_letters + string.digits)
            for x in range(GET_UNIQUE_SHORT_ID_LENGHT)
        )

    def add_to_db(obj):
        """Добавляет объект в базу данных и делает коммит"""
        db.session.add(obj)
        db.session.commit()

    def get_short_link(short):
        """Ищет переданную короткую ссылку в базе данных и возвращает её
        либо None"""
        return URLMap.query.filter_by(short=short).first()

    def get_short_link_or_404(short):
        """Ищет переданную короткую ссылку в базе данных и возвращает её
        либо 404"""
        return URLMap.query.filter_by(short=short).first_or_404()
