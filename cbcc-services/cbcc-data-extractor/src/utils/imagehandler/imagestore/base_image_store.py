from abc import ABC, abstractmethod

class BaseImageStore(ABC):
    @abstractmethod
    def retrieve(self, path_to_image_location):
        pass
    
    @abstractmethod
    def store(self, path_of_image_to_store):
        pass