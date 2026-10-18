-- Interior Design Studio Database Schema
-- MySQL Database Setup

-- Create database
CREATE DATABASE IF NOT EXISTS interior_design_studio;
USE interior_design_studio;

-- Services table
CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    price_range VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    description TEXT,
    image_url VARCHAR(255),
    before_image_url VARCHAR(255),
    after_image_url VARCHAR(255),
    area_sqft INT,
    completion_date DATE,
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Consultations table
CREATE TABLE IF NOT EXISTS consultations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    project_type VARCHAR(50),
    budget VARCHAR(50),
    preferred_date DATE,
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contact Messages table
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(150),
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'unread',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Testimonials table
CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    client_title VARCHAR(100),
    testimonial TEXT NOT NULL,
    rating INT DEFAULT 5,
    project_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

-- Insert sample services
INSERT INTO services (name, description, icon, price_range) VALUES
('Residential Interior Design', 'Complete home interior solutions tailored to your lifestyle and preferences.', 'home', '₹1,500 - ₹3,500/sq.ft'),
('Commercial Interior Design', 'Professional workspace designs that enhance productivity and brand identity.', 'office', '₹1,200 - ₹2,800/sq.ft'),
('Modular Kitchen', 'Custom-designed modular kitchens with premium finishes and smart storage solutions.', 'kitchen', '₹2,00,000 - ₹8,00,000'),
('Living Room Design', 'Elegant living spaces that combine comfort with sophisticated aesthetics.', 'sofa', '₹1,00,000 - ₹5,00,000'),
('Bedroom Design', 'Serene and stylish bedrooms designed for ultimate relaxation and comfort.', 'bed', '₹80,000 - ₹4,00,000'),
('Office Interior Design', 'Modern office interiors that reflect your company culture and values.', 'desk', '₹1,000 - ₹2,500/sq.ft');

-- Insert sample projects
INSERT INTO projects (name, category, location, description, image_url, area_sqft, completion_date, featured) VALUES
('Luxury Villa Interiors', 'Residential', 'Mumbai', 'Complete interior design for a 5BHK luxury villa with modern contemporary aesthetics.', 'villa-interior.jpg', 4500, '2025-06-15', TRUE),
('Corporate Office Space', 'Commercial', 'Bangalore', 'Modern office design for a tech startup with collaborative workspaces.', 'office-interior.jpg', 3200, '2025-08-20', TRUE),
('Modular Kitchen Premium', 'Kitchen', 'Delhi', 'Italian marble modular kitchen with smart storage and premium appliances.', 'kitchen-interior.jpg', 180, '2025-05-10', TRUE),
('Minimalist Living Room', 'Living Room', 'Pune', 'Scandinavian-inspired living room with neutral tones and natural materials.', 'living-room.jpg', 350, '2025-07-05', FALSE),
('Master Bedroom Suite', 'Bedroom', 'Hyderabad', 'Luxurious master bedroom with walk-in closet and spa-like bathroom.', 'bedroom-interior.jpg', 400, '2025-04-18', FALSE),
('Boutique Showroom', 'Commercial', 'Chennai', 'Contemporary retail space design for a fashion boutique.', 'showroom-interior.jpg', 1200, '2025-09-01', TRUE);

-- Insert sample testimonials
INSERT INTO testimonials (client_name, client_title, testimonial, rating) VALUES
('Rajesh Kumar', 'Homeowner, Mumbai', 'Exceptional design quality and attention to detail. They transformed our home into a masterpiece.', 5),
('Priya Sharma', 'CEO, TechStart Bangalore', 'Professional team with innovative ideas. Our office space now reflects our brand perfectly.', 5),
('Amit Patel', 'Business Owner, Delhi', 'The modular kitchen exceeded our expectations. Quality craftsmanship and timely delivery.', 5),
('Sneha Reddy', 'Interior Enthusiast, Hyderabad', 'Working with this team was a pleasure. They understood our vision and delivered beyond expectations.', 5);
