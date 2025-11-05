"""
Management command to initialize the database with sample data
Run: python manage.py init_sample_data
Created by Cavin Otieno
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.subscriptions.models import Plan
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Initialize database with sample subscription plans'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample subscription plans...')
        
        # Create subscription plans
        plans_data = [
            {
                'name': 'Starter',
                'slug': 'starter',
                'description': 'Perfect for individuals and small projects',
                'price': Decimal('499.00'),
                'billing_cycle': 'monthly',
                'features': {
                    'users': 1,
                    'storage': '1GB',
                    'support': 'Email',
                    'features': ['Basic Dashboard', 'Email Support', '1GB Storage']
                },
                'is_popular': False,
                'display_order': 1,
            },
            {
                'name': 'Professional',
                'slug': 'professional',
                'description': 'Ideal for growing businesses and teams',
                'price': Decimal('1999.00'),
                'billing_cycle': 'monthly',
                'features': {
                    'users': 5,
                    'storage': '10GB',
                    'support': 'Priority Email',
                    'features': [
                        'Advanced Dashboard',
                        'Priority Support',
                        '10GB Storage',
                        'API Access',
                        'Custom Reports'
                    ]
                },
                'is_popular': True,
                'display_order': 2,
            },
            {
                'name': 'Enterprise',
                'slug': 'enterprise',
                'description': 'For large organizations with advanced needs',
                'price': Decimal('4999.00'),
                'billing_cycle': 'monthly',
                'features': {
                    'users': 'Unlimited',
                    'storage': '100GB',
                    'support': '24/7 Phone & Email',
                    'features': [
                        'Full Dashboard Access',
                        '24/7 Support',
                        '100GB Storage',
                        'API Access',
                        'Custom Reports',
                        'Dedicated Account Manager',
                        'SLA Guarantee'
                    ]
                },
                'is_popular': False,
                'display_order': 3,
            },
            # Annual plans with discount
            {
                'name': 'Starter Annual',
                'slug': 'starter-annual',
                'description': 'Perfect for individuals and small projects (Annual billing)',
                'price': Decimal('4999.00'),  # ~17% discount
                'billing_cycle': 'annually',
                'features': {
                    'users': 1,
                    'storage': '1GB',
                    'support': 'Email',
                    'features': ['Basic Dashboard', 'Email Support', '1GB Storage']
                },
                'is_popular': False,
                'display_order': 4,
            },
            {
                'name': 'Professional Annual',
                'slug': 'professional-annual',
                'description': 'Ideal for growing businesses and teams (Annual billing)',
                'price': Decimal('19999.00'),  # ~17% discount
                'billing_cycle': 'annually',
                'features': {
                    'users': 5,
                    'storage': '10GB',
                    'support': 'Priority Email',
                    'features': [
                        'Advanced Dashboard',
                        'Priority Support',
                        '10GB Storage',
                        'API Access',
                        'Custom Reports'
                    ]
                },
                'is_popular': True,
                'display_order': 5,
            },
        ]
        
        created_count = 0
        for plan_data in plans_data:
            plan, created = Plan.objects.get_or_create(
                slug=plan_data['slug'],
                defaults=plan_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created plan: {plan.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Plan already exists: {plan.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Created {created_count} new plans')
        )
        self.stdout.write(
            self.style.SUCCESS(f'✓ Total plans in database: {Plan.objects.count()}')
        )
