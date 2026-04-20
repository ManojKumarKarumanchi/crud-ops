"""
Improved Database Seeder with Realistic Data + Test Credentials
"""

import asyncio
import random
from datetime import datetime, timezone
from faker import Faker
from sqlalchemy import select

from app.db import SessionLocal
from app.db.models import User, Item
from app.auth.security import get_password_hash

fake = Faker()


# ADMIN USER SEEDING
async def seed_admin(db):
    ''' Seed a default admin user with known credentials for testing purposes. '''

    admin_email = "admin"
    admin_password = "adminpass123"

    # Check if admin exists
    result = await db.execute(select(User).where(User.email == admin_email))
    existing_admin = result.scalar_one_or_none()

    if existing_admin:
        print(f"[SKIP] Admin user already exists: {admin_email}")
        return existing_admin

    admin_user = User(
        email=admin_email,
        hashed_password=get_password_hash(admin_password),
        full_name="System Administrator",
        is_active=True,
        is_admin=True,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
    )

    db.add(admin_user)
    await db.commit()
    return admin_user


# USER SEEDING
async def seed_users(db, count=6):
    """ Seed regular users with realistic data. All users share the same password."""

    users_created = []
    common_password = "Test@123"  # same for all (easy testing)

    for i in range(count):
        name = fake.name()
        email = fake.unique.email()

        # Check existing
        result = await db.execute(select(User).where(User.email == email))
        if result.scalar_one_or_none():
            continue

        user = User(
            email=email,
            hashed_password=get_password_hash(common_password),
            full_name=name,
            is_active=True,
            is_admin=False,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )

        db.add(user)
        users_created.append({
            "email": email,
            "password": common_password,
            "name": name
        })

        print(f"[CREATE] {name} | {email}")

    await db.commit()

    print(f"\nCreated {len(users_created)} users")

    # Print credentials clearly
    for u in users_created:
        print(f"Email: {u['email']} | Password: {u['password']}")

    return users_created


# ITEM SEEDING
async def seed_items(db, count=6):
    ''' Seed items with realistic product data across multiple categories '''
    # Realistic product catalog with category-aligned data
    product_catalog = {
        "Electronics": [
            {"title": "Sony WH-1000XM5 Wireless Headphones", "desc": "Industry-leading noise cancellation with crystal clear audio. 30-hour battery life, multipoint connection, and premium build quality. Perfect for travel and work.", "price": 29999},
            {"title": "Apple MacBook Air M2 13-inch", "desc": "Lightweight laptop with Apple M2 chip, 8GB RAM, 256GB SSD. Stunning Retina display and all-day battery life. Ideal for students and professionals.", "price": 114900},
            {"title": "Samsung Galaxy S24 Ultra 5G", "desc": "Flagship smartphone with 200MP camera, S Pen, and 5000mAh battery. 12GB RAM, 256GB storage. Titanium frame with Gorilla Glass protection.", "price": 129999},
            {"title": "LG 27-inch 4K UHD Monitor", "desc": "Professional-grade display with IPS panel, HDR10 support, and 99% sRGB coverage. USB-C connectivity with 60W power delivery.", "price": 34999},
        ],
        "Books": [
            {"title": "Atomic Habits by James Clear", "desc": "Practical strategies for forming good habits and breaking bad ones. International bestseller with proven techniques for personal transformation.", "price": 599},
            {"title": "The Psychology of Money", "desc": "Timeless lessons on wealth, greed, and happiness by Morgan Housel. Essential reading for understanding financial decision-making.", "price": 399},
            {"title": "Clean Code by Robert C. Martin", "desc": "Essential guide for software developers. Learn to write maintainable, elegant code with practical examples and best practices.", "price": 1299},
            {"title": "Sapiens: A Brief History", "desc": "Yuval Noah Harari explores the history of humankind from the Stone Age to the modern age. Thought-provoking and brilliantly written.", "price": 499},
        ],
        "Clothing": [
            {"title": "Levi's 501 Original Fit Jeans", "desc": "Classic straight-leg jeans with button fly. 100% cotton denim, stonewashed finish. Timeless style that never goes out of fashion.", "price": 3999},
            {"title": "Nike Dri-FIT Training T-Shirt", "desc": "Moisture-wicking performance fabric keeps you dry during workouts. Lightweight, breathable design with athletic fit.", "price": 1499},
            {"title": "Adidas Ultraboost Running Shoes", "desc": "Premium running shoes with Boost cushioning and Primeknit upper. Continental rubber outsole for superior grip in all conditions.", "price": 14999},
            {"title": "The North Face Thermoball Jacket", "desc": "Lightweight insulated jacket with synthetic fill. Water-resistant, packable design perfect for outdoor adventures.", "price": 12999},
        ],
        "Home & Kitchen": [
            {"title": "Philips Air Fryer XXL", "desc": "Large capacity air fryer with Rapid Air technology. Cook healthy meals with 90% less fat. Digital display with 7 preset programs.", "price": 15999},
            {"title": "Prestige Induction Cooktop 2000W", "desc": "Energy-efficient cooking with automatic voltage regulator. Indian menu presets, timer function, and feather touch buttons.", "price": 2499},
            {"title": "Amazon Echo Dot (5th Gen)", "desc": "Smart speaker with Alexa voice control. Rich sound quality, control smart home devices, and access music streaming services.", "price": 4499},
            {"title": "Milton Thermosteel Flask 1L", "desc": "Double-walled vacuum insulation keeps beverages hot for 24 hours or cold for 24 hours. Leak-proof lid and durable stainless steel.", "price": 899},
        ],
        "Sports & Fitness": [
            {"title": "Yonex Astrox 99 Badminton Racket", "desc": "Professional-grade racket with Namd graphite for explosive power. Head-heavy balance, ideal for aggressive play.", "price": 16999},
            {"title": "Cosco Cricket Bat English Willow", "desc": "Premium cricket bat with Grade 1 English willow. Thick edges, large sweet spot, and traditional shape for power hitting.", "price": 8999},
            {"title": "Nivia Storm Football Size 5", "desc": "FIFA Quality certified football with hand-stitched construction. Superior air retention and consistent flight characteristics.", "price": 1299},
            {"title": "Strauss Adjustable Dumbbells 20kg Set", "desc": "Space-saving home gym equipment with quick-change weight system. Non-slip handles and protective rubber coating.", "price": 3499},
        ],
        "Toys & Games": [
            {"title": "LEGO Creator Expert Modular Building", "desc": "Advanced building set with 2500+ pieces. Detailed architecture with opening doors, interiors, and mini-figures. Ages 16+.", "price": 12999},
            {"title": "Hot Wheels Track Builder Set", "desc": "Customizable race track with loop-de-loops, launchers, and crash zones. Includes 2 die-cast cars. Hours of creative play.", "price": 2999},
            {"title": "Barbie Dreamhouse Playset", "desc": "3-story dollhouse with working elevator, slide, pool, and 70+ accessories. Lights and sounds for realistic play experience.", "price": 9999},
            {"title": "Hasbro Monopoly Classic Board Game", "desc": "Timeless family board game for 2-6 players. Buy properties, build houses, and bankrupt opponents to win.", "price": 1299},
        ],
    }

    items_created = 0
    categories = list(product_catalog.keys())

    # Ensure we get one item from each category
    for category in categories[:count]:
        products = product_catalog[category]
        product = random.choice(products)

        item = Item(
            title=product["title"],
            description=product["desc"],
            price=product["price"],
            category=category,
            is_available=fake.boolean(chance_of_getting_true=90),
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )

        db.add(item)
        items_created += 1

        print(f"[CREATE] {item.title}")
        print(f"Category: {category} | Price: Rs.{item.price/100:.2f} | Available: {item.is_available}")

    await db.commit()
    print(f"\nCreated {items_created} items across {items_created} categories")
    return items_created


# SUMMARY
async def display_summary(db):
    ''' Display a summary of seeded data '''
    users = (await db.execute(select(User))).scalars().all()
    items = (await db.execute(select(Item))).scalars().all()

    print(f"Users: {len(users)}")
    print(f"Items: {len(items)}")

    if users:
        u = users[0]
        print("\nSample User:")
        print(f"Name: {u.full_name}")
        print(f"Email: {u.email}")

    if items:
        i = items[0]
        print("\nSample Item:")
        print(f"Title: {i.title}")
        print(f"Price: Rs.{i.price/100:.2f}")


# MAIN
async def main():
    ''' Main function to run the seeding process '''
    async with SessionLocal() as db:
        try:
            await seed_admin(db)
            await seed_users(db, 6)
            await seed_items(db, 6)
            await display_summary(db)

            print("\n[SUCCESS] Seeding complete!")

        except Exception as e:
            print(f"\n[ERROR] {e}")
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
