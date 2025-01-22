-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS restaurant_analysis;
USE restaurant_analysis;

-- Tabla para almacenar información básica de los restaurantes
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    location_id INT NOT NULL,
    avg_rating DECIMAL(3, 2), -- Calificación promedio (0.00 - 5.00)
    num_of_reviews INT, -- Número total de reseñas
    price_level ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Tabla para almacenar categorías de restaurantes
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT
);

-- Tabla para almacenar información geográfica
CREATE TABLE IF NOT EXISTS locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    state VARCHAR(255) NOT NULL, -- Estado (Ej: California, Texas)
    city VARCHAR(255) NOT NULL,
    population INT, -- Población de la ciudad
    total_restaurants INT, -- Número total de restaurantes en la ciudad
    UNIQUE (state, city)
);

-- Tabla para almacenar reseñas de usuarios
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT NOT NULL,
    user_id VARCHAR(255) NOT NULL, -- ID único del usuario
    rating INT CHECK (rating BETWEEN 1 AND 5), -- Calificación de 1 a 5
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- Tabla para almacenar métricas de rendimiento (KPIs)
CREATE TABLE IF NOT EXISTS kpis (
    kpi_id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL,
    dissatisfied_ratio DECIMAL(5, 2), -- Porcentaje de usuarios insatisfechos
    category_demand VARCHAR(255), -- Categorías con alta demanda
    restaurants_per_population DECIMAL(10, 2), -- Proporción de restaurantes/población
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_avg_rating ON restaurants(avg_rating);
CREATE INDEX idx_state_city ON locations(state, city);
CREATE INDEX idx_restaurant_id ON reviews(restaurant_id);
