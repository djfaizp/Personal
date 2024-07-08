import os
import importlib

def load_plugins(client, db):
    plugins_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(plugins_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"plugins.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, 'setup'):
                module.setup(client, db)
