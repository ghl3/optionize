

class OptionizedParameter(object):
    """
    Instances of this class represent class parameters in the Optionized
    class. They can also be used independently as a wrapper for calls to
    parser.add_option, where the arguments are chosen automatically invoking a
    little basic sense to deal with various option types, including bool and
    list.
    """
    suppress_conflict_warning = True

    def __init__(self, inst, name, default_val, short=None, help=None):
        self._default_val = default_val
        self._present_val = default_val
        self._short = short
        self._long = name
        self._help = help
        self._type = type(default_val)
        self._inst = inst

    def add_option(self, parser):
        from optparse import OptionConflictError

        def callback(option, opt_str, value, parser, *args, **kwargs):
            setattr(self._inst, self._long, kwargs.get('custom_value', value))

        short = '-' + self._short if self._short else None
        val = self._default_val
        try:
            if self._type is bool and val is False:
                parser.add_option('--' + self._long,
                                  short,
                                  default=val,
                                  metavar=val,
                                  help=self._help,
                                  action='callback',
                                  callback=callback,
                                  callback_kwargs={'custom_value': True})
            elif self._type is bool and val is True:
                parser.add_option('--no-' + self._long,
                                  short,
                                  default=val,
                                  metavar=val,
                                  help=self._help,
                                  action='callback',
                                  callback=callback,
                                  callback_kwargs={'custom_value': False})
            else:
                parser.add_option('--' + self._long,
                                  short,
                                  default=val,
                                  metavar=val,
                                  help=self._help,
                                  action='callback',
                                  callback=callback,
                                  type=type(val))
        except OptionConflictError as e:
            if not self.suppress_conflict_warning:
                print e


class OptionizedClass(object):
    """
    Classes derived from OptionizedClass will automatically add their attributes
    to an optparse.OptionParser instance when add_options is called. Those
    attributes will be modified through callbacks when the parse_args method is
    called on the parser. All attributes not starting in an underscore and
    having a type in [str, int, float, bool, list] are assumed to be command
    line options. If the attribute is a tuple whose first entry is of one of
    these types, then it is assumed to have the format

    attribute_name = (default_value, short_option, help_string)

    where either of the latter two may be None.
    """
    def __init__(self):
        self.__options = [ ]
        for k in dir(self):
            v = getattr(self, k)
            if type(v) is tuple:
                val = v[0]
                args = (self, k,) + v
                setattr(self, k, val)
            else:
                val = v
                args = (self, k, v)
            if not k.startswith('_') and type(val) in [
                str, int, float, bool, list]:
                if type(v) is tuple:
                    args = (self, k,) + v
                else:
                    args = (self, k, v)
                self.__options.append(OptionizedParameter(*args))

    def add_options(self, parser):
        """
        Populate a new group of the optparse.OptionParser instance `parser` with
        class attributes. The group name is the instance's class name.
        """
        from optparse import OptionGroup
        group = OptionGroup(parser, "problem settings for %s" %
                            self.__class__.__name__)
        for opt in self.__options:
            opt.add_option(group)
        parser.add_option_group(group)

    def report(self, first=True):
        """
        Pretty-print the class runtime parameters to standard output. Useful to
        confirm command line options have been parsed correctly.
        """
        if first:
            line1 = '\n' + ' '*4 + '%s configuration' % self.__class__.__name__
            print line1
            print ' '*4 + '-' * (len(line1) - 5) + '\n'
        for opt in self.__options:
            print ' %20s ...... %s %s' % (opt._long, getattr(self, opt._long),
                                         '('+opt._help+')' if opt._help else '')
        print '\n',
