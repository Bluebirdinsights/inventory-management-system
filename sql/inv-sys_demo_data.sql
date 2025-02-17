-- --------------------------------------------------------
-- Demo Data for Brewery Inventory System
-- Generated for demonstration purposes only
-- All data is fictional and AI-generated
-- Created: February 2025
-- --------------------------------------------------------

-- Categories
INSERT INTO categories (name) VALUES ('IPA & Pale Ales');
INSERT INTO categories (name) VALUES ('Stouts & Porters');
INSERT INTO categories (name) VALUES ('Lagers & Pilsners');
INSERT INTO categories (name) VALUES ('Wheat & Belgian');
INSERT INTO categories (name) VALUES ('Sours & Wild Ales');
INSERT INTO categories (name) VALUES ('Non-Alcoholic');

-- Business Customers
INSERT INTO customers (name, contact_info) VALUES ('Ølhallen Tromsø', 'bestilling@olhallen.no | +47 221 43 567');
INSERT INTO customers (name, contact_info) VALUES ('Håndverker Oslo', 'innkjop@handverker.no | +47 815 92 301');
INSERT INTO customers (name, contact_info) VALUES ('Cardinal Pub', 'orders@cardinalpub.no | +47 553 78 142');
INSERT INTO customers (name, contact_info) VALUES ('Vinmonopolet Majorstuen', 'majorstuen@vinmonopolet.no | +47 400 12 876');
INSERT INTO customers (name, contact_info) VALUES ('Crowbar Oslo', 'beer@crowbar.no | +47 928 45 632');
INSERT INTO customers (name, contact_info) VALUES ('RooR Bergen', 'post@roor.no | +47 329 32 775');
INSERT INTO customers (name, contact_info) VALUES ('Café Opera', 'bestilling@cafeopera.no | +47 735 91 234');
INSERT INTO customers (name, contact_info) VALUES ('Geir Flom', 'shop@aegirbrewery.no | +47 922 84 567');
INSERT INTO customers (name, contact_info) VALUES ('Mathallen Oslo', 'orders@mathallen.no | +47 518 76 432');
INSERT INTO customers (name, contact_info) VALUES ('Brewery Market', 'wholesale@brewerymarket.no | +47 233 45 678');

-- Products
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (1, 'Mountain Haze IPA', 'IPA & Pale Ales', 'Small-batch craft Mountain Haze IPA brewed with local ingredients', 45, 180);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (2, 'Pine Valley DIPA', 'IPA & Pale Ales', 'Small-batch craft Pine Valley DIPA brewed with local ingredients', 45, 180);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (3, 'Sunset Session Pale', 'IPA & Pale Ales', 'Small-batch craft Sunset Session Pale brewed with local ingredients', 45, 180);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (4, 'Nordic Forest APA', 'IPA & Pale Ales', 'Small-batch craft Nordic Forest APA brewed with local ingredients', 45, 180);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (5, 'Midnight Coffee Stout', 'Stouts & Porters', 'Small-batch craft Midnight Coffee Stout brewed with local ingredients', 45, 180);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (6, 'Vanilla Bean Porter', 'Stouts & Porters', 'Small-batch craft Vanilla Bean Porter brewed with local ingredients', 45, 180);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (7, 'Oatmeal Breakfast Stout', 'Stouts & Porters', 'Small-batch craft Oatmeal Breakfast Stout brewed with local ingredients', 45, 180);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (8, 'Baltic Porter Reserve', 'Stouts & Porters', 'Small-batch craft Baltic Porter Reserve brewed with local ingredients', 45, 180);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (9, 'Fjord Pilsner', 'Lagers & Pilsners', 'Small-batch craft Fjord Pilsner brewed with local ingredients', 45, 150);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (10, 'Classic Helles', 'Lagers & Pilsners', 'Small-batch craft Classic Helles brewed with local ingredients', 45, 150);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (11, 'Vienna Style Lager', 'Lagers & Pilsners', 'Small-batch craft Vienna Style Lager brewed with local ingredients', 45, 150);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (12, 'North Coast Dunkel', 'Lagers & Pilsners', 'Small-batch craft North Coast Dunkel brewed with local ingredients', 45, 150);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (13, 'Cloudy Hefeweizen', 'Wheat & Belgian', 'Small-batch craft Cloudy Hefeweizen brewed with local ingredients', 45, 120);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (14, 'Nordic Wit', 'Wheat & Belgian', 'Small-batch craft Nordic Wit brewed with local ingredients', 45, 120);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (15, 'Abbey Style Tripel', 'Wheat & Belgian', 'Small-batch craft Abbey Style Tripel brewed with local ingredients', 45, 120);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (16, 'Rye Saison', 'Wheat & Belgian', 'Small-batch craft Rye Saison brewed with local ingredients', 45, 120);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (17, 'Cherry Sour', 'Sours & Wild Ales', 'Small-batch craft Cherry Sour brewed with local ingredients', 45, 365);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (18, 'Wild Farmhouse Ale', 'Sours & Wild Ales', 'Small-batch craft Wild Farmhouse Ale brewed with local ingredients', 45, 365);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (19, 'Raspberry Lambic Style', 'Sours & Wild Ales', 'Small-batch craft Raspberry Lambic Style brewed with local ingredients', 45, 365);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (20, 'Hop Sparkling Water', 'Non-Alcoholic', 'Small-batch craft Hop Sparkling Water brewed with local ingredients', 45, 90);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (21, 'Craft Root Beer', 'Non-Alcoholic', 'Small-batch craft Craft Root Beer brewed with local ingredients', 45, 90);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (22, 'NA IPA', 'Non-Alcoholic', 'Small-batch craft NA IPA brewed with local ingredients', 45, 90);
INSERT INTO products (id, name, category, description, base_price, days_to_expiration) 
    VALUES (23, 'Botanical Brew', 'Non-Alcoholic', 'Small-batch craft Botanical Brew brewed with local ingredients', 45, 90);


-- Production Data (Inventory)
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (1, 500, 'L', '2025-02-15'::date, 
    ('2025-05-15'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 1)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (9, 800, 'L', '2025-02-10'::date, 
    ('2025-06-10'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 9)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (5, 400, 'L', '2025-02-20'::date, 
    ('2025-05-20'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 5)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (13, 600, 'L', '2025-02-25'::date, 
    ('2025-05-25'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 13)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (20, 300, 'L', '2025-02-28'::date, 
    ('2025-04-28'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 20)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (2, 450, 'L', '2025-03-01'::date, 
    ('2025-06-01'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 2)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (10, 700, 'L', '2025-03-05'::date, 
    ('2025-07-05'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 10)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (17, 400, 'L', '2025-03-10'::date, 
    ('2025-09-10'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 17)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (21, 400, 'L', '2025-03-12'::date, 
    ('2025-05-12'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 21)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (3, 550, 'L', '2025-03-15'::date, 
    ('2025-06-15'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 3)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (23, 449, 'L', '2025-01-04'::date, 
    ('2025-01-04'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 23)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (2, 722, 'L', '2025-01-09'::date, 
    ('2025-01-09'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 2)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (9, 224, 'L', '2025-01-12'::date, 
    ('2025-01-12'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 9)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (3, 285, 'L', '2025-01-13'::date, 
    ('2025-01-13'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 3)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (16, 623, 'L', '2025-01-16'::date, 
    ('2025-01-16'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 16)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (4, 542, 'L', '2025-01-16'::date, 
    ('2025-01-16'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 4)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (2, 269, 'L', '2025-01-19'::date, 
    ('2025-01-19'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 2)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (3, 653, 'L', '2025-01-20'::date, 
    ('2025-01-20'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 3)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (9, 328, 'L', '2025-01-23'::date, 
    ('2025-01-23'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 9)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (8, 206, 'L', '2025-01-23'::date, 
    ('2025-01-23'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 8)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (4, 624, 'L', '2025-01-23'::date, 
    ('2025-01-23'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 4)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (22, 381, 'L', '2025-01-25'::date, 
    ('2025-01-25'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 22)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (12, 617, 'L', '2025-01-25'::date, 
    ('2025-01-25'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 12)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (5, 616, 'L', '2025-01-26'::date, 
    ('2025-01-26'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 5)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (3, 403, 'L', '2025-01-28'::date, 
    ('2025-01-28'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 3)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (8, 309, 'L', '2025-01-28'::date, 
    ('2025-01-28'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 8)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (14, 428, 'L', '2025-02-02'::date, 
    ('2025-02-02'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 14)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (16, 389, 'L', '2025-02-04'::date, 
    ('2025-02-04'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 16)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (20, 343, 'L', '2025-02-06'::date, 
    ('2025-02-06'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 20)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (19, 371, 'L', '2025-02-13'::date, 
    ('2025-02-13'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 19)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (19, 762, 'L', '2025-02-20'::date, 
    ('2025-02-20'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 19)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (18, 633, 'L', '2025-02-22'::date, 
    ('2025-02-22'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 18)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (20, 374, 'L', '2025-02-27'::date, 
    ('2025-02-27'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 20)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (8, 683, 'L', '2025-03-06'::date, 
    ('2025-03-06'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 8)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (13, 463, 'L', '2025-03-10'::date, 
    ('2025-03-10'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 13)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (5, 656, 'L', '2025-03-19'::date, 
    ('2025-03-19'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 5)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (3, 251, 'L', '2025-03-20'::date, 
    ('2025-03-20'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 3)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (8, 751, 'L', '2025-03-21'::date, 
    ('2025-03-21'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 8)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (18, 516, 'L', '2025-03-22'::date, 
    ('2025-03-22'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 18)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (6, 769, 'L', '2025-03-22'::date, 
    ('2025-03-22'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 6)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (1, 314, 'L', '2025-03-22'::date, 
    ('2025-03-22'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 1)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (8, 496, 'L', '2025-03-24'::date, 
    ('2025-03-24'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 8)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (4, 735, 'L', '2025-03-25'::date, 
    ('2025-03-25'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 4)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (8, 375, 'L', '2025-03-29'::date, 
    ('2025-03-29'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 8)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (12, 264, 'L', '2025-03-30'::date, 
    ('2025-03-30'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 12)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (21, 361, 'L', '2025-04-01'::date, 
    ('2025-04-01'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 21)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (13, 516, 'L', '2025-04-07'::date, 
    ('2025-04-07'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 13)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (6, 780, 'L', '2025-04-08'::date, 
    ('2025-04-08'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 6)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (6, 677, 'L', '2025-04-08'::date, 
    ('2025-04-08'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 6)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (10, 648, 'L', '2025-04-09'::date, 
    ('2025-04-09'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 10)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (23, 540, 'L', '2025-04-10'::date, 
    ('2025-04-10'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 23)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (23, 655, 'L', '2025-04-12'::date, 
    ('2025-04-12'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 23)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (10, 486, 'L', '2025-04-13'::date, 
    ('2025-04-13'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 10)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (16, 297, 'L', '2025-04-13'::date, 
    ('2025-04-13'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 16)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (12, 761, 'L', '2025-04-18'::date, 
    ('2025-04-18'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 12)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (1, 582, 'L', '2025-04-18'::date, 
    ('2025-04-18'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 1)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (17, 808, 'L', '2025-04-21'::date, 
    ('2025-04-21'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 17)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (2, 412, 'L', '2025-04-23'::date, 
    ('2025-04-23'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 2)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (2, 435, 'L', '2025-04-23'::date, 
    ('2025-04-23'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 2)));
INSERT INTO inventory (product_id, quantity, unit, production_date, expiry_date) 
    VALUES (8, 478, 'L', '2025-04-28'::date, 
    ('2025-04-28'::date + INTERVAL '1 day' * (SELECT days_to_expiration FROM products WHERE id = 8)));

-- Sales Data
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (1, 5, 100, 'L', 89, '2025-02-20 14:30:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (9, 4, 200, 'L', 82, '2025-02-25 10:15:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (5, 1, 75, 'L', 92, '2025-03-01 16:45:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (20, 9, 150, 'L', 45, '2025-03-05 11:20:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (13, 2, 120, 'L', 86, '2025-03-10 15:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (7, 2, 79, 'L', 90, '2025-01-06 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (3, 2, 364, 'L', 96, '2025-01-07 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (13, 5, 149, 'L', 76, '2025-01-11 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (6, 8, 186, 'L', 75, '2025-01-14 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (9, 4, 293, 'L', 85, '2025-01-18 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (22, 1, 342, 'L', 73, '2025-01-22 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (14, 10, 252, 'L', 77, '2025-01-22 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (5, 8, 280, 'L', 71, '2025-01-22 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (2, 6, 390, 'L', 87, '2025-01-25 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (1, 5, 285, 'L', 97, '2025-01-26 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (17, 10, 128, 'L', 96, '2025-01-27 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (10, 1, 281, 'L', 73, '2025-02-11 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (7, 2, 335, 'L', 90, '2025-02-16 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (9, 10, 119, 'L', 72, '2025-02-21 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (17, 10, 146, 'L', 84, '2025-02-24 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (22, 3, 281, 'L', 78, '2025-02-25 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (4, 1, 297, 'L', 90, '2025-02-27 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (16, 8, 230, 'L', 98, '2025-02-28 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (8, 4, 240, 'L', 87, '2025-03-02 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (14, 3, 117, 'L', 72, '2025-03-06 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (3, 1, 389, 'L', 99, '2025-03-08 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (20, 2, 225, 'L', 91, '2025-03-22 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (3, 9, 163, 'L', 79, '2025-03-24 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (9, 5, 177, 'L', 86, '2025-03-25 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (15, 6, 180, 'L', 95, '2025-03-30 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (14, 1, 281, 'L', 70, '2025-03-31 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (5, 5, 212, 'L', 90, '2025-04-02 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (10, 6, 60, 'L', 92, '2025-04-11 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (9, 7, 323, 'L', 78, '2025-04-16 12:00:00'::timestamp, 'completed');
INSERT INTO sales (product_id, customer_id, quantity, unit, price_per_unit, sale_date, status) 
    VALUES (5, 6, 148, 'L', 85, '2025-04-24 12:00:00'::timestamp, 'completed');
