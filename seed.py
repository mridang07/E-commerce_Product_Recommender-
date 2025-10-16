from . import models

SAMPLE_PRODUCTS = [
    ('p1','Noise-Cancelling Headphones','Comfortable over-ear Bluetooth headphones','audio',99.99,['headphones','bluetooth','audio']),
    ('p2','Wireless Mouse','Ergonomic wireless mouse with long battery life','accessories',25.50,['mouse','wireless','peripherals']),
    ('p3','Mechanical Keyboard','Tactile mechanical keyboard, compact','accessories',79.00,['keyboard','mechanical','peripherals']),
    ('p4','USB-C Fast Charger','45W USB-C charger compact design','power',29.99,['charger','usb-c','power']),
    ('p5','Smartwatch Lite','Fitness focused wearable with notifications','wearables',129.00,['watch','fitness','wearable']),
    ('p6','Bluetooth Earbuds','True wireless earbuds with charging case','audio',49.99,['earbuds','bluetooth','audio']),
    ('p7','Laptop Sleeve 13"','Padded sleeve for 13 inch laptops','accessories',19.99,['sleeve','laptop','case']),
    ('p8','4K Monitor 27"','27-inch 4K IPS monitor for creators','display',299.00,['monitor','4k','display']),
    ('p9','Portable SSD 1TB','Fast portable SSD with USB-C','storage',149.99,['ssd','storage','usb-c']),
    ('p10','Webcam HD','1080p webcam with built-in mic','camera',59.99,['webcam','camera','streaming'])
]

def seed_demo(session):
    # create products
    for pid,title,desc,cat,price,tags in SAMPLE_PRODUCTS:
        existing = session.query(models.Product).filter(models.Product.id==pid).first()
        if not existing:
            models.create_product(session, pid, title, desc, cat, price, tags)
    # create demo user and interactions
    user = models.get_or_create_user(session, "demo_user")
    # sample interactions: views on audio and accessories
    interactions = [
        ('demo_user','p6','view'),
        ('demo_user','p2','view'),
        ('demo_user','p7','add_to_cart'),
        ('demo_user','p1','view'),
        ('demo_user','p3','purchase'),
    ]
    for u,p,t in interactions:
        models.create_interaction(session, u, p, t)
