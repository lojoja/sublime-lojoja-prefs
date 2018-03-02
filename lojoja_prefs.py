import sublime

PACKAGE_NAME = '~lojojaPrefs'
SETTINGS_FILE = '{}.sublime-settings'.format(PACKAGE_NAME)
PACKAGE_CONTROL_SETTINGS_FILE = 'Package Control.sublime-settings'
SETTINGS_MAP = [
    {
        'current': 'install_prereleases',
        'enabled': 'prerelease_packages',
        'disabled': 'disabled_prerelease_packages'
    },
    {
        'current': 'installed_packages',
        'enabled': 'packages',
        'disabled': 'disabled_packages'
    }
]


def write_console(msg):
    print('{}: {}'.format(PACKAGE_NAME, msg))


def get_packages(current, enable, disable):
    return sort_packages(set(current + enable).difference(disable))


def sort_packages(packages):
    return sorted(packages, key=str.lower)


def plugin_loaded():
    """ Actions to run when plugin is loaded. """

    # Manage packages
    write_console('Checking package lists')

    settings = sublime.load_settings(SETTINGS_FILE)
    package_control_settings = sublime.load_settings(PACKAGE_CONTROL_SETTINGS_FILE)

    DEBUG = settings.get('debug', False)

    changed = False
    for keys in SETTINGS_MAP:
        current = package_control_settings.get(keys['current'], [])
        if DEBUG:
            write_console('Current "{0}" package list: {1}'.format(keys['current'], current))

        updated = get_packages(current,
                               settings.get(keys['enabled'], []),
                               settings.get(keys['disabled'], []))
        if DEBUG:
            write_console('New "{0}" package list: {1}'.format(keys['current'], updated))

        if sort_packages(current) != updated:
            changed = True
            package_control_settings.set(keys['current'], updated)
            write_console('Updated "{}" package list'.format(keys['current']))
        else:
            write_console('"{}" package list already up to date'.format(keys['current']))

    if changed:
        sublime.save_settings(PACKAGE_CONTROL_SETTINGS_FILE)
