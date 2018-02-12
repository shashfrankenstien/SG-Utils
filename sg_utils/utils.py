import string, random, sys

class dotdict(dict):
	"""dot.notation access to dictionary attributes"""
	
	def __getattr__(self, attr):
		if attr.startswith('__'):
			raise AttributeError
		return self.get(attr, None)
	
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__


def iterdict(d):
	if sys.version_info.major==3:
		return d.items()
	else:
		return d.iteritems()


def giberish(size=64):
	"""Generates salt for password encryption"""
	alph = str(string.lowercase+string.digits)*2
	return str(''.join(random.sample(alph, size)))
