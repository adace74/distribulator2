import string
from os import sep
s = string
d = s.join(s.split(__file__, sep)[:-1], sep)+sep
_ = lambda f: s.rstrip(open(d+f).read())

try:
    __doc__ = _('README')
except:
    pass
