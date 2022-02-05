from abc import ABC, abstractmethod

class BaseImageStore(ABC):
    @abstractmethod
    def retrieve(self, image_name):
        pass
    
    @abstractmethod
    def store(self, path_of_image_to_store, image_name):
        pass