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
    """,
    "4_games_per_genre": """
        select ge.genre_name, count(g.id) as game_count
        from genre as ge 
        join game as g on ge.id = g.genre_id
        group by ge.genre_name
        order by game_count desc;
    """,
    "5_publishers_by_sales": """
        select p.publisher_name, sum(rs.num_sales) as total_sales
        from publisher as p
        join game_platform as gplat on p.id = gplat.game_publisher_id
        join region_sales as rs on gplat.id = rs.game_platform_id
        group by p.publisher_name
        order by total_sales desc
        limit 10;
    """,
    "6_yearly_sales": """
        select gplat.release_year, sum(rs.num_sales) as total_sales
        from game_platform as gplat
        join region_sales as rs on gplat.id = rs.game_platform_id
        group by gplat.release_year
        order by gplat.release_year;
    """,
    "7_platforms_by_sales": """
        select pl.platform_name, sum(rs.num_sales) as total_sales
        from platform as pl
        join game_platform as gplat on pl.id = gplat.platform_id
        join region_sales as rs on gplat.id = rs.game_platform_id
        group by pl.platform_name
        order by total_sales desc;
    """,
    "8_best_selling_genre_per_region": """
        select region_name, genre_name, total_sales
        from (
            select r.region_name, ge.genre_name, sum(rs.num_sales) as total_sales,
                   row_number() over (partition by r.region_name order by sum(rs.num_sales) desc) as rn
            from region as r
            join region_sales as rs on r.id = rs.region_id
            join game_platform as gplat on rs.game_platform_id = gplat.id
            join game_publisher as gpub on gplat.game_publisher_id = gpub.id
            join game as g on gpub.game_id = g.id
            join genre as ge on g.genre_id = ge.id
            group by r.region_name, ge.genre_name
        ) ranked
        where rn = 1
        order by total_sales desc;
    """,
    "9_platforms_by_game_count": """
        select p.platform_name, count(distinct g.id) as game_count
        from platform as p
        join game_platform as gplat on p.id = gplat.platform_id
        join game_publisher as gpub on gplat.game_publisher_id = gpub.id
        join game as g on gpub.game_id = g.id
        group by p.platform_name
        order by game_count desc;
    """,
    "10_cumulative_global_sales": """
        select gplat.release_year,
               sum(sum(rs.num_sales)) over (order by gplat.release_year) as cumulative_sales
        from game_platform as gplat
        join region_sales as rs on gplat.id = rs.game_platform_id
        group by gplat.release_year
        order by gplat.release_year;
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