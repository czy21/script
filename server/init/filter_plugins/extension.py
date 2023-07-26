class FilterModule(object):
    ''' Ansible core jinja2 filters '''

    def filters(self):
        return {
            'format_args': lambda value, pattern: pattern.format(value) if isinstance(value, str) else pattern.format(*value),
        }