__author__ = "Matthieu Gallet"


class RubyClass:
    def __init__(self, ruby_class_name, attributes=None):
        self.ruby_class_name = ruby_class_name
        self.attributes = attributes or {}

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.attributes == other.attributes
        )

    def __hash__(self):
        return hash(hash(self.__class__.__name__) + hash(repr(self.attributes)))

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.attributes)

    def __str__(self):
        return "%s(%r)" % (self.__class__.__name__, self.attributes)


class String:
    def __init__(self, text: str, attrs=None):
        self.text = text
        self.attributes = attrs or {}

    def __eq__(self, other):
        if isinstance(other, str):
            return self.text == other
        elif isinstance(other, String):
            return self.text == other.text and self.attributes == other.attributes
        return False

    def __hash__(self):
        return hash(self.text)

    def __repr__(self):
        return repr(self.text)

    def __str__(self):
        return self.text

    def __add__(self, other):
        return String(self.text + str(other), self.attributes)

    def __ne__(self, other):
        if isinstance(other, str):
            return self.text != other
        elif isinstance(other, String):
            return self.text != other.text or self.attributes != other.attributes
        return False

    def __lt__(self, other):
        return self.text < other

    def __gt__(self, other):
        return self.text > other

    def __le__(self, other):
        return self.text > other

    def __ge__(self, other):
        return self.text >= other

    def __iter__(self):
        yield from self.text

    def __bool__(self):
        return bool(self.text)

    def __getitem__(self, item):
        return self.text[item]

    def __len__(self):
        return len(self.text)

    def encode(self, *args, **kwargs):
        return self.text.encode(*args, **kwargs)


class Class(RubyClass):
    pass


class UsrMarshal(RubyClass):
    def __init__(self, ruby_class_name, attributes=None):
        self._private_data = None
        super().__init__(ruby_class_name, attributes=attributes)

    def marshal_load(self, private_data):
        self._private_data = private_data

    def marshal_dump(self):
        return self._private_data


class UserDef(RubyClass):
    """ object with a user-defined serialization format using the _dump instance method and _load class method.

    data is a byte sequence containing the user-defined representation of the object.

The class method _load is called on the class with a string created from the byte-sequence.
"""
    def __init__(self, ruby_class_name, attributes=None):
        self._private_data = None
        super().__init__(ruby_class_name, attributes=attributes)

    def _load(self, private_data: bytes):
        self._private_data = private_data

    def _dump(self) -> bytes:
        return self._private_data


class Object(RubyClass):
    def __init__(self, ruby_class_name, attributes):
        super().__init__(ruby_class_name, attributes)


class Extended(RubyClass):
    pass


class Module(RubyClass):
    pass


class Symbol:

    __registered_symbols__ = {}

    def __new__(cls, name):
        if name in cls.__registered_symbols__:
            return cls.__registered_symbols__[name]
        return super(Symbol, cls).__new__(cls)

    def __init__(self, name):
        self.name = name
        self.__registered_symbols__[name] = self

    def __hash__(self):
        return hash("<<<:%s:>>>" % self.name)

    def __repr__(self):
        return 'Symbol("%s")' % self.name

    def __str__(self):
        return ":%s" % self.name

    def encode(self, *args, **kwargs):
        return self.name.encode(*args, **kwargs)
