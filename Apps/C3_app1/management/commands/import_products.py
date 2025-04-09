import csv
from django.core.management.base import BaseCommand
from Apps.C3_app1.models import Product

class Command(BaseCommand):
    help = 'Import product data from test_products.csv'

    def handle(self, *args, **options):
        success_count = 0
        failures = []

        try:
            with open('test_products.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for idx, row in enumerate(reader, start=1):
                    try:
                        name = row['name'].strip()
                        description = row['description'].strip()
                        price = float(row['price'])
                        reorder_threshold = int(row.get('reorder_threshold', 5))  # Optional

                        Product.objects.create(
                            name=name,
                            description=description,
                            price=price,
                            reorder_threshold=reorder_threshold
                        )
                        self.stdout.write(self.style.SUCCESS(f"[Row {idx}] ✅ Imported: {name}"))
                        success_count += 1

                    except (ValueError, TypeError) as e:
                        error = f"[Row {idx}] ❌ Invalid data: {e}"
                        failures.append(error)
                        self.stdout.write(self.style.ERROR(error))

                    except KeyError as e:
                        error = f"[Row {idx}] ❌ Missing column: {e}"
                        failures.append(error)
                        self.stdout.write(self.style.ERROR(error))

            # Summary
            self.stdout.write(self.style.SUCCESS(f"\n✅ Import complete."))
            self.stdout.write(f"✔ Successful rows: {success_count}")
            self.stdout.write(f"❌ Failed rows: {len(failures)}")

        except FileNotFoundError:
            self.stderr.write("❌ File 'test_products.csv' not found in project root.")
