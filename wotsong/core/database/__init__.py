
from typing import List, Type
from wotsong.core.services.firebase import Firestore
from flask_sqlalchemy import SQLAlchemy, Model

from wotsong.core.utils import snake_to_camel
from marshmallow import Schema
firestore_db = Firestore()

class BaseItem(Model, object):

    schema: Schema

    def as_dict(self):
        entity = vars(self)
        return {key: entity[key] for key in entity if not key.startswith('_')}

    def as_camel_dict(self):
        return snake_to_camel(self.as_dict())

    def __repr__(self):
        repr = "<{class_name} (".format(class_name=type(self).__name__)
        dict = self.as_dict()
        return repr + "{0!r})>".format(dict)

db = SQLAlchemy(model_class=BaseItem)

def init_db(app):
    db.init_app(app)
    from .User import User
    with app.app_context():
        db.create_all()

def update_entity(entity: BaseItem, partial_data: dict) -> None:
    entity.schema.validate(partial_data, partial=True)
    for key in partial_data:
        setattr(entity, key, partial_data[key])

def create_entity(cls: Type[BaseItem], payload: dict) -> BaseItem:
    cls.schema.validate(payload)
    entity = cls(**payload)
    db.session.add(entity)
    return entity
        