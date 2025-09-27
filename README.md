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

### ERD Diagram
![erd](ERD_Diagram.png)


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