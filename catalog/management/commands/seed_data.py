from django.core.management.base import BaseCommand
from catalog.models import Branch, Product, Category
from decimal import Decimal
import cloudinary.uploader
import random

class Command(BaseCommand):
    help = 'Seeds the database with initial data for all branches'
    
    def handle(self, *args, **kwargs):
        cloudinary.config(
            cloud_name='dsoa80grh',
            api_key='919418199999632',
            api_secret='TKf5nLZOi4fp0a6K_usxReaTezk',
            secure=True
        )
        
        # Upload multiple product images
        image_files = {
            'amazingday': 'media/products/Amazingdaygoldenmorn.jpg',
            'auntieb_semo': 'media/products/auntieb-semo.jpg',
            'semovita': 'media/products/Golden-Penny-Semovita-2kg.jpg',
            'twist': 'media/products/goldenpennytwist.png',
            'goldenvita': 'media/products/Goldenvita.jpg',
            'honeywellsemo': 'media/products/Honeywellsemo.webp',
            'honeywellwheat': 'media/products/honeywell.webp',
            'spaghetti': 'media/products/GP-Spaghetti-500g.png',
            'spread': 'media/products/GP-Spread-large-1.jpg',
            'indomie_chicken': 'media/products/indomie-chicken-flavour-lg.jpg',
            'knorr': 'media/products/knorrimage.webp',
            'minimie': 'media/products/minimienoodles.png',
            'noodle_goat': 'media/products/noodle_goat_meat_large.jpg',
            'noodle_jollof': 'media/products/noodles-jollof-chicken-large-1-1.jpg',
            'pasta_spaghetti': 'media/products/pasta-auntie-b-spaghetti-large-1.jpg'
        }
        
        # Upload all images and store URLs
        uploaded_images = {}
        for key, image_path in image_files.items():
            try:
                upload_result = cloudinary.uploader.upload(image_path)
                uploaded_images[key] = upload_result.get('secure_url')
                print(f"Successfully uploaded {key}: {image_path}")
            except Exception as e:
                print(f"Failed to upload {key} ({image_path}): {e}")
                uploaded_images[key] = None

        # Create categories
        categories = [
            'Semolina', 'Noodles', 'Spreads', 'Vitamins', 'Seasoning', 
            'Snacks', 'Flour', 'Pasta', 'Sugar', 'Instant Foods'
        ]
        for cat in categories:
            Category.objects.get_or_create(name=cat)

        # Create branches
        branches = [
            {
                "name": "IyanaPaja Branch", 
                "address": "331 alagba old ipaja road Agege, Opposite iyanapaja",
                "contact": "Mrs. Udoka - 07045294852"
            },
            {
                "name": "Agege Stadium Branch", 
                "address": "1 ijaye road Agege close to stadium agege",
                "contact": "Mrs. Florence - 08146085194"
            },
            {
                "name": "Ajah Branch", 
                "address": "1 ganiyu adeboyejo close, Eputu ajah",
                "contact": "Mrs. Tolu - 09035908287"
            },
        ]
        created_branches = []
        for b in branches:
            branch, _ = Branch.objects.get_or_create(
                name=b["name"], 
                address=b["address"]
            )
            created_branches.append(branch)

        products = [
            {
                "name": "Golden Penny Semovita 1kg",
                "description": "Premium semolina flour for making smooth and delicious semovita",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14650.00'),
                "unit": "1kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('semovita')
            },
            {
                "name": "Golden Penny Semovita 900g",
                "description": "Premium semolina flour for making smooth and delicious semovita",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14700.00'),
                "unit": "900g",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('semovita')
            },
            {
                "name": "Golden Penny Semovita 2kg",
                "description": "Premium semolina flour for making smooth and delicious semovita",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14600.00'),
                "unit": "2kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('semovita')
            },
            {
                "name": "Golden Penny Semovita 5kg",
                "description": "Premium semolina flour for making smooth and delicious semovita",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('7180.00'),
                "unit": "5kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('semovita')
            },
            {
                "name": "Golden Penny Semovita 10kg",
                "description": "Premium semolina flour for making smooth and delicious semovita",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14180.00'),
                "unit": "10kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('semovita')
            },
            {
                "name": "GP Noodles Chicken Flavor",
                "description": "Delicious instant noodles with authentic chicken flavor",
                "category": Category.objects.get(name="Noodles"),
                "price": Decimal('7125.00'),
                "unit": "pack",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('indomie_chicken')
            },
            {
                "name": "GP Noodles Goat Meat Flavor",
                "description": "Delicious instant noodles with authentic goat meat flavor",
                "category": Category.objects.get(name="Noodles"),
                "price": Decimal('7790.00'),
                "unit": "pack",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('noodle_goat')
            },
            {
                "name": "Golden Penny Spread 15g Sachet",
                "description": "Premium butter spread in convenient sachet packaging",
                "category": Category.objects.get(name="Spreads"),
                "price": Decimal('11500.00'),
                "unit": "15g sachet",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('spread')
            },
            {
                "name": "Golden Penny Spread 450g Sachet",
                "description": "Premium butter spread in family size sachet",
                "category": Category.objects.get(name="Spreads"),
                "price": Decimal('15400.00'),
                "unit": "450g sachet",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('spread')
            },
            {
                "name": "Golden Penny Spread 900g Sachet",
                "description": "Premium butter spread in bulk sachet packaging",
                "category": Category.objects.get(name="Spreads"),
                "price": Decimal('14400.00'),
                "unit": "900g sachet",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('spread')
            },
            {
                "name": "GoldenVita 1kg",
                "description": "Nutritious vitamin supplement for daily health",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('10950.00'),
                "unit": "1kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('goldenvita')
            },
            {
                "name": "Auntie B Semolina 1kg",
                "description": "High quality semolina flour for traditional meals",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('13500.00'),
                "unit": "1kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('auntieb_semo')
            },
            {
                "name": "Auntie B Semolina 5kg",
                "description": "High quality semolina flour for traditional meals",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('6650.00'),
                "unit": "5kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('auntieb_semo')
            },
            {
                "name": "Auntie B Semolina 10kg",
                "description": "High quality semolina flour for traditional meals",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('13080.00'),
                "unit": "10kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('auntieb_semo')
            },
            {
                "name": "Honeywell Penny Semolina 1kg",
                "description": "Premium semolina flour for making smooth and delicious semovita",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14650.00'),
                "unit": "1kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('honeywellsemo')
            },
            {
                "name": "Honeywell Penny Semolina 2kg",
                "description": "Premium semolina flour for making smooth and delicious semovita",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14650.00'),
                "unit": "2kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('honeywellsemo')
            },
            {
                "name": "Honeywell Penny Semolina 5kg",
                "description": "Premium semolina flour for making smooth and delicious semovita",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14650.00'),
                "unit": "5kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('honeywellsemo')
            },
            {
                "name": "Honeywell Penny Semolina 10kg",
                "description": "Premium semolina flour for making smooth and delicious semovita",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14650.00'),
                "unit": "10kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('honeywellsemo')
            },
            {
                "name": "Honeywell whole wheat meal 1kg",
                "description": "Premium wheat flour for making smooth and delicious wheat meal",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14650.00'),
                "unit": "1kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('honeywellwheat')
            },
            {
                "name": "Honeywell whole wheat meal 2kg",
                "description": "Premium wheat flour for making smooth and delicious wheat meal",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14650.00'),
                "unit": "2kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('honeywellwheat')
            },
            {
                "name": "Honeywell whole wheat meal 5kg",
                "description": "Premium wheat flour for making smooth and delicious wheat meal",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14650.00'),
                "unit": "5kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('honeywellwheat')
            },
            {
                "name": "Honeywell whole wheat meal 10kg",
                "description": "Premium wheat flour for making smooth and delicious wheat meal",
                "category": Category.objects.get(name="Semolina"),
                "price": Decimal('14650.00'),
                "unit": "10kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('honeywellwheat')
            },
            {
                "name": "GP Spaghettini",
                "description": "Thin spaghetti pasta for Italian dishes",
                "category": Category.objects.get(name="Pasta"),
                "price": Decimal('18400.00'),
                "unit": "pack",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('spaghetti')
            },
            {
                "name": "Minimee",
                "description": "Instant noodles perfect for quick meals",
                "category": Category.objects.get(name="Noodles"),
                "price": Decimal('7680.00'),
                "unit": "pack",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('minimie')
            },
            {
                "name": "Knorr Seasoning",
                "description": "Premium seasoning cubes for enhanced flavor",
                "category": Category.objects.get(name="Seasoning"),
                "price": Decimal('24850.00'),
                "unit": "pack",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('knorr')
            },
            {
                "name": "Chin Chin",
                "description": "Crispy and sweet traditional Nigerian snack",
                "category": Category.objects.get(name="Snacks"),
                "price": Decimal('12150.00'),
                "unit": "pack",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('twist')
            },
            {
                "name": "Tastytom Jollof",
                "description": "Ready-to-use jollof rice seasoning mix",
                "category": Category.objects.get(name="Seasoning"),
                "price": Decimal('7500.00'),
                "unit": "pack",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('noodle_jollof')
            },
            {
                "name": "Wheat Flour 4.75kg",
                "description": "Premium wheat flour for baking and cooking",
                "category": Category.objects.get(name="Flour"),
                "price": Decimal('5500.00'),
                "unit": "4.75kg",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('semovita')
            },
            {
                "name": "Jollof Hot Hot",
                "description": "Spicy jollof rice seasoning mix",
                "category": Category.objects.get(name="Seasoning"),
                "price": Decimal('6800.00'),
                "unit": "pack",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('noodle_jollof')
            },
            {
                "name": "Sugar Cube Regular",
                "description": "Premium white sugar cubes for sweetening",
                "category": Category.objects.get(name="Sugar"),
                "price": Decimal('52000.00'),
                "unit": "pack",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('semovita')
            },
            {
                "name": "Sugar Cube 500g",
                "description": "Premium white sugar cubes for sweetening",
                "category": Category.objects.get(name="Sugar"),
                "price": Decimal('17600.00'),
                "unit": "500g",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('semovita')
            },
            {
                "name": "Sugar Cube 250g",
                "description": "Premium white sugar cubes for sweetening",
                "category": Category.objects.get(name="Sugar"),
                "price": Decimal('12600.00'),
                "unit": "250g",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('semovita')
            },
            {
                "name": "Amazing Day Sachet",
                "description": "Instant meal preparation in convenient sachet",
                "category": Category.objects.get(name="Instant Foods"),
                "price": Decimal('17150.00'),
                "unit": "sachet",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('amazingday')
            },
            {
                "name": "Yum Bowl Sachet",
                "description": "Instant noodle bowl with rich flavoring",
                "category": Category.objects.get(name="Instant Foods"),
                "price": Decimal('18100.00'),
                "unit": "sachet",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('noodle_jollof')
            },
            {
                "name": "Yum Bowl Refill",
                "description": "Refill pack for Yum Bowl instant noodles",
                "category": Category.objects.get(name="Instant Foods"),
                "price": Decimal('12200.00'),
                "unit": "refill",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('noodle_jollof')
            },
            {
                "name": "Twist 200g",
                "description": "Crunchy snack perfect for any time of day",
                "category": Category.objects.get(name="Snacks"),
                "price": Decimal('9000.00'),
                "unit": "200g",
                "on_sale": False,
                "sale_price": None,
                "image": uploaded_images.get('twist')
            },
        ]
        
        # Create product variants for each branch
        for p in products:
            for branch in created_branches:
                Product.objects.get_or_create(
                    name=p["name"],
                    description=p["description"],
                    category=p["category"],
                    price=p["price"],
                    unit=p["unit"],
                    on_sale=p["on_sale"],
                    sale_price=p["sale_price"],
                    branch=branch,
                    image=p["image"]
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database with product data for all branches'))