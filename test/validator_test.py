from cerberus import Validator, errors


class CustomErrorHandler(errors.BasicErrorHandler):
    messages = errors.BasicErrorHandler.messages.copy()
    messages[errors.REQUIRED_FIELD.code] = '必填'
    messages[errors.BAD_TYPE.code] = '类型错误'


schema = {'*你是': {'type': 'string', 'required': True}}
document = {'*你是': 55}
v = Validator(schema, error_handler=CustomErrorHandler)
v.validate(document, schema)
print(v.errors)
