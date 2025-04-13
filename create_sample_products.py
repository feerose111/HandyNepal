import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'handynepal.settings')
django.setup()

from app.models import Product, Artisan

def create_sample_artisans():
    """Create sample artisans if they don't exist"""
    if Artisan.objects.count() == 0:
        artisans_data = [
            {
                'first_name': 'Ram',
                'last_name': 'Bahadur',
                'artisan_type': 'woodworker',
                'description': 'Ram is a skilled woodworker from Kathmandu with over 20 years of experience crafting traditional Nepalese wooden items.',
                'location': 'Kathmandu'
            },
            {
                'first_name': 'Sita',
                'last_name': 'Sharma',
                'artisan_type': 'textile_weaver',
                'description': 'Sita specializes in traditional Nepalese textile weaving, creating beautiful pashmina shawls and other textile products.',
                'location': 'Bhaktapur'
            },
            {
                'first_name': 'Krishna',
                'last_name': 'Tamang',
                'artisan_type': 'potter',
                'description': 'Krishna is a third-generation potter from Bhaktapur, known for his traditional clay pottery techniques.',
                'location': 'Bhaktapur'
            }
        ]
        
        for data in artisans_data:
            Artisan.objects.create(**data)
        
        print(f"Created {len(artisans_data)} sample artisans")

def create_sample_products():
    """Create sample products if there are fewer than 6"""
    if Product.objects.count() < 6:
        # Get artisans
        artisans = list(Artisan.objects.all())
        if not artisans:
            print("No artisans found. Please create artisans first.")
            return
        
        # Sample product data
        products_data = [
            {
                'name': 'Handcrafted Wooden Buddha Statue',
                'description': 'This beautifully handcrafted wooden Buddha statue is made by skilled artisans in Nepal. Each piece is unique and showcases the exceptional craftsmanship that has been passed down through generations.',
                'price': Decimal('89.99'),
                'category': 'wood-crafts',
                'is_featured': True,
                'is_new': False,
                'is_bestseller': True,
                'stock': 15,
                'artisan': artisans[0]  # Ram Bahadur
            },
            {
                'name': 'Hand-carved Wooden Mandala',
                'description': 'This intricate hand-carved wooden mandala represents the universe in Hindu and Buddhist symbolism. Each piece is meticulously crafted by skilled artisans using traditional techniques.',
                'price': Decimal('65.00'),
                'category': 'wood-crafts',
                'is_featured': False,
                'is_new': False,
                'is_bestseller': False,
                'stock': 8,
                'artisan': artisans[0]  # Ram Bahadur
            },
            {
                'name': 'Carved Wooden Elephant Figurine',
                'description': 'This beautifully carved wooden elephant figurine is a symbol of good luck and prosperity in Nepalese culture. Each piece is handcrafted with attention to detail by skilled artisans.',
                'price': Decimal('45.00'),
                'discount_price': Decimal('38.25'),
                'category': 'wood-crafts',
                'is_featured': False,
                'is_new': False,
                'is_bestseller': False,
                'stock': 20,
                'artisan': artisans[0]  # Ram Bahadur
            },
            {
                'name': 'Handmade Ceramic Tea Set',
                'description': 'This elegant ceramic tea set is handcrafted by skilled potters in Nepal. The set includes a teapot and four cups, each featuring traditional Nepalese designs.',
                'price': Decimal('45.99'),
                'category': 'pottery',
                'is_featured': True,
                'is_new': False,
                'is_bestseller': False,
                'stock': 5,
                'artisan': artisans[2]  # Krishna Tamang
            },
            {
                'name': 'Traditional Clay Flower Vase',
                'description': 'This traditional clay flower vase is handcrafted using ancient pottery techniques. Each vase is unique and showcases the natural beauty of Nepalese clay.',
                'price': Decimal('35.50'),
                'category': 'pottery',
                'is_featured': False,
                'is_new': True,
                'is_bestseller': False,
                'stock': 12,
                'artisan': artisans[2]  # Krishna Tamang
            },
            {
                'name': 'Traditional Nepalese Pashmina Shawl',
                'description': 'This luxurious pashmina shawl is handwoven by skilled artisans in Nepal. Made from the finest pashmina wool, it offers exceptional softness and warmth.',
                'price': Decimal('75.00'),
                'discount_price': Decimal('60.00'),
                'category': 'textiles',
                'is_featured': True,
                'is_new': False,
                'is_bestseller': True,
                'stock': 25,
                'artisan': artisans[1]  # Sita Sharma
            }
        ]
        
        for data in products_data:
            Product.objects.create(**data)
        
        print(f"Created {len(products_data)} sample products")
    else:
        print(f"There are already {Product.objects.count()} products in the database")

if __name__ == "__main__":
    create_sample_artisans()
    create_sample_products()
    print("Sample data creation completed!") 