from decimal import Decimal
from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seeds database with realistic sample categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding categories and products...')

        categories_data = [
            {
                'name': 'Electronics',
                'slug': 'electronics',
                'icon': '💻',
                'description': 'Laptops, headphones, smart devices, and accessories.'
            },
            {
                'name': 'Fashion',
                'slug': 'fashion',
                'icon': '👕',
                'description': 'Trendy apparel, jackets, shoes, and luxury wear.'
            },
            {
                'name': 'Home & Living',
                'slug': 'home-living',
                'icon': '🛋️',
                'description': 'Modern furniture, kitchenware, and home decor.'
            },
            {
                'name': 'Fitness & Sports',
                'slug': 'fitness-sports',
                'icon': '⚡',
                'description': 'Workout gear, smart fitness wearables, and sporting equipment.'
            },
        ]

        categories = {}
        for cdata in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cdata['slug'],
                defaults={
                    'name': cdata['name'],
                    'icon': cdata['icon'],
                    'description': cdata['description']
                }
            )
            categories[cdata['slug']] = cat

        products_data = [
            # Electronics
            {
                'category': categories['electronics'],
                'name': 'AeroSound Pro Wireless Headphones',
                'slug': 'aerosound-pro-wireless-headphones',
                'description': 'Premium noise-cancelling wireless headphones with 40-hour battery life, immersive spatial audio, and ultra-plush memory foam earcups.',
                'price': Decimal('199.99'),
                'stock': 25,
                'rating': Decimal('4.8'),
                'rating_count': 124,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80',
            },
            {
                'category': categories['electronics'],
                'name': 'Nova UltraBook 15 Pro',
                'slug': 'nova-ultrabook-15-pro',
                'description': 'Feather-light aluminum laptop powered by a 12-core processor, stunning 4K OLED display, and all-day battery life for creators and professionals.',
                'price': Decimal('1149.00'),
                'stock': 12,
                'rating': Decimal('4.9'),
                'rating_count': 89,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80',
            },
            {
                'category': categories['electronics'],
                'name': 'PulseTrack Smartwatch Gen 4',
                'slug': 'pulsetrack-smartwatch-gen-4',
                'description': 'Track your health in real-time with ECG monitoring, sleep analysis, built-in GPS, water resistance up to 50m, and vibrant always-on display.',
                'price': Decimal('179.50'),
                'stock': 30,
                'rating': Decimal('4.6'),
                'rating_count': 65,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80',
            },
            {
                'category': categories['electronics'],
                'name': 'RetroMechanical Wireless Keyboard',
                'slug': 'retromechanical-wireless-keyboard',
                'description': 'Tactile mechanical switches with customizable RGB backlighting, hot-swappable keys, and multi-device Bluetooth connectivity.',
                'price': Decimal('89.99'),
                'stock': 18,
                'rating': Decimal('4.7'),
                'rating_count': 42,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80',
            },

            # Fashion
            {
                'category': categories['fashion'],
                'name': 'Urban Minimalist Leather Jacket',
                'slug': 'urban-minimalist-leather-jacket',
                'description': 'Handcrafted from 100% genuine top-grain leather, featuring a tailored modern fit, YKK antique brass zippers, and silk-lined interior.',
                'price': Decimal('249.00'),
                'stock': 15,
                'rating': Decimal('4.9'),
                'rating_count': 53,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=80',
            },
            {
                'category': categories['fashion'],
                'name': 'Classic Oxford Canvas Sneakers',
                'slug': 'classic-oxford-canvas-sneakers',
                'description': 'Timeless design meets ergonomic cushioning. Breathable organic cotton upper with vulcanized non-slip rubber outsoles for daily comfort.',
                'price': Decimal('69.95'),
                'stock': 40,
                'rating': Decimal('4.5'),
                'rating_count': 110,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=800&q=80',
            },
            {
                'category': categories['fashion'],
                'name': 'Heritage Wool Overcoat',
                'slug': 'heritage-wool-overcoat',
                'description': 'A tailored double-breasted silhouette woven from heavy-weight merino wool blend to keep you sharp and warm in any weather.',
                'price': Decimal('189.00'),
                'stock': 8,
                'rating': Decimal('4.7'),
                'rating_count': 38,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=800&q=80',
            },

            # Home & Living
            {
                'category': categories['home-living'],
                'name': 'Nordic Ceramic Coffee Pour-Over Set',
                'slug': 'nordic-ceramic-coffee-set',
                'description': 'Artisan stoneware pour-over dripper with a heat-resistant borosilicate glass carafe and stainless steel mesh filter.',
                'price': Decimal('44.99'),
                'stock': 22,
                'rating': Decimal('4.8'),
                'rating_count': 77,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80',
            },
            {
                'category': categories['home-living'],
                'name': 'Minimalist Ambient Desk Lamp',
                'slug': 'minimalist-ambient-desk-lamp',
                'description': 'Dimmable touch-controlled LED desk light with wireless charging base, natural warm spectrum, and anodized aluminum finish.',
                'price': Decimal('59.50'),
                'stock': 16,
                'rating': Decimal('4.6'),
                'rating_count': 31,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80',
            },

            # Fitness & Sports
            {
                'category': categories['fitness-sports'],
                'name': 'ProGrip Performance Yoga Mat',
                'slug': 'progrip-performance-yoga-mat',
                'description': 'Extra thick 6mm eco-friendly natural rubber with laser-engraved alignment guides and non-slip textured grip for maximum stability.',
                'price': Decimal('49.99'),
                'stock': 35,
                'rating': Decimal('4.9'),
                'rating_count': 94,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&w=800&q=80',
            },
            {
                'category': categories['fitness-sports'],
                'name': 'HydroFlow Insulated Sports Flask 1L',
                'slug': 'hydroflow-insulated-sports-flask',
                'description': 'Double-walled vacuum insulated stainless steel bottle keeping drinks icy cold for 24 hours or steaming hot for 12 hours.',
                'price': Decimal('29.99'),
                'stock': 50,
                'rating': Decimal('4.7'),
                'rating_count': 140,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=800&q=80',
            }
        ]

        for pdata in products_data:
            p, created = Product.objects.get_or_create(
                slug=pdata['slug'],
                defaults=pdata
            )
            if not created:
                for key, val in pdata.items():
                    setattr(p, key, val)
                p.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(products_data)} products across {len(categories_data)} categories.'))
