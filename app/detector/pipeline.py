import time
from importlib import import_module


class Pipeline:
    """
    Pipeline orchestrator. 
    """

    def __init__(self, context, config):
        self.context = context
        self.config = config
        self.components = []
        self.error = False
        self.create_pipeline()

    def create_pipeline(self):
        """
        Creates sequential pipeline of objects per config.
        """

        for component_cls, component_cfg in self.config.components.items():
            module = import_module(component_cfg['module'])
            component_cls = getattr(module, component_cls)
            init = component_cfg.get('init', None)
            component_obj = self.initialize_component(component_cls, init)
            self.components.append(component_obj)
    
    def initialize_component(self, component_cls, init):
        """
        Passes context variables to class constructor per config.
        """

        if init is None:
            return component_cls()

        kwargs = {}
        for attr, source in init.items():
            val = self.context.read(source)
            kwargs.update({attr: val})
        
        component_obj = component_cls(**kwargs)
        return component_obj

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
