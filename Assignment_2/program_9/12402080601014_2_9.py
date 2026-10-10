class Product:
    def __init__(self, product_id, name, stock, purchase, selling):
        self.product_id = product_id
        self.name = name
        self.stock = int(stock)
        self.purchase = float(purchase)
        self.selling = float(selling)

    def __add__(self, other):
        return Product(
            self.product_id,
            self.name,
            self.stock + other.stock,
            min(self.purchase, other.purchase),
            max(self.selling, other.selling)
        )

    def display(self):
        print(
            self.product_id,
            self.name,
            "stock=" + str(self.stock),
            "purchase=" + str(self.purchase),
            "selling=" + str(self.selling)
        )

def read_inventory(path):
    inventory = {}

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.split()

            if len(parts) == 5:
                product = Product(*parts)
                inventory[product.product_id] = product

    return inventory

a = read_inventory(input("Inventory A file: "))
b = read_inventory(input("Inventory B file: "))

merged = dict(a)

for product_id, product in b.items():
    if product_id in merged:
        merged[product_id] = merged[product_id] + product
    else:
        merged[product_id] = product

total = 0

for product_id in sorted(merged):
    product = merged[product_id]
    product.display()
    total += product.stock * product.selling

print("Total valuation:", total)