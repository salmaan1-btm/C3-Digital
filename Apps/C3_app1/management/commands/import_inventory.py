import csv
from django.core.management.base import BaseCommand
from Apps.C3_app1.models import Product, Dealership

class Command(BaseCommand):
    help = 'Import products from test_inventory.csv'

    def handle(self, *args, **options):
        success_count = 0
        failures = []

        try:
            with open('test_inventory.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for idx, row in enumerate(reader, start=1):
                    try:
                        dealership_name = row['dealership'].strip()
                        dealership = Dealership.objects.get(name=dealership_name)
                        stock = int(row['stock'])
                        price = float(row['price'])

                        Product.objects.create(
                            name=row['name'],
                            description=row['description'],
                            stock=stock,
                            price=price,
                            dealership=dealership
                        )
                        self.stdout.write(self.style.SUCCESS(f"[Row {idx}] Imported: {row['name']}"))
                        success_count += 1

                    except Dealership.DoesNotExist:
                        error = f"[Row {idx}] ❌ Dealership '{row['dealership']}' not found."
                        failures.append(error)
                        self.stdout.write(self.style.ERROR(error))

                    except (ValueError, TypeError) as e:
                        error = f"[Row {idx}] ❌ Invalid number format: {e}"
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
            self.stderr.write("❌ File 'test_inventory.csv' not found in project root.")
