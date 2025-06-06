from __future__ import annotations
import sys
import types
from pathlib import Path


def _stub_dependencies() -> None:
    """Provide minimal stand-ins for heavy optional dependencies."""
    class DummyArray(list):
        def __mul__(self, other):  # type: ignore[override]
            return DummyArray([other * x for x in self])

        __rmul__ = __mul__

    numpy_mod = types.ModuleType("numpy")

    class FInfo:
        def __init__(self, _dtype):
            self.tiny = 1e-30

    numpy_mod.finfo = lambda dtype: FInfo(dtype)  # type: ignore
    numpy_mod.ones = lambda n, *a, **k: DummyArray([1] * n)
    numpy_mod.ndarray = DummyArray
    numpy_mod.array = lambda x, *a, **k: DummyArray(list(x))
    numpy_mod.bool_ = bool

    pandas_mod = types.ModuleType("pandas")
    pandas_mod.DataFrame = type("DataFrame", (), {})

    modules: dict[str, types.ModuleType] = {
        "numpy": numpy_mod,
        "pandas": pandas_mod,
        "matplotlib": types.ModuleType("matplotlib"),
        "matplotlib.pyplot": types.ModuleType("matplotlib.pyplot"),
        "matplotlib.patches": types.ModuleType("matplotlib.patches"),
        "matplotlib.axes": types.ModuleType("matplotlib.axes"),
        "matplotlib.text": types.ModuleType("matplotlib.text"),
        "matplotlib.textpath": types.ModuleType("matplotlib.textpath"),
        "matplotlib.transforms": types.ModuleType("matplotlib.transforms"),
        "matplotlib.collections": types.ModuleType("matplotlib.collections"),
        "matplotlib.path": types.ModuleType("matplotlib.path"),
        "matplotlib.font_manager": types.ModuleType("matplotlib.font_manager"),
        "matplotlib.colors": types.ModuleType("matplotlib.colors"),
        "tqdm": types.ModuleType("tqdm"),
    }

    modules["matplotlib.patches"].Rectangle = object
    modules["matplotlib.patches"].PathPatch = object
    modules["matplotlib.axes"].Axes = object
    modules["matplotlib.text"].TextPath = object
    modules["matplotlib.textpath"].TextPath = object
    modules["matplotlib.transforms"].Affine2D = object
    modules["matplotlib.transforms"].Bbox = object
    modules["matplotlib.collections"].PatchCollection = object
    modules["matplotlib.path"].Path = object
    modules["matplotlib.colors"].to_rgb = lambda x: (0, 0, 0)
    modules["tqdm"].tqdm = lambda x, **kw: x

    for name, mod in modules.items():
        sys.modules.setdefault(name, mod)


def test_core_symbols_exist() -> None:
    _stub_dependencies()
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import logomaker_batch

    assert hasattr(logomaker_batch, "BatchLogo")
    assert hasattr(logomaker_batch, "Logo")
    assert hasattr(logomaker_batch, "get_color_dict")
