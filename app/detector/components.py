from __future__ import annotations

from abc import ABC
from abc import abstractmethod
import cv2


class Component(ABC):
    """
    Abstract class for all detector components.
    """

    # def execute(self, context: Context) -> None:
    #     """
    #     Envelope method for process() at runtime.
    #     """

    #     self.context = context
    #     self.read_context()
    #     self.process()
    #     self.write_context()

    # def read_context(self) -> None:
    #     """
    #     Declares component class attributes with appropriate context variables. 
    #     """

    #     for attr, ctxt in self.config.pipeline.components.get(self.__class__.__name__).get('input').items():
    #         try:
    #             val = self.context.read(ctxt)
    #             setattr(self, attr, val)
    #         except Exception as e:
    #             raise e

    # def write_context(self) -> None:
    #     """
    #     Updates appropriate context variables with updated component class attributes.
    #     """
        
    #     for attr, ctxt in self.config.pipeline.components.get(self.__class__.__name__).get('output').items():
    #         try:
    #             val = getattr(self, attr)
    #             self.context.write(ctxt, val)
    #         except Exception as e:
    #             raise e
    
    # def initialize_configurations(self, key: str) -> None:
    #     """
    #     Initializes configuration attributes.
    #     """

    #     schema = getattr(self.config, key)
    #     for key, val in schema.__dict__.items():
    #         setattr(self, key, val) 

    @abstractmethod
    def run(self) -> None:
        """
        Main logic implemented by each component. 
        """

        raise NotImplementedError


class PreProcessor(Component):
 
    def __init__(self, scale, size, mean, swapRB, crop):  

        # static
        self.scale = scale
        self.size = size
        self.mean = mean
        self.swapRB = swapRB
        self.crop = crop

        # dynamic
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
            self.run()
            return self._blob
        return self._blob

    @image.setter
    def image(self, image):
        """
        Setter method for image.
        """

        self._image = image

    def run(self):
        self._blob = cv2.dnn.blobFromImage(
            self.image,
            self.scale,
            self.size,
            self.mean,
            self.swapRB,
            self.crop
        )


class ObjectDetector(Component):
    
    def __init__(self, model):
        
        # static
        self._model = model

        # dynamic
        self._blob = None
        self._outs = None
        self._max_confidence = 0 # return the max confidence of all desired classes

    @property
    def blob(self):
        return self._blob

    @property
    def outs(self):
        if self._outs is None:
            self.run()
        return self._outs

    @blob.setter
    def blob(self, blob):
        self._blob = blob

    def run(self):
        self._outs = self._model.compute_outputs(self._blob)


class EventSender(Component):
    
    def __init__(self, broker, threshold):

        # static
        self._broker = broker
        self._threshold = threshold

        # dynamic
        self._timestamp = None
        self._image = None
        self._outs = None
        self._event = None
        self._max_confidence = 0

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def image(self):
        return self._image

    @property
    def outs(self):
        return self._outs

    @property
    def event(self):
        if self._event is None:
            self.run()
        return self._event

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @image.setter
    def image(self, image):
        self._image = image

    @outs.setter
    def outs(self, outs):
        self._outs = outs

    def run(self):
        if self._max_confidence >= self._threshold:
            self._construct_event()
            self._broker.put(self._event)

    def _construct_event(self):
        self._event = {
            'timestamp': self._timestamp,
            'image': self._image,
            'outs': self._outs
        }