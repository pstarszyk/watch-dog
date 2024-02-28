from abc import ABC
from abc import abstractmethod

import cv2


class Component(ABC):
    """
    Abstract class for all detector components.
    """

    def __init__(self, config):
        self.config = config
        self.context = None

    
    def execute(self, context):
        """
        Envelope method for process() at runtime.
        """

        self.context = context
        self.read_context()
        self.process()
        self.write_context()

    def read_context(self):
        """
        Declares component class attributes with appropriate context variables. 
        """

        for attr, ctxt in self.config.pipeline.components.get(self.__class__.__name__).get('input').items():
            try:
                val = self.context.read(ctxt)
                setattr(self, attr, val)
            except Exception as e:
                raise e


    def write_context(self):
        """
        Updates appropriate context variables with updated component class attributes.
        """
        
        for attr, ctxt in self.config.pipeline.components.get(self.__class__.__name__).get('output').items():
            try:
                val = getattr(self, attr)
                self.context.write(ctxt, val)
            except Exception as e:
                raise e


    @abstractmethod
    def process(self):
        """
        Main logic implemented by each component. 
        """

        raise NotImplementedError


class PreProcessor(Component):
    
    scale:  float = 1.0/255
    size:   tuple = (416, 416)
    mean:   tuple = (0, 0, 0)
    swapRB: bool  = True
    crop:   bool  = False

    def __init__(self):
        self._blob = None
        self._image = None        

    @property
    def image(self):
        return self._image

    @property
    def blob(self):
        if self._image is None:
            print("Input Image.")
        if self._blob is None:
            self.process()
            return self._blob
        return self._blob

    @image.setter
    def image(self, image):
        self._image = image

    @blob.setter
    def blob(self, blob):
        self._blob = blob

    def process(self):
        self.blob = cv2.dnn.blobFromImage(
            self.image,
            self.scale,
            self.size,
            self.mean,
            self.swapRB,
            self.crop
        )


class ModelScore(Component):
    ...

