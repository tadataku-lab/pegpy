
class TreeType(object):
  pass


class String(TreeType):
  
  def __str__(self):
    return 'Str'


class KeyValue(TreeType):
  
  __slots__ = ['inner']

  def __init__(self, inner):
    self.inner = inner
  
  def __str__(self):
    return f'{{{",".join([f"{key}: {value}" for key, value in self.inner.items()])}}}'


class Tuple(TreeType):

  __slots__ = ['inner']

  def __init__(self, inner):
    self.inner = inner
  
  def __str__(self):
    return f'{"x".join(self.inner)}'


class List(TreeType):

  __slots__ = ['inner']

  def __init__(self, inner):
    self.inner = inner
  
  def __str__(self):
    return f'List[{self.inner}]'


class Union(TreeType):

  __slots__ = ['inner']

  def __init__(self, inner):
    self.inner = inner
  
  def __str__(self):
    return f'{" | ".join(self.inner)}'


class Option(TreeType):

  __slots__ = ['inner']

  def __init__(self, inner):
    self.inner = inner
  
  def __str__(self):
    return f'Option[{self.inner}]'


class Variable(TreeType):

  __slots__ = ['T']

  def __init__(self, T):
    self.T = T
  
  def __str__(self):
    return self.T


class Error(object):

  __slots__ = ['message']

  def __init__(self, message):
    self.message = message
  
  def __str__(self):
    return self.message