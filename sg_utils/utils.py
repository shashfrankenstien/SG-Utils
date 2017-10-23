import string, random

class dotdict(dict):
	"""dot.notation access to dictionary attributes"""
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__



def giberish(size=64):
    """Generates salt for password encryption"""
    alph = str(string.lowercase+string.digits)*2
    return str(''.join(random.sample(alph, size)))