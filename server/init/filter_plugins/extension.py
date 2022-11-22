class FilterModule(object):
    ''' Ansible core jinja2 filters '''

    def filters(self):
        return {
            'format_args': lambda value, pattern: pattern.format(*value),
        }
