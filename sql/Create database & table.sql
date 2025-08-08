CREATE DATABASE vgames;
USE vgames;

-- Create table
CREATE TABLE video_games (
	id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Platform VARCHAR(50),
    Year_of_Release INT,
    Genre VARCHAR(50),
    Publisher VARCHAR(255),]
    NA_Sales FLOAT,
    EU_Sales FLOAT,
    JP_Sales FLOAT,
    Other_Sales FLOAT,
    Global_Sales FLOAT,
    Critic_Score FLOAT,
    Critic_Count INT,
    User_Score FLOAT,
    User_Count INT,
    Rating VARCHAR(20)
)