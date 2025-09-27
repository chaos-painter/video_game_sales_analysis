# Video Game Sales Analytics

## Company
**Pixel Insights Ltd.**  
Pixel Insights is a data analytics consultancy specializing in entertainment and media industries.  
Our team provides publishers, developers, and investors with data-driven insights to better understand market trends, player behavior, and the commercial performance of video games across regions, platforms, and genres.

---

## Project Overview
This project focuses on analyzing **global video game sales** using a PostgreSQL database.  
We explore which games, genres, platforms, publishers, and regions drive the most sales, and how these patterns evolve over time.  
The analysis is performed through SQL queries and Python scripts that extract and summarize key performance metrics.

### Example Analytics
- Top 10 best-selling games worldwide
  
![best-selling games](query_result_screenshots/bestselling_games.png)

- Top regions by sales
  
![best-selling games](query_result_screenshots/regions_by_sales.png)

- Top genres by game count
  
![best-selling games](query_result_screenshots/genres_by_game_count.png)



## How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/videogame-analytics.git
cd videogame-analytics
```

### 2. Set Up PostgreSQL Database
- Install PostgreSQL (if not already installed).
- Create a database called `videogames`.
- Run the dump files.

### 3. Configure Database Connection
Update `DB_CONFIG` in `main.py` with your PostgreSQL credentials:
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "videogames",
    "user": "postgres",
    "password": "yourpassword"
}
```

### 4. Install Python Dependencies
```bash
pip install psycopg2
```

### 5. Run Analytics
```bash
python main.py
```
This will execute all predefined SQL queries and print results in the terminal.

---

## Sample SQL Queries
Below are example SQL queries used in the project to analyze the video game sales dataset:

### Top 10 Best-Selling Games Worldwide
```sql
select g.game_name, SUM(rs.num_sales) as total_sales
from game as g 
join game_publisher as gpub on g.id = gpub.game_id
join game_platform as gplat on gpub.id = gplat.game_publisher_id
join region_sales rs on gplat.id = rs.game_platform_id
group by g.game_name
order by total_sales desc
limit 10
```

### Top regions by sales
```sql
select r.region_name, sum(rs.num_sales) as total_sales
from region as r
join region_sales as rs on r.id = rs.region_id
group by r.region_name
order by total_sales DESC
limit 3
```

### Top genres by game count
```sql
select ge.genre_name, sum(rs.num_sales) as total_sales
from genre as ge
join game as g on ge.id = g.genre_id
join game_publisher as gpub on g.id = gpub.game_id
join game_platform as gplat on gpub.id = gplat.game_publisher_id
join region_sales as rs on gplat.id = rs.game_platform_id
group by ge.genre_name
order by total_sales desc
```


## Tools & Resources
- **PostgreSQL**: Relational database to store and query video game sales data.
- **Python (psycopg2)**: To connect to PostgreSQL and run SQL queries.
- **SQL**: For data extraction, aggregation, and analytics.
- **Git/GitHub**: For version control and collaboration.
- **Data Source**: Video Game Sales dataset (structured into tables: games, genres, publishers, platforms, regions, and sales).

---

## Next Steps
- Add visualizations (e.g., matplotlib, seaborn, or Tableau dashboards).
- Deploy results on a simple web interface for interactive exploration.
- Expand analysis with predictive models for future sales forecasting.