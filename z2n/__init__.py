from pkg_resources import get_distribution, DistributionNotFound

__project__ = 'z2n-periodogram'
__version__ = None
__license__ = 'MIT'
__author__ = 'Yohan Alexander'
__copyright__ = 'Copyright (C) 2020, Z2n Software, by Yohan Alexander.'
__description__ = 'A program for interative periodograms analysis.'
__maintainer__ = 'Yohan Alexander'
__email__ = 'yohanfranca@gmail.com'
__status__ = 'Development'
__credits__ = 'Yohan Alexander'
__docs__ = 'https://z2n-periodogram.readthedocs.io'
__url__ = 'https://github.com/yohanalexander/z2n-periodogram'
__z2n__ = '''
        Z2n Software, a program for interactive periodograms analysis.
        Copyright (C) 2020, and MIT License, by Yohan Alexander [UFS].
        Type "help" for more information or "docs" for documentation.
        '''
__plt__ = '''
        Interactive plotting window of the Z2n Software.
        Type "help" for more information.
        '''

try:
    __version__ = get_distribution(__project__).version
except DistributionNotFound:
    VERSION = __project__ + '-' + '(local)'
else:
    VERSION = __project__ + '-' + __version__
    from z2n.plot import Plot
    from z2n.series import Series
