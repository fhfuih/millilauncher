"""
An object to handle a single Minecraft version file.
"""
from string import Template
from .mclibrary import MCLibrary

class MCVersion(object):
    """
    An object to handle a single Minecraft version file.
    """
    def __init__(self, d):
        """
        Initialize a MCVersion object by a dict parsed from <version>.json
        """
        self.id = d['id']
        self.assets = d.get('assets')
        self.jar = d.get('jar', self.id)
        self.main_class = d.get('mainClass')
        self.minecraft_arguments = d.get('minecraftArguments')
        if self.minecraft_arguments:
            self.minecraft_arguments = Template(self.minecraft_arguments)

        self.libraries = []
        self.extract = []
        for obj in d.get('libraries', []):
            lib = MCLibrary(obj)
            if lib.allow:
                self.libraries.append(lib)
                if lib.exclude:
                    self.extract.append(lib)

        self.inherits_from = d.get('inheritsFrom')

    def inherit(self, parent):
        """
        Check if this version has parent, and inherit its data if so.
        This function is called on invoking MCVersionsList.get()
        """
        if not parent or not self.inherits_from:
            return False
        if parent.id == self.id:
            raise ValueError('Self-inheritance attempt')
        else:
            self.inherits_from = parent.inherits_from
            if not self.minecraft_arguments:
                self.minecraft_arguments = parent.minecraft_arguments
            if not self.assets:
                self.assets = parent.assets
            if not self.jar:
                self.jar = parent.jar
            if not self.main_class:
                self.main_class = parent.main_class
            self.libraries += parent.libraries
            self.extract += parent.extract
            return True
