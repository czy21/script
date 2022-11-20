class FilterModule(object):
    ''' Ansible core jinja2 filters '''

    def filters(self):
        return {
            'format': lambda val, pattern: pattern.format(*val),
        }
