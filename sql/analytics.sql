-- ==========================================
-- Crypto Analytics Queries
-- ==========================================

-- 1. View all cryptocurrency data
SELECT
    id,
    symbol,
    current_price,
    market_cap,
    total_volume,
    price_change_percentage_24h
FROM crypto_prices;


-- 2. Rank cryptocurrencies by 24-hour change
SELECT
    id,
    symbol,
    price_change_percentage_24h
FROM crypto_prices
ORDER BY price_change_percentage_24h DESC;


-- 3. Highest-priced cryptocurrency
SELECT
    id,
    symbol,
    current_price
FROM crypto_prices
ORDER BY current_price DESC
LIMIT 1;


-- 4. Largest market-cap cryptocurrency
SELECT
    id,
    symbol,
    market_cap
FROM crypto_prices
ORDER BY market_cap DESC
LIMIT 1;


-- 5. Total number of cryptocurrencies
SELECT COUNT(*) AS total_coins
FROM crypto_prices;