import abc
from typing import List, Tuple

from peewee import fn, DoesNotExist

from utils import make_password


class ApiAimoFacade(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def all(self):
        pass

    @abc.abstractmethod
    def last(self):
        pass

    @abc.abstractmethod
    def create(self, data):
        pass


class ApiAimoBridge(ApiAimoFacade):

    def __init__(self, model):
        self.model = model

    @property
    def all(self):
        return

    @all.getter
    def all(self) -> list:
        all = self.model.select()
        return all

    def ids_item(self, values: List[int]):
        model = self.model
        items = model.select().where(model.id << values)
        return items

    def wheres(self, wheres):
        model = self.model
        try:
            items = model.select().where(wheres)
            return items
        except DoesNotExist:
            return {"error": "Not Found"}
        except  Exception as e:
            raise e

    @property
    def last(self):
        return

    @last.getter
    def last(self):
        try:
            last = self.model.select().order_by(self.model.id.desc()).get()
            return last
        except self.model.DoesNotExist:
            return []
        except Exception as e:
            raise e

    def create(self, data):
        try:
            if 'password' in data:
                data['password'] = make_password(data['password'])
            model = self.model(**data)
            model.save()
            return model
        except Exception as e:
            raise e

    def create_bulk(self, data):
        database = self.model.__dict__["_meta"].__dict__['database']
        with database.atomic():
            for data_dict in data:
                if 'password' in data_dict:
                    data_dict['password'] = make_password(data_dict['password'])
                self.model.create(**data_dict)
