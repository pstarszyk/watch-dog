from __future__ import annotations

from abc import ABC
from abc import abstractmethod
import cv2

from app.runtime.detector.context import Context


class Component(ABC):
    """
    Abstract class for all detector components.
    """

    def __init__(self, config):
        self.config = config
        self.context = None
    
    def execute(self, context: Context) -> None:
        """
        Envelope method for process() at runtime.
        """

        self.context = context
        self.read_context()
        self.process()
        self.write_context()

    def read_context(self) -> None:
        """
        Declares component class attributes with appropriate context variables. 
        """

        for attr, ctxt in self.config.pipeline.components.get(self.__class__.__name__).get('input').items():
            try:
                val = self.context.read(ctxt)
                setattr(self, attr, val)
            except Exception as e:
                raise e

    def write_context(self) -> None:
        """
        Updates appropriate context variables with updated component class attributes.
        """
        
        for attr, ctxt in self.config.pipeline.components.get(self.__class__.__name__).get('output').items():
            try:
                val = getattr(self, attr)
                self.context.write(ctxt, val)
            except Exception as e:
                raise e
    
    def initialize_configurations(self, key: str) -> None:
        """
        Initializes configuration attributes.
        """

        schema = getattr(self.config, key)
        for key, val in schema.__dict__.items():
            setattr(self, key, val) 

    @abstractmethod
    def process(self) -> None:
        """
        Main logic implemented by each component. 
        """

        raise NotImplementedError


class PreProcessor(Component):
 
    def __init__(self, config):
        super().__init__(config)
        self.initialize_configurations('preprocessor_config')
        self._blob = None
        self._image = None

    @property
    def image(self):
        """
        Getter method for image.
        """

        return self._image
    
    @property
    def blob(self):
        """
        Getter method for blob.
        """

        if self._image is None:
            raise Exception("No image found.")
        if self._blob is None:
            self.process()
            return self._blob
        return self._blob

    @image.setter
    def image(self, image):
        """
        Setter method for image.
        """

        self._image = image

    def process(self):
        self._blob = cv2.dnn.blobFromImage(
            self.image,
            self.scale,
            self.size,
            self.mean,
            self.swapRB,
            self.crop
        )


class ModelScore(Component):
    ...
