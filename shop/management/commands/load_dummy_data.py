from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Product, Feedback
import csv
from pathlib import Path

class Command(BaseCommand):
    help = "Load dummy products and interactions from data/*.csv"

    def handle(self, *args, **options):
        base = Path.cwd()
        data_dir = base / "data"
        prod_file = data_dir / "dummy_products.csv"
        inter_file = data_dir / "dummy_interactions.csv"

        if not prod_file.exists():
            self.stdout.write(self.style.ERROR(f"{prod_file} not found"))
            return

        with prod_file.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                p, created = Product.objects.get_or_create(
                    title=row["title"],
                    defaults={
                        "description": row.get("description", ""),
                        "price": row.get("price") or 0,
                        "category": row.get("category", ""),
                    },
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f"Loaded {count} products"))

        if inter_file.exists():
            with inter_file.open(encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    username = row["username"]
                    user, _ = User.objects.get_or_create(username=username)
                    prod_title = row["product_title"]
                    try:
                        product = Product.objects.get(title=prod_title)
                    except Product.DoesNotExist:
                        continue
                    liked = row["liked"] in ("1", "true", "True")
                    Feedback.objects.update_or_create(user=user, product=product, defaults={"liked": liked})
            self.stdout.write(self.style.SUCCESS("Loaded interactions"))
        else:
            self.stdout.write(self.style.WARNING("No interactions file found"))
