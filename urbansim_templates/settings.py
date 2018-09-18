global pipe
pipe = {}

def register_modules(d):
	"""
	Take a dictionary with modules/class loaded so far
	and store them into a global variable pipe
	that can be shared across the whole packages"
	
	"""
	for key in d.keys():
		pipe[key] = d[key]