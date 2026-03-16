from argostranslate import package, translate

_loaded = False

def _load():
    global _loaded
    if _loaded:
        return
    print("Loading argostranslate no→en package...")
    package.update_package_index()
    available = package.get_available_packages()
    pkg = next(p for p in available if p.from_code == "nb" and p.to_code == "en")
    package.install_from_path(pkg.download())
    _loaded = True
    print("Package installed.")

def translate_no_en(text):
    _load()
    installed = translate.get_installed_languages()
    no = next(l for l in installed if l.code == "nb")
    en = next(l for l in installed if l.code == "en")
    return no.get_translation(en).translate(text)
