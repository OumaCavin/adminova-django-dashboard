"""
Management command to load subscription plans
"""
from django.core.management.base import BaseCommand
from apps.subscriptions.models import Plan


class Command(BaseCommand):
    help = 'Load sample subscription plans'

    def handle(self, *args, **options):
        plans_data = [
            {
                'name': 'Free',
                'slug': 'free-monthly',
                'description': 'Basic features for individuals',
                'price': 0,
                'billing_cycle': 'monthly',
                'features': {
                    'storage': '1GB',
                    'users': '1',
                    'support': 'Community',
                    'analytics': False
                },
                'is_active': True,
                'display_order': 1,
            },
            {
                'name': 'Starter Monthly',
                'slug': 'starter-monthly',
                'description': 'Perfect for small teams',
                'price': 2500,
                'billing_cycle': 'monthly',
                'features': {
                    'storage': '10GB',
                    'users': '5',
                    'support': 'Email',
                    'analytics': True
                },
                'is_active': True,
                'is_popular': True,
                'display_order': 2,
            },
            {
                'name': 'Starter Annual',
                'slug': 'starter-annual',
                'description': 'Perfect for small teams (Save 16%)',
                'price': 25000,
                'billing_cycle': 'annually',
                'features': {
                    'storage': '10GB',
                    'users': '5',
                    'support': 'Email',
                    'analytics': True
                },
                'is_active': True,
                'display_order': 3,
            },
            {
                'name': 'Professional Monthly',
                'slug': 'professional-monthly',
                'description': 'For growing businesses',
                'price': 5000,
                'billing_cycle': 'monthly',
                'features': {
                    'storage': '50GB',
                    'users': '20',
                    'support': 'Priority',
                    'analytics': True,
                    'api_access': True
                },
                'is_active': True,
                'display_order': 4,
            },
            {
                'name': 'Professional Annual',
                'slug': 'professional-annual',
                'description': 'For growing businesses (Save 16%)',
                'price': 50000,
                'billing_cycle': 'annually',
                'features': {
                    'storage': '50GB',
                    'users': '20',
                    'support': 'Priority',
                    'analytics': True,
                    'api_access': True
                },
                'is_active': True,
                'display_order': 5,
            },
            {
                'name': 'Enterprise Monthly',
                'slug': 'enterprise-monthly',
                'description': 'Advanced features for large organizations',
                'price': 10000,
                'billing_cycle': 'monthly',
                'features': {
                    'storage': 'Unlimited',
                    'users': 'Unlimited',
                    'support': '24/7 Dedicated',
                    'analytics': True,
                    'api_access': True,
                    'custom_integrations': True
                },
                'is_active': True,
                'display_order': 6,
            },
            {
                'name': 'Enterprise Annual',
                'slug': 'enterprise-annual',
                'description': 'Advanced features for large organizations (Save 16%)',
                'price': 100000,
                'billing_cycle': 'annually',
                'features': {
                    'storage': 'Unlimited',
                    'users': 'Unlimited',
                    'support': '24/7 Dedicated',
                    'analytics': True,
                    'api_access': True,
                    'custom_integrations': True
                },
                'is_active': True,
                'display_order': 7,
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
                    self.style.SUCCESS(f'✓ Created: {plan.name} - KSh {plan.price}/{plan.billing_cycle}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'• Already exists: {plan.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Loaded {created_count} new plans!')
        )
