CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    overdraft_limit DECIMAL(10, 2) DEFAULT 0.00,
    interest_rate DECIMAL(5, 2) DEFAULT 0.00,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id VARCHAR(36 )PRIMARY KEY,
    account_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    comment VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

CREATE TABLE IF NOT EXISTS stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    stock_price DECIMAL(10, 2) NULL,
    dividend_rate DECIMAL(5, 2) DEFAULT 0.00,
    total_owned DECIMAL(12, 2) DEFAULT 0.00,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Sample Data
INSERT INTO users (name, email) VALUES ('Alice Smith', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob Johnson', 'bob@example.com');
INSERT INTO users (name, email) VALUES ('Charlie Brown', 'charlie@example.com');

INSERT INTO accounts (owner_id, balance, overdraft_limit, interest_rate) VALUES 
(1, 500.00, 100.00, 5.00),  -- Alice
(2, 1700.00, 200.00, 4.00), -- Bob
(3, 1500.00, 300.00, 3.00); -- Charlie

-- Insert transactions for Alice
INSERT INTO transactions (id, account_id, amount, transaction_type, comment, created_at) VALUES 
('550e8400-e29b-41d4-a716-446655440000', 1, 800.00, 'deposit', 'Initial deposit', '2024-01-01 10:00:00'),
('550e8400-e29b-41d4-a716-446655440001', 1, -200.00, 'withdrawal', 'Groceries', '2024-01-05 12:30:00'),
('550e8400-e29b-41d4-a716-446655440002', 1, -300.00, 'withdrawal', 'Utilities', '2024-01-10 15:45:00'),
('550e8400-e29b-41d4-a716-446655440003', 1, -100.00, 'withdrawal', 'Dining out', '2024-01-15 18:00:00'),
('550e8400-e29b-41d4-a716-446655440004', 1, -100.00, 'withdrawal', 'Miscellaneous', '2024-01-20 20:15:00'),
('550e8400-e29b-41d4-a716-446655440045', 1, 400.00, 'deposit', 'Another deposit', '2024-02-01 10:00:00');

-- Insert transactions for Bob
INSERT INTO transactions (id, account_id, amount, transaction_type, comment, created_at) VALUES 
('550e8400-e29b-41d4-d356-446655440005', 2, 1000.00, 'deposit', 'Initial deposit', '2024-01-02 09:00:00'),
('550e8400-e29b-41d4-d356-446655440006', 2, 1500.00, 'deposit', 'Bonus payment', '2024-01-07 11:00:00'),
('550e8400-e29b-41d4-d356-446655440007', 2, -400.00, 'withdrawal', 'Car payment', '2024-01-12 14:30:00'),
('550e8400-e29b-41d4-d356-446655440008', 2, -100.00, 'withdrawal', 'Groceries', '2024-01-17 17:00:00'),
('550e8400-e29b-41d4-d356-446655440009', 2, -300.00, 'withdrawal', 'Dining out', '2024-01-22 19:45:00');



-- Insert transactions for Charlie
INSERT INTO transactions (id, account_id, amount, transaction_type, comment, created_at) VALUES 
('550e8400-e29b-41d4-456o-44665544000a', 3, 2000.00, 'deposit', 'Initial deposit', '2024-01-03 08:30:00'),
('550e8400-e29b-41d4-456o-44665544000b', 3, 1000.00, 'deposit', 'Investment return', '2024-01-08 10:15:00'),
('550e8400-e29b-41d4-456o-44665544000c', 3, -600.00, 'withdrawal', 'Vacation', '2024-01-13 16:00:00'),
('550e8400-e29b-41d4-456o-44665544000d', 3, -400.00, 'withdrawal', 'Home repairs', '2024-01-18 13:00:00'),
('550e8400-e29b-41d4-456o-44665544000e', 3, -500.00, 'withdrawal', 'Dining out', '2024-01-23 21:30:00');



INSERT INTO stocks (symbol, company_name, total_owned, stock_price,  dividend_rate, owner_id) VALUES
('AAPL', 'Apple Inc.',200, 150.00, 0.00, 1),  -- Owned by Alice
('GOOGL', 'Alphabet Inc.',13, 2800.00, 0.00, 1),  -- Owned by Alice
('AMZN', 'Amazon.com Inc.',343, 3400.00, 0.00, 2),  -- Owned by Bob
('MSFT', 'Microsoft Corp.',7899, 3300.00, 0.00, 2),  -- Owned by Bob
('TSLA', 'Tesla Inc.',456, 800.00, 0.00, 3);  -- Owned by Charlie
