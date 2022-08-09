-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 09, 2022 at 09:39 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stream`
--

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

CREATE TABLE `comment` (
  `username` varchar(128) NOT NULL,
  `video` varchar(256) NOT NULL,
  `text` varchar(1024) NOT NULL DEFAULT 'no comment'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`username`, `video`, `text`) VALUES
('user4', 'pishro.mp4', 'wow');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `id` varchar(128) NOT NULL,
  `user` varchar(128) NOT NULL,
  `assignee` varchar(128) DEFAULT NULL,
  `text` varchar(1024) NOT NULL,
  `reply` varchar(1024) DEFAULT NULL,
  `state` varchar(16) NOT NULL DEFAULT 'NEW'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`id`, `user`, `assignee`, `text`, `reply`, `state`) VALUES
('8e00e928-b7a1-4d2f-b249-efd243c5abe9', 'user4', NULL, 'heeelp', NULL, 'CLOSED'),
('86204ce8-dfc6-41a2-be24-36c196ce8372', 'user4', 'admin3', 'noooooo', 'hmmmmmmmm', 'PENDING'),
('38d4f448-721e-4562-b11c-71bcfd2ed7d7', 'admin3', NULL, 'super admin it\'s me mario', NULL, 'NEW'),
('0ddce22d-ca6a-4de0-8dcb-2d323889c59b', 'admin3', NULL, 'super admin it\'s me mario', NULL, 'NEW'),
('3e550b2f-fdb5-4b9a-ae30-33e66a61adef', 'admin3', NULL, 'super admin it\'s me mario', NULL, 'NEW'),
('b0b9373d-1fd3-4243-890d-eed5c63f3dd7', 'admin3', NULL, 'hey super admin e lanati chetori', NULL, 'NEW'),
('5d7e706e-9035-4b52-abde-5e84163aa43f', 'admin3', 'manager', 'heeeelp', NULL, 'PENDING'),
('5b10cbdf-12d9-4536-802c-bc3a7b1f38cd', 'admin3', 'manager', 'hmmmmmmm', NULL, 'NEW'),
('9b092264-48f1-4719-ad1e-05a33af0921a', 'admin3', 'manager', 'wowowow', NULL, 'CLOSED');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `strikes` int(16) NOT NULL DEFAULT 0,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `is_approved` int(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `password`, `strikes`, `is_admin`, `is_approved`) VALUES
('admin1', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 0, 1, 1),
('admin2', '173af653133d964edfc16cafe0aba33c8f500a07f3ba3f81943916910c257705', 0, 1, 1),
('admin3', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 0, 1, 1),
('manager', 'dummy password', 0, 1, 1),
('user', 'c2be913485d6a963507d8c7f769d133749788e31e1ce508a284e80dd706dd785', 0, 0, 1),
('user1', '123', 0, 1, 1),
('user2', 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35', 0, 0, 0),
('user3', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 0, 1, 1),
('user4', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `video`
--

CREATE TABLE `video` (
  `title` varchar(256) NOT NULL,
  `name_identifier` varchar(128) NOT NULL,
  `owner` varchar(128) NOT NULL,
  `adrs` varchar(512) NOT NULL,
  `available` tinyint(1) NOT NULL DEFAULT 1,
  `likes` tinyint(1) NOT NULL DEFAULT 0,
  `dislikes` tinyint(1) NOT NULL DEFAULT 0,
  `label` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `video`
--

INSERT INTO `video` (`title`, `name_identifier`, `owner`, `adrs`, `available`, `likes`, `dislikes`, `label`) VALUES
('pishro.mp4', 'b240c9f0-574c-4e56-86cf-273c992f4b8b', 'user', '/home/re/Documents/darC/1401_1/videos/pishro.mp4', 1, 6, 0, ', dangerous');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comment`
--
ALTER TABLE `comment`
  ADD KEY `video` (`video`),
  ADD KEY `user` (`username`) USING BTREE;

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD KEY `user_f` (`user`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `video`
--
ALTER TABLE `video`
  ADD PRIMARY KEY (`title`),
  ADD KEY `name_id` (`name_identifier`),
  ADD KEY `owner` (`owner`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `user` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `video` FOREIGN KEY (`video`) REFERENCES `video` (`title`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `user_f` FOREIGN KEY (`user`) REFERENCES `user` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `video`
--
ALTER TABLE `video`
  ADD CONSTRAINT `owner` FOREIGN KEY (`owner`) REFERENCES `user` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;