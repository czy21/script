from cerberus import Validator, errors

from cerberus import Validator

class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REQUIRED_FIELD.code] = '必填'
    messages[errors.BAD_TYPE.code] = '类型错误'


schema = {'name': {'type': 'string', 'required': True}}
document = {}
v = Validator(schema, error_handler=CustomErrorHandler)
v.validate(document)
print(v.errors)
