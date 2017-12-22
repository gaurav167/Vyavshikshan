class LocaleRegexProvider(object):
    """
    A mixin to provide a default regex property which can vary by active
    language.
    """
    def __init__(self, regex):
        # regex is either a string representing a regular expression, or a
        # translatable string (using ugettext_lazy) representing a regular
        # expression.
        self._regex = regex
        self._regex_dict = {}

    @property
    def regex(self):
        """
        Returns a compiled regular expression, depending upon the activated
        language-code.
        """
        language_code = get_language()
        if language_code not in self._regex_dict:
            if isinstance(self._regex, six.string_types):
                regex = self._regex
            else:
                regex = force_text(self._regex)
            try:
                compiled_regex = re.compile(regex, re.UNICODE)
            except re.error as e:
                raise ImproperlyConfigured(
                    '"%s" is not a valid regular expression: %s' %
                    (regex, six.text_type(e)))

            self._regex_dict[language_code] = compiled_regex
        return self._regex_dict[language_code]