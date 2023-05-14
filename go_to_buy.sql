-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 12, 2023 at 09:34 AM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `go_to_buy`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`id`, `product_id`, `user_id`, `quantity`) VALUES
(5, 5, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address` text NOT NULL,
  `card_number` varchar(255) NOT NULL,
  `card_expiry` varchar(10) NOT NULL,
  `card_cvv` varchar(10) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `total`, `name`, `email`, `address`, `card_number`, `card_expiry`, `card_cvv`, `created_at`) VALUES
(1, 1, '123.00', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '545', '2023-05-12 05:06:04'),
(2, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:09:51'),
(3, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:13:38'),
(4, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:14:37'),
(5, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:15:23'),
(6, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:23:32'),
(7, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:25:00'),
(8, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:28:20'),
(9, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:29:58'),
(10, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:30:49'),
(11, 1, '19.97', 'joseph gitau', 'crosetsw09@gmail.com', '10300, 10200', '1212121212121212', '12121', '123', '2023-05-12 05:33:35');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`, `created_at`) VALUES
(1, 11, 1, 1, '2023-05-12 05:33:35'),
(2, 11, 1, 1, '2023-05-12 05:33:35'),
(3, 11, 1, 1, '2023-05-12 05:33:35');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `p_name` varchar(50) NOT NULL,
  `p_description` varchar(255) NOT NULL,
  `p_image` varchar(100) NOT NULL,
  `price` float NOT NULL,
  `quantity` int(11) NOT NULL,
  `carbon_footprint` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `p_name`, `p_description`, `p_image`, `price`, `quantity`, `carbon_footprint`) VALUES
(1, 'Organic Avocado', 'Fresh organic Hass avocado from California', 'avocado.jpg', 2.99, 200, 0.4),
(2, 'Grass-Fed Ribeye Steak', 'Grass-fed and -finished beef from a local ranch', 'steak.jpg', 19.99, 50, 0.7),
(3, 'Fair Trade Coffee', 'Medium roast coffee beans sourced from fair trade farms', 'coffee.jpg', 8.99, 150, 0.2),
(4, 'Reusable Water Bottle', 'Stainless steel water bottle with double-walled insulation', 'water_bottle.jpg', 15.99, 100, 0.1),
(5, 'Organic Kale', 'Fresh organic kale from a local farm', 'kale.jpg', 3.99, 300, 0.3),
(6, 'Eco-Friendly Laundry Detergent', 'Plant-based, non-toxic laundry detergent in a refillable container', 'laundry.jpg', 12.99, 75, 0.2);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `created_at`) VALUES
(1, 'burt', 'burt@gmail.com', '123', '2023-05-11 21:24:19');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
