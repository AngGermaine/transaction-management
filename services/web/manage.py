from flask.cli import FlaskGroup
from project import app,db,Game
import csv

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    # Path to your CSV file
    csv_file = '/usr/src/app/games.csv'

    # Open and read the CSV file
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {k.strip(): v for k, v in row.items()}

            # Create a new Game object for each row in the CSV
            game = Game(
                game_name=row['game_name'],
                release_year=int(row['release_year']),
                release_month=int(row['release_month']),
                release_day=int(row['release_day'])
            )

            # Add the game to the session
            db.session.add(game)

        # Commit the changes to the database
        db.session.commit()

    print("Database seeded with games from CSV.")

if __name__ == "__main__":
    cli()
