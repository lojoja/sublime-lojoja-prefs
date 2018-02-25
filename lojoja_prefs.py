import sublime

PACKAGE_NAME = '~lojojaPrefs'
SETTINGS_FILE = 'Package Control.sublime-settings'


def plugin_loaded():
    """ Force an update of the Package Control `installed_packages` list. """
    try:
        from package_control import events
    except ImportError:
        print('~lojojaPrefs failed to import `package_control.events`. Aborting `installed_packages` updated.')
        return

    if events.install(PACKAGE_NAME) or events.post_upgrade(PACKAGE_NAME):
        settings = sublime.load_settings(SETTINGS_FILE)

        i_pkgs = settings.get('installed_packages', [])
        u_pkgs = settings.get('uninstalled_packages', [])
        i_pkgs = [p for p in i_pkgs if p not in u_pkgs]

        settings.set('installed_packages', i_pkgs)
        sublime.save_settings(SETTINGS_FILE)
