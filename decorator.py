import functools
import inspect

def typesafe(func):
	"""
    Creates a decorator that processes annotations for each argument passed
    into its target function, raising an exception if there's a problem.

    @typesafe
	def test(a:int, b:int) -> int:
		return a + b

	test(2, b=3)

    """
	@functools.wraps(func)
	def wrapper(*args, **kwargs):

		spec = inspect.getfullargspec(func)
		annotations = spec.annotations
		explicit_args = dict(zip(spec.args, args))
		error = "Wrong type for %s: expected %s, got %s."

		for name, annotation in annotations.items():
			if name in annotations and not isinstance(annotation, type):
				raise TypeError("The annotation for '%s' is not a type." % name)

		for name, arg in kwargs.items():
			if name in annotations and not isinstance(arg, annotations.get(name)):
				raise TypeError(error % (name,
                                    annotations[name].__name__,
                                    type(arg).__name__))

		for name, arg in explicit_args.items():
			if name in annotations and not isinstance(arg, annotations.get(name)):
				raise TypeError(error % (name,
                                     annotations[name].__name__,
                                     type(arg).__name__))
		r = func(*args, **kwargs)
		if 'return' in annotations and not isinstance(r, annotations.get('return')):
				raise TypeError(error % ('the return value',
									annotations.get('return').__name__,
									type(r).__name__))
	return wrapper