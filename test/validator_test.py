from cerberus import Validator, errors


from cerberus import Validator

class MyValidator(Validator):
    def _check_with_oddity(self, field, value):
        if not value & 1:
            self._error(field, "Must be an odd number")

schema = {'amount': {'check_with': 'oddity', 'type': 'integer'}}

v = MyValidator(schema)

v.validate({'amount': 3})
print(v.errors)