
class Context:
    """
    Context holds variables during runtime.
    """

    def __init__(self, broker, model, config):
        # static variables are frame agnostic.
        self.static = {
            'broker': broker,
            'model': model,
            'config': config
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

        path = key.split('.')
        if len(path) == 1:
            return getattr(self, key)
        if path[0] == 'static':
            if path[1] == 'config':
                v = self.static['config']
                for p in path[2:]:
                    v = getattr(v, p)
                return v
            else:
                return self.static.get(path[1])
        return self.dynamic.get(path[1])


    def write(self, key, val):
        """
        Writes variable to context.
        """

        self.dynamic.update({key: val})
