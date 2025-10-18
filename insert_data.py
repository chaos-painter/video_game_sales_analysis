import time
import random
import uuid
from sqlalchemy import text
from config import engine


EXISTING_GENRES = {
    "Action", "Adventure", "Fighting", "Misc", "Platform",
    "Puzzle", "Racing", "Role-Playing", "Shooter",
    "Simulation", "Sports", "Strategy"
}

NEW_GENRES = [
    "Survival", "Horror", "Stealth", "Open World", "Music",
    "Educational", "VR", "Card Game", "Sandbox"
]

PUBLISHERS = ["Atlus", "NovaWorks", "8Bit Realm", "Quantum Games"]
PLATFORMS = ["Steam Deck", "VR Quest", "Mobile Plus", "PC Cloud"]
REGIONS = ["North America", "Europe", "Asia", "Oceania", "Latin America"]

SESSION_ID = str(uuid.uuid4())


def insert_new_data():
    with engine.begin() as conn:
        for genre in NEW_GENRES:
            res = conn.execute(text("SELECT 1 FROM genre WHERE genre_name = :g"), {"g": genre}).fetchone()
            if not res:
                conn.execute(text("INSERT INTO genre (genre_name) VALUES (:g)"), {"g": genre})
                print(f"Inserted new genre: {genre}")

        genres = [row[0] for row in conn.execute(text("SELECT id FROM genre WHERE genre_name = 'Puzzle'"))]
        publishers = []
        for pub in PUBLISHERS:
            res = conn.execute(text("SELECT id FROM publisher WHERE publisher_name = :p"), {"p": pub}).fetchone()
            if not res:
                conn.execute(text("INSERT INTO publisher (publisher_name) VALUES (:p)"), {"p": pub})
            res = conn.execute(text("SELECT id FROM publisher WHERE publisher_name = :p"), {"p": pub}).fetchone()
            publishers.append(res[0])

        platforms = []
        for plat in PLATFORMS:
            res = conn.execute(text("SELECT id FROM platform WHERE platform_name = :p"), {"p": plat}).fetchone()
            if not res:
                conn.execute(text("INSERT INTO platform (platform_name) VALUES (:p)"), {"p": plat})
            res = conn.execute(text("SELECT id FROM platform WHERE platform_name = :p"), {"p": plat}).fetchone()
            platforms.append(res[0])

        regions = [row[0] for row in conn.execute(text("SELECT id FROM region"))]

    with engine.connect() as conn:
        for i in range(20):
            genre_id = random.choice(genres)
            publisher_id = random.choice(publishers)
            platform_id = random.choice(platforms)
            release_year = random.randint(2005, 2015)

            game_name = f"{random.choice(['Echo', 'Crimson', 'Frost', 'Abyss', 'Chrono'])} {random.choice(['Legacy', 'Haven', 'Run', 'Quest', 'Origin'])}"

            game_id = conn.execute(
                text("""
                    INSERT INTO game (genre_id, game_name)
                    VALUES (:genre_id, :game_name)
                    RETURNING id
                """),
                {"genre_id": genre_id, "game_name": game_name}
            ).scalar()

            game_publisher_id = conn.execute(
                text("""
                    INSERT INTO game_publisher (game_id, publisher_id)
                    VALUES (:game_id, :publisher_id)
                    RETURNING id
                """),
                {"game_id": game_id, "publisher_id": publisher_id}
            ).scalar()

            game_platform_id = conn.execute(
                text("""
                    INSERT INTO game_platform (game_publisher_id, platform_id, release_year)
                    VALUES (:game_publisher_id, :platform_id, :release_year)
                    RETURNING id
                """),
                {
                    "game_publisher_id": game_publisher_id,
                    "platform_id": platform_id,
                    "release_year": release_year
                }
            ).scalar()

            for region_id in regions:
                num_sales_millions = round(random.uniform(0.05, 100.0), 2)
                conn.execute(
                    text("""
                        INSERT INTO region_sales (region_id, game_platform_id, num_sales)
                        VALUES (:region_id, :game_platform_id, :num_sales)
                    """),
                    {"region_id": region_id, "game_platform_id": game_platform_id, "num_sales": num_sales_millions}
                )

            conn.execute(
                text("""
                    INSERT INTO inserted_records_log (session_id, game_id)
                    VALUES (:sid, :gid)
                """),
                {"sid": SESSION_ID, "gid": game_id}
            )
            conn.commit()
            print(f"Inserted game '{game_name}' ({release_year}) [Session: {SESSION_ID}]")
            time.sleep(2)


if __name__ == "__main__":
    print(f"Starting data insertion session: {SESSION_ID}")
    insert_new_data()
    print("Done inserting new data.")
