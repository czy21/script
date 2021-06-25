table_template = [
    "ent_datacenter_inspect_sale_",
    "ent_datacenter_inspect_purchase_",
    "ent_datacenter_inspect_inventory_",
    "ent_datacenter_inspect_sale_day_",
    "ent_datacenter_inspect_purchase_day_",
    "ent_datacenter_inspect_inventory_day_",
]
for t in range(1, 101):
    for s in table_template:
        table=s+str(t)
        update="update "+table+" bf set bf.producer = '' where bf.producer is null;"
        print(update)
