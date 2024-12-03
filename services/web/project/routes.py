from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
import psycopg2
from math import ceil
import os


# Create a Blueprint
app_routes = Blueprint("app_routes", __name__)

# Database connection
def get_db_connection(db_type="master"):

    if db_type is None:
        db_type = session.get('db_type', 'master')  # Default to 'master' if no db_type is in the session

    # Default to the master database
    if db_type == "db2":
        db_url = os.getenv("DATABASE_URL_SLAVE1")
    elif db_type == "db3":
        db_url = os.getenv("DATABASE_URL_SLAVE2")
    else:
        db_url = os.getenv("DATABASE_URL_MASTER")
    
    # Parse the database URL (can be adjusted depending on your connection library)
    conn = psycopg2.connect(db_url)
    return conn

@app_routes.route("/", methods=["GET"])
def index():
    # Get the database type from the query parameter (or default to "master")
    db_type = request.args.get("db", "master")
    
    # Pagination setup
    page = request.args.get("page", 1, type=int)
    items_per_page = 100
    offset = (page - 1) * items_per_page

    # Search query parameters
    search_query = request.args.get("search", "")
    year_filter = request.args.get("year", None)
    month_filter = request.args.get("month", None)
    day_filter = request.args.get("day", None)
    sort_order = request.args.get("sort", "id_desc")

    query = "SELECT * FROM Public.games WHERE game_name ILIKE %s"
    params = [f"%{search_query}%"]

    # Add conditions based on filters
    if year_filter and year_filter != "None" and year_filter.strip():
        query += " AND release_year = %s"
        params.append(year_filter)

    if month_filter and month_filter != "None" and month_filter.strip():
        query += " AND release_month = %s"
        params.append(month_filter)

    if day_filter and day_filter != "None" and day_filter.strip():
        query += " AND release_day = %s"
        params.append(day_filter)

    if sort_order == "id_desc":
        query += " ORDER BY id DESC"
    else:
        query += f" ORDER BY release_year {sort_order}, release_month {sort_order}, release_day {sort_order}"

    query += " LIMIT %s OFFSET %s"
    params.extend([items_per_page, offset])

    # Database connection and query execution
    conn = get_db_connection(db_type)
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

    return render_template("index.html", games=games, page=page, total_pages=total_pages,
                           search_query=search_query, year_filter=year_filter, sort_order=sort_order,
                           month_filter=month_filter, day_filter=day_filter)

# Routes for handling database selection
@app_routes.route('/set_db', methods=['POST'])
def set_db():
    db_type = request.form.get('db_type')  # Get the selected db_type from the form
    session['db_type'] = db_type  # Store the selected db_type in the session for future requests
    return redirect(url_for('app_routes.index', db=db_type))  # Redirect back to the main page



@app_routes.route("/add", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        game_name = request.form["game_name"]
        release_year = request.form["release_year"]
        release_month = int(request.form["release_month"])
        release_day = int(request.form["release_day"])

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Public.games (game_name, release_year, release_month, release_day) VALUES (%s, %s, %s, %s)",
                    (game_name, release_year, release_month, release_day))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("app_routes.index"))

    return render_template("add_game.html")

@app_routes.route("/edit/<int:game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM Public.games WHERE id = %s", (game_id,))
    game = cur.fetchone()

    if request.method == "POST":
        game_name = request.form["game_name"]
        release_year = request.form["release_year"]
        release_month = request.form["release_month"]
        release_day = request.form["release_day"]

        cur.execute("UPDATE Public.games SET game_name = %s, release_year = %s, release_month = %s, release_day = %s WHERE id = %s",
                    (game_name, release_year, release_month, release_day, game_id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("app_routes.index"))

    cur.close()
    conn.close()

    return render_template("edit_game.html", game=game)

@app_routes.route("/delete/<int:game_id>", methods=["GET"])
def delete_game(game_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM Public.games WHERE id = %s", (game_id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("app_routes.index"))
