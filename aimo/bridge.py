import abc
from typing import List

from peewee import fn


class ApiAimoFacade(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def all(self):
        pass


class ApiAimoBridge(ApiAimoFacade):

    def __init__(self, model):
        self.model = model

    def __objs_to_list(self, obj):
        items = [item.__dict__['_data'] for item in obj]
        return items

    @property
    def all(self):
        return

    @all.getter
    def all(self) -> list:
        all = self.model.select()
        all_data = self.__objs_to_list(all)
        return all_data

    def ids_item(self, values: List[int]):
        model = self.model
        items = model.select().where(model.id << values)
        all_data = self.__objs_to_list(items)
        return all_data

    @property
    def last(self):
        return

    @last.getter
    def last(self):
        try:
            last = self.model.select().order_by(self.model.id.desc()).get()
            return last.__dict__['_data']
        except self.model.DoesNotExist:
            return []
        except Exception as e:
            raise e

