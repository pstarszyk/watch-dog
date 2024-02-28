
class Context:
    """
    Context holds variables during runtime.
    """

    def __init__(self, broker, model):
        # static variables are frame agnostic.
        self.static = {
            'broker': broker,
            'model': model
        }

        # dynamic variables are frame specific.
        self.dynamic = {}    

    def clear(self):
        """
        Clears all frame specific variables.
        """

        self.dynamic.clear()

    def read(self, key):
        """
        Reads context variable.
        """

        return self.dynamic.get(key)
    
    def write(self, key, val):
        """
        Writes variable to context.
        """

        self.dynamic.update({key: val})