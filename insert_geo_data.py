import json
import uuid
from sqlalchemy import text
from config import engine

SESSION_ID = str(uuid.uuid4())

def assign_countries_to_publishers():
    with open("publisher_countries.json", "r", encoding="utf-8") as f:
        country_map = json.load(f)

    with engine.begin() as conn:
        conn.execute(text("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name = 'publisher' AND column_name = 'country'
                ) THEN
                    ALTER TABLE publisher ADD COLUMN country VARCHAR(100);
                END IF;
            END$$;
        """))

        publishers = conn.execute(text("SELECT id, publisher_name FROM publisher")).fetchall()

        for pub_id, name in publishers:
            country = None
            for key, val in country_map.items():
                if key.lower() == name.lower():
                    country = val
                    break

            if not country:
                country = "Unknown"

            conn.execute(
                text("""
                    UPDATE publisher
                    SET country = :country
                    WHERE id = :pid
                """),
                {"country": country, "pid": pub_id}
            )

            print(f"Updated {name}: country = {country}")

    print("Done assigning countries to publishers.")


if __name__ == "__main__":
    assign_countries_to_publishers()
    print(f"Starting data insertion session: {SESSION_ID}")