import time
from importlib import import_module


class Pipeline:
    """
    Pipeline orchestrator. 
    """

    def __init__(self, config, context):
        self.config = config 
        self.context = context
        self.components = []
        self.error = False
        self.create_pipeline()

    def create_pipeline(self):
        """
        Creates pipeline defined by config.
        """

        for component_cls, component_cfg in self.config.pipeline.components.items():
            module = import_module(component_cfg['module'])
            component_cls = getattr(module, component_cls)
            component_obj = component_cls(self.config)
            self.components.append(component_obj)

    def run(self, image):
        """
        Run sequential pipeline on image input.
        """

        self.context.clear()
        self.context.write('image', image)
        self.context.write('timestamp', int(1e3 * time.time()))

        for component in self.components:
            try:
                # run full pipeline on input image frame.
                component.execute(self.context)
            except:
                # If error, just return and go to next frame.
                return