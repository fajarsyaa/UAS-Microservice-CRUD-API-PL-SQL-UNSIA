CREATE TABLE IF NOT EXISTS ms_customer (
    id SERIAL PRIMARY KEY,
    username VARCHAR(120) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE,
    password VARCHAR(255) NOT NULL,
    no_rek INTEGER UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS ms_merchant (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE,
    password VARCHAR(255) NOT NULL,
    no_rek INTEGER UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS trx_payment (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    merchant_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES ms_customer(id),
    FOREIGN KEY (merchant_id) REFERENCES ms_merchant(id)
);

CREATE TABLE IF NOT EXISTS ms_customer_log (
    id SERIAL PRIMARY KEY,
    action VARCHAR(10) NOT NULL,
    username VARCHAR(120) NOT NULL,
    email VARCHAR(120),
    password VARCHAR(255) NOT NULL,
    no_rek INTEGER NOT NULL,
    changed_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS ms_merchant_log (
    id SERIAL PRIMARY KEY,
    action VARCHAR(10) NOT NULL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(120),
    password VARCHAR(255) NOT NULL,
    no_rek INTEGER NOT NULL,
    changed_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS trx_payment_log (
    id SERIAL PRIMARY KEY,
    action VARCHAR(10) NOT NULL,
    customer_id INTEGER,
    merchant_id INTEGER,
    amount FLOAT,
    changed_at TIMESTAMP NOT NULL
);


CREATE OR REPLACE FUNCTION log_ms_customer_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO ms_customer_log (action, username, email, password, no_rek, changed_at)
        VALUES ('INSERT', NEW.username, NEW.email, NEW.password, NEW.no_rek, NOW());
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO ms_customer_log (action, username, email, password, no_rek, changed_at)
        VALUES ('UPDATE', NEW.username, NEW.email, NEW.password, NEW.no_rek, NOW());
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO ms_customer_log (action, username, email, password, no_rek, changed_at)
        VALUES ('DELETE', OLD.username, OLD.email, OLD.password, OLD.no_rek, NOW());
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER ms_customer_trigger
AFTER INSERT OR UPDATE OR DELETE ON ms_customer
FOR EACH ROW EXECUTE FUNCTION log_ms_customer_changes();

CREATE OR REPLACE FUNCTION log_ms_merchant_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO ms_merchant_log (action, username, email, password, no_rek, changed_at)
        VALUES ('INSERT', NEW.username, NEW.email, NEW.password, NEW.no_rek, NOW());
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO ms_merchant_log (action, username, email, password, no_rek, changed_at)
        VALUES ('UPDATE', NEW.username, NEW.email, NEW.password, NEW.no_rek, NOW());
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO ms_merchant_log (action, username, email, password, no_rek, changed_at)
        VALUES ('DELETE', OLD.username, OLD.email, OLD.password, OLD.no_rek, NOW());
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ms_merchant_trigger
AFTER INSERT OR UPDATE OR DELETE ON ms_merchant
FOR EACH ROW EXECUTE FUNCTION log_ms_merchant_changes();

CREATE OR REPLACE FUNCTION log_trx_payment_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO trx_payment_log (action, customer_id, merchant_id, amount, changed_at)
        VALUES ('INSERT', NEW.customer_id, NEW.merchant_id, NEW.amount, NOW());
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO trx_payment_log (action, customer_id, merchant_id, amount, changed_at)
        VALUES ('DELETE', OLD.customer_id, OLD.merchant_id, OLD.amount, NOW());
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trx_payment_trigger
AFTER INSERT OR DELETE ON trx_payment
FOR EACH ROW EXECUTE FUNCTION log_trx_payment_changes();
