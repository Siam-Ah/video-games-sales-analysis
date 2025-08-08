USE vgames;

-- DATASET OVERVIEW
-- Count total rows
SELECT COUNT(*) AS total_games FROM video_games;

-- Count distinct categories
SELECT 	COUNT(DISTINCT Platform) AS platforms,
		COUNT(DISTINCT Genre) AS genres,
		COUNT(DISTINCT Publisher) AS publishers,
        COUNT(DISTINCT Rating) AS rating
FROM video_games;

-- Year range
SELECT 	MIN(Year_of_Release) AS first_year,
		MAX(Year_of_Release) AS last_year
FROM video_games;

-- TOP SELLERS
-- Top 10 games by global sales
SELECT Name, Platform, Global_Sales
FROM video_games
ORDER BY Global_Sales DESC
LIMIT 10;

-- Top 10 platforms by total global sales
SELECT Platform, SUM(Global_Sales) AS total_sales
FROM video_games
GROUP BY Platform
ORDER BY total_sales DESC
LIMIT 10;

-- REGIONAL SALES
-- Top sales per region
SELECT
	SUM(NA_Sales) AS na_sales,
    SUM(EU_Sales) AS eu_sales,
    SUM(JP_Sales) AS jp_sales,
    SUM(Other_Sales) AS other_sales,
    SUM(Global_Sales) AS global_sales
FROM video_games;

-- Region with highest average sales per game
SELECT 'NA' AS region, AVG(NA_Sales) AS avg_sales FROM video_games
UNION ALL
SELECT 'EU', AVG(EU_Sales) FROM video_games
UNION ALL
SELECT 'JP', AVG(JP_Sales) from video_games
UNION ALL
Select 'Other', AVG(Other_sales) FROM video_games
ORDER BY avg_sales DESC;

-- GENRE ANALYSIS
-- Top genres by global sales
SELECT Genre, SUM(Global_Sales) AS total_sales
FROM video_games
GROUP BY Genre
ORDER BY total_sales DESC;

-- Genres with highest average critic scores
SELECT 	Genre, 
		ROUND(AVG(Critic_Score),2) AS avg_critic_score,
        ROUND(AVG(USER_Score),2) AS avg_user_score
FROM video_games
GROUP BY Genre
ORDER BY SUM(Global_Sales) DESC;

-- PUBLISHER INSIGHTS
-- Top publishers by global sales
SELECT Publisher, SUM(Global_Sales) AS total_sales
FROM  video_games
GROUP BY Publisher
ORDER BY total_sales DESC
LIMIT 10;

-- Average critic & user scores per publisher (top 10 by sales)
SELECT 	Publisher,
		ROUND(AVG(Critic_Score),2) AS avg_critic_score,
        ROUND(AVG(User_Score),2) AS avg_user_score
FROM video_games
GROUP BY Publisher
ORDER BY SUM(Global_Sales) DESC
LIMIT 10;

-- TIME TRENDS
-- Sales by year
SELECT Year_of_Release, SUM(Global_Sales) AS total_sales
FROM video_games
GROUP BY Year_of_Release
ORDER BY Year_of_Release;

-- Genre popularity by decade
SELECT 	(Year_of_Release DIV 10) * 10 AS decade, Genre,
		SUM(Global_Sales) AS total_sales
FROM video_games
GROUP BY decade, Genre
ORDER BY decade, total_sales DESC;

-- SCORES & SALES RELATIONSHIP
-- Correlation-like check: Average sales grouped by critic score buckets
SELECT 	FLOOR(Critic_Score/10)*10 AS critic_bucket,
		AVG(Global_Sales) AS avg_sales
FROM video_games
GROUP BY critic_bucket
ORDER BY critic_bucket;

-- PLATFORM LIFESPAN
SELECT Platform, MIN(Year_of_Release) AS first_year, MAX(Year_of_Release) AS last_year
FROM video_games
GROUP BY Platform
ORDER BY first_year;

-- REGIONAL GENRE PREFERENCES
(
  SELECT 'NA' AS region, Genre, SUM(NA_Sales) AS sales
  FROM video_games 
  GROUP BY Genre
  ORDER BY sales DESC 
  LIMIT 1
)
UNION ALL
(
  SELECT 'EU' AS region, Genre, SUM(EU_Sales) AS sales
  FROM video_games 
  GROUP BY Genre
  ORDER BY sales DESC 
  LIMIT 1
)
UNION ALL
(
  SELECT 'JP' AS region, Genre, SUM(JP_Sales) AS sales
  FROM video_games 
  GROUP BY Genre
  ORDER BY sales DESC 
  LIMIT 1
)
UNION ALL
(
  SELECT 'Other' AS region, Genre, SUM(Other_Sales) AS sales
  FROM video_games 
  GROUP BY Genre
  ORDER BY sales DESC 
  LIMIT 1
);

-- SALES-TO-SCORE RATIO
SELECT Name, Platform, Critic_Score, User_Score, Global_Sales
FROM video_games
WHERE Critic_Score >= 85 AND Global_Sales > 5
ORDER BY Global_Sales DESC;
