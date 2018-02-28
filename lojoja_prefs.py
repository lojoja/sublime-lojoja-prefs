import sublime

PACKAGE_NAME = '~lojojaPrefs'
LP_SETTINGS_FILE = '{}.sublime-settings'.format(PACKAGE_NAME)
PC_SETTINGS_FILE = 'Package Control.sublime-settings'


def plugin_loaded():
    """ Force an update of the Package Control `installed_packages` list. """
    try:
        from package_control import events
    except ImportError:
        print('[{}] Failed to import `package_control.events`. Aborting `installed_packages` updated.'.format(PACKAGE_NAME))
        return

    if events.install(PACKAGE_NAME) or events.post_upgrade(PACKAGE_NAME):
        lp_settings = sublime.load_settings(LP_SETTINGS_FILE)
        pc_settings = sublime.load_settings(PC_SETTINGS_FILE)

        i_pkgs = pc_settings.get('installed_packages', [])
        u_pkgs = lp_settings.get('uninstalled_packages', [])
        i_pkgs = [p for p in i_pkgs if p not in u_pkgs]

        pc_settings.set('installed_packages', i_pkgs)
        sublime.save_settings(PC_SETTINGS_FILE)

        print('[{}] Installed Package list updated'.format(PACKAGE_NAME))
