DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name char(80) NOT NULL,
    status char(60) NOT NULL
);

CREATE TABLE  products(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name char(60) NOT NULL,
      skus varchar(60) NOT NULL,
      quantity INTEGER,
      Idorders INTEGER,
      CONSTRAINT fk_orders FOREIGN KEY (Idorders) REFERENCES orders (id)

);