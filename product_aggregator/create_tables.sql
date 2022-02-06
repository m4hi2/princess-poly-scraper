CREATE TABLE IF NOT EXISTS product (
  name VARCHAR(250) NOT NULL,
  price FLOAT NOT NULL,
  full_price FLOAT NOT NULL,
  size VARCHAR(100) NOT NULL,
  color VARCHAR(100) NOT NULL,
  image_links TEXT[],
  stock int NOT NULL,
  description TEXT
  );
