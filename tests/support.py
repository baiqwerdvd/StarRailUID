"""Load a plugin module without starting the bot framework."""

import importlib.util
from pathlib import Path
import sys
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def stub_module(name, **attributes):
    module = ModuleType(name)
    module.__dict__.update(attributes)
    return module


def load_module(relative_path, stubs=None):
    path = ROOT / relative_path
    parts = Path(relative_path).with_suffix("").parts
    name = ".".join(parts)
    modules = dict(stubs or {})
    for index in range(1, len(parts)):
        package = ".".join(parts[:index])
        mod = stub_module(package)
        mod.__path__ = [str(ROOT.joinpath(*parts[:index]))]
        modules.setdefault(package, mod)
    for imported in list(modules):
        components = imported.split(".")
        for index in range(1, len(components)):
            package = ".".join(components[:index])
            if package not in modules and package not in sys.modules:
                mod = stub_module(package)
                mod.__path__ = []
                modules[package] = mod
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    modules[name] = module
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    return module
