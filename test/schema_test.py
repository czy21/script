import json
import pathlib
import re


def name_convert_to_camel(name: str) -> str:
    """下划线转驼峰(小驼峰)"""
    return re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name)


def sql_type_to_java_type(val):
    if "varchar" in val:
        return "java.lang.String"
    if "datetime" in val:
        return "java.time.LocalDateTime"
    if "date" in val:
        return "java.time.LocalDate"
    if "decimal" in val:
        return "java.math.BigDecimal"
    if "bigint" in val:
        return "java.lang.Long"
    if "int" in val:
        return "java.lang.Integer"


'''
SELECT CONCAT(JSON_OBJECT('column_name',column_name,'column_comment',column_comment,'column_type',column_type),",") as a
from information_schema.COLUMNS
where table_name = 'budget_cost_year_med_detail'
  and column_name not in ('delete_flag','create_user','create_time','update_user','update_time')
'''


def generate_config(file: pathlib.Path):
    columns = []
    for t in json.loads(file.read_text()):
        column = {}
        column["name"] = name_convert_to_camel(t.get("column_name"))
        column["desc"] = t.get("column_comment")
        column["javaType"] = sql_type_to_java_type(t.get("column_type"))
        column["schemaSuffix"] = "detail"
        columns.append(column)
    print(json.dumps(columns, indent=2, ensure_ascii=False))


def generate_template(file: pathlib.Path, is_import: bool = False, exclude_fields: list = None):
    cfg = json.loads(file.read_text())
    for t in sorted(cfg.get("fields"), key=lambda k: k.get("sort", 0)):
        if t.get("name") not in exclude_fields:
            field_content = []
            head = t.get("heads", [t.get("desc")])
            if not t.get("heads") and t.get("required"):
                head[-1] = "*"+head[-1]
            if is_import and t.get("required"):
                field_content.append("@NotBlank(message = \"{0}不能为空\")".format(head[-1].replace("*", "")))
            field_content.append("@ExcelProperty(value = {{{0}}} {1})".format(",".join(["\"{0}\"".format(a) for a in head]), ",converter = BigDecimalNumberConverter.class" if not is_import and t.get('javaType') in ['java.math.BigDecimal'] else ""))
            field_content.append(f"private {str(t.get('javaType')).split('.')[2] if not is_import and t.get('javaType') in ['java.math.BigDecimal'] else 'String'} {t.get('name')};\n")
            print("\n".join(field_content))
    if is_import:
        print("@ExcelProperty(value = {\"错误信息\"}) \nprivate String message;")


if __name__ == '__main__':
    schema = pathlib.Path(__file__).parent.joinpath("build/columns.json")
    generate_config(schema)
    print("===========================\n")
    config = pathlib.Path(__file__).parent.joinpath("build/config.json")
    generate_template(config, True, exclude_fields=["id", "domain", "baseId", "dataStatus", "dataVersion"])
