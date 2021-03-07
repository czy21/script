from pymongo import MongoClient

client = MongoClient(host="mongodb://admin:***REMOVED***@192.168.2.4:27017/")

table = client["erp"]["ent_file_column_mapping"]
sd_metadata = {
    "businessType": "SD",
    "fields": [
        # {
        #     "key": "primaryKey",
        #     "column": "",
        #     "header": "销售表主键"
        # },
        {
            "key": "date",
            "column": "date",
            "header": "日期"
        },
        {
            "key": "orderDate",
            "column": "order_date",
            "header": "订单日期"
        },
        {
            "key": "distributorCode",
            "column": "distributor_code",
            "header": "经销商代码"
        },
        {
            "key": "distributorName",
            "column": "distributor_name",
            "header": "经销商名称"
        },
        {
            "key": "customerCode",
            "column": "customer_code",
            "header": "客户代码"
        },
        {
            "key": "customerName",
            "column": "customer_name",
            "header": "客户名称"
        },
        {
            "key": "customerAddress",
            "column": "customer_address",
            "header": "客户地址"
        },
        {
            "key": "productCode",
            "column": "product_code",
            "header": "产品代码"
        },
        {
            "key": "productName",
            "column": "product_name",
            "header": "产品名称"
        },
        {
            "key": "productCommonName",
            "column": "product_common_name",
            "header": "通用名"
        },
        {
            "key": "productSpecification",
            "column": "product_specification",
            "header": "产品规格"
        },
        {
            "key": "productBatchNumber",
            "column": "product_batch_number",
            "header": "产品批号"
        },
        {
            "key": "productManufactureDate",
            "column": "product_manufacture_date",
            "header": "生产日期"
        },
        {
            "key": "productIndate",
            "column": "product_indate",
            "header": "有效期"
        },
        {
            "key": "productModel",
            "column": "product_model",
            "header": "产品型号"
        },
        {
            "key": "productLine",
            "column": "product_line",
            "header": "产品线"
        },
        {
            "key": "productQuantity",
            "column": "product_quantity",
            "header": "数量"
        },
        {
            "key": "productUnit",
            "column": "product_unit",
            "header": "单位"
        },
        {
            "key": "productPrice",
            "column": "product_price",
            "header": "单价"
        },
        {
            "key": "productAmount",
            "column": "product_amount",
            "header": "金额"
        },
        {
            "key": "productManufacturer",
            "column": "product_manufacturer",
            "header": "生产厂家"
        },
        {
            "key": "saleBehavior",
            "column": "sale_behavior",
            "header": "销售行为"
        },
        {
            "key": "saleOrder",
            "column": "sale_order",
            "header": "销售单号"
        },
        {
            "key": "despatchOrder",
            "column": "despatch_order",
            "header": "发运单"
        },
        {
            "key": "subsidiaryName",
            "column": "subsidiary_name",
            "header": "子公司名称"
        },
        {
            "key": "warehouse",
            "column": "warehouse",
            "header": "仓库"
        },
        {
            "key": "supplierName",
            "column": "supplier_name",
            "header": "供应商名称"
        },
        {
            "key": "departments",
            "column": "departments",
            "header": "科室"
        },
        {
            "key": "invoiceDate",
            "column": "invoice_date",
            "header": "开票日期"
        },
        {
            "key": "taxAmount",
            "column": "tax_amount",
            "header": "税额"
        },
        {
            "key": "realRight",
            "column": "real_right",
            "header": "物权"
        },
        {
            "key": "saleCost",
            "column": "sale_cost",
            "header": "销售成本"
        },
        {
            "key": "remark",
            "column": "remark",
            "header": "销售备注"
        },
        {
            "key": "customerProvince",
            "column": "customer_province",
            "header": "客户省份"
        },
        {
            "key": "customerCity",
            "column": "customer_city",
            "header": "客户城市"
        }
    ]
}
table.drop()
table.save(sd_metadata)
