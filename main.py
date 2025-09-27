import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,             
    "dbname": "videogames",
    "user": "postgres",
    "password": "1234"
}


QUERIES = {
    "1_top_10_games": """
        select g.game_name, sum(rs.num_sales) as total_sales
        from game as g 
        join game_publisher as gpub on g.id = gpub.game_id
        join game_platform as gplat on gpub.id = gplat.game_publisher_id
        join region_sales rs on gplat.id = rs.game_platform_id
        group by g.game_name
        order by total_sales desc
        limit 10;
    """,
    "2_top_3_regions": """
        select r.region_name, sum(rs.num_sales) as total_sales
        from region as r
        join region_sales as rs on r.id = rs.region_id
        group by r.region_name
        order by total_sales desc
        limit 3;
    """,
    "3_genres_by_sales": """
        select ge.genre_name, sum(rs.num_sales) as total_sales
        from genre as ge
        join game as g on ge.id = g.genre_id
        join game_publisher as gpub on g.id = gpub.game_id
        join game_platform as gplat on gpub.id = gplat.game_publisher_id
        join region_sales as rs on gplat.id = rs.game_platform_id
        group by ge.genre_name
        order by total_sales desc;
    """
}

def run_queries():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("set search_path to video_games;")

        for name, query in QUERIES.items():
            print(f"\n--- {name.replace('_',' ').title()} ---")
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("error:", e)

if __name__ == "__main__":
    run_queries()
