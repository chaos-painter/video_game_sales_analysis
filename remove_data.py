from sqlalchemy import text
from config import engine

def remove_data(session_id: str):
    with engine.begin() as conn:
        games = conn.execute(
            text("SELECT game_id FROM inserted_records_log WHERE session_id = :sid"),
            {"sid": session_id}
        ).fetchall()
        game_ids = [g[0] for g in games]

        if not game_ids:
            print("⚠️ No records found for that session_id.")
            return

        for game_id in game_ids:
            # Get related records
            gp_ids = [row[0] for row in conn.execute(text("SELECT id FROM game_publisher WHERE game_id = :gid"), {"gid": game_id})]
            for gp_id in gp_ids:
                gplat_ids = [row[0] for row in conn.execute(text("SELECT id FROM game_platform WHERE game_publisher_id = :gpid"), {"gpid": gp_id})]
                for gplat_id in gplat_ids:
                    conn.execute(text("DELETE FROM region_sales WHERE game_platform_id = :id"), {"id": gplat_id})
                    conn.execute(text("DELETE FROM game_platform WHERE id = :id"), {"id": gplat_id})
                conn.execute(text("DELETE FROM game_publisher WHERE id = :id"), {"id": gp_id})

            conn.execute(text("DELETE FROM game WHERE id = :id"), {"id": game_id})
            print(f"Removed game ID {game_id}")

        conn.execute(text("DELETE FROM inserted_records_log WHERE session_id = :sid"), {"sid": session_id})

    print(f"Removed all data from session {session_id}")

if __name__ == "__main__":
    sid = input("Enter session ID to remove: ").strip()
    remove_data(sid)
