from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from math import ceil

app = Flask(__name__)

# Connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        dbname='games', 
        user='postgres', 
        password='admin', 
        host='localhost', 
        port='5432'
    )
    return conn

@app.route('/', methods=['GET'])
def index():
    # Pagination setup
    page = request.args.get('page', 1, type=int)  # Get page number, default to 1
    items_per_page = 100
    offset = (page - 1) * items_per_page

    # Search query parameters
    search_query = request.args.get('search', '')
    year_filter = request.args.get('year', None)
    month_filter = request.args.get('month', None)  # Get month filter
    day_filter = request.args.get('day', None)  # Get day filter
    sort_order = request.args.get('sort', 'id_desc')  # Default sort by 'id_desc'

    # Build SQL query with filters and pagination
    query = "SELECT * FROM Public.games WHERE game_name ILIKE %s"
    params = [f"%{search_query}%"]  # Using ILIKE for case-insensitive search

    if year_filter:
        query += " AND release_year = %s"
        params.append(year_filter)

    if month_filter:
        query += " AND release_month = %s"
        params.append(month_filter)

    if day_filter:
        query += " AND release_day = %s"
        params.append(day_filter)

    # Add sorting logic based on the sort order
    if sort_order == 'id_desc':
        query += " ORDER BY id DESC"  # Sort by ID in descending order (recently added first)
    else:
        query += f" ORDER BY release_year {sort_order}, release_month {sort_order}, release_day {sort_order}"

    query += " LIMIT %s OFFSET %s"
    params.extend([items_per_page, offset])

    # Execute the query
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, tuple(params))
    games = cur.fetchall()

    # Get total number of records for pagination
    cur.execute("SELECT COUNT(*) FROM Public.games WHERE game_name ILIKE %s", (f"%{search_query}%",))
    total_records = cur.fetchone()[0]

    cur.close()
    conn.close()

    # Calculate the number of pages
    total_pages = ceil(total_records / items_per_page)

    return render_template('index.html', games=games, page=page, total_pages=total_pages,
                           search_query=search_query, year_filter=year_filter, sort_order=sort_order,
                           month_filter=month_filter, day_filter=day_filter)



@app.route('/add', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        # Get the game details from the form
        game_name = request.form['game_name']
        release_year = request.form['release_year']
        release_month = int(request.form['release_month'])  # Convert month to integer
        release_day = int(request.form['release_day'])  # Convert day to integer

        # Insert into the database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Public.games (game_name, release_year, release_month, release_day) VALUES (%s, %s, %s, %s)",
                    (game_name, release_year, release_month, release_day))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))  # Redirect to the main page after adding

    return render_template('add_game.html')



@app.route('/edit/<int:game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch the game to edit
    cur.execute("SELECT * FROM Public.games WHERE id = %s", (game_id,))
    game = cur.fetchone()

    if request.method == 'POST':
        # Get the updated game details from the form
        game_name = request.form['game_name']
        release_year = request.form['release_year']
        release_month = request.form['release_month']
        release_day = request.form['release_day']

        # Update the game in the database
        cur.execute("UPDATE Public.games SET game_name = %s, release_year = %s, release_month = %s, release_day = %s WHERE id = %s",
                    (game_name, release_year, release_month, release_day, game_id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))  # Redirect to the main page after updating

    cur.close()
    conn.close()

    return render_template('edit_game.html', game=game)


@app.route('/delete/<int:game_id>', methods=['GET'])
def delete_game(game_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Delete the game from the database
    cur.execute("DELETE FROM Public.games WHERE id = %s", (game_id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))  # Redirect to the main page after deleting


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
