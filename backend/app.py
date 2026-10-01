import os
import re
from datetime import datetime, date, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


# --------------------------------------------------
# Application setup
# --------------------------------------------------

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

app = Flask(
    __name__,
    template_folder=f"{ROOT}/frontend/templates",
    static_folder=f"{ROOT}/frontend/static"
)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "e-library-dev")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE}/e_library.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --------------------------------------------------
# Database Models
# --------------------------------------------------

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    isbn = db.Column(db.String(40), unique=True, nullable=False)
    year = db.Column(db.Integer)
    status = db.Column(
        db.String(20),
        default="Available",
        nullable=False
    )


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    membership = db.Column(
        db.String(30),
        default="Standard",
        nullable=False
    )
    joined_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("book.id"),
        nullable=False
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("member.id"),
        nullable=False
    )

    issue_date = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=False
    )

    return_date = db.Column(db.Date)

    book = db.relationship(
        "Book",
        backref="issues"
    )

    member = db.relationship(
        "Member",
        backref="issues"
    )


# --------------------------------------------------
# Starter Books
# --------------------------------------------------

BOOKS = [
    (
        "Python Crash Course",
        "Eric Matthes",
        "Programming",
        "9781593279288",
        2019
    ),
    (
        "Clean Code",
        "Robert C. Martin",
        "Programming",
        "9780132350884",
        2008
    ),
    (
        "Automate the Boring Stuff",
        "Al Sweigart",
        "Programming",
        "9781593275990",
        2019
    ),
    (
        "Learning JavaScript",
        "Ethan Brown",
        "Programming",
        "9781491952023",
        2019
    ),
    (
        "Fluent Python",
        "Luciano Ramalho",
        "Programming",
        "9781492056355",
        2022
    ),

    (
        "Docker Deep Dive",
        "Nigel Poulton",
        "Cloud & DevOps",
        "9781916585006",
        2024
    ),
    (
        "The Kubernetes Book",
        "Nigel Poulton",
        "Cloud & DevOps",
        "9781916585068",
        2024
    ),
    (
        "AWS for Beginners",
        "D. Roy",
        "Cloud & DevOps",
        "9781805123456",
        2023
    ),
    (
        "Linux Command Line",
        "William Shotts",
        "Cloud & DevOps",
        "9781593279523",
        2019
    ),
    (
        "The DevOps Handbook",
        "Gene Kim",
        "Cloud & DevOps",
        "9781950508402",
        2021
    ),

    (
        "SQL Cookbook",
        "Anthony Molinaro",
        "Database",
        "9780596009762",
        2005
    ),
    (
        "Learning SQL",
        "Alan Beaulieu",
        "Database",
        "9781492057611",
        2020
    ),
    (
        "PostgreSQL Up & Running",
        "Regina Obe",
        "Database",
        "9781491963418",
        2017
    ),
    (
        "Database System Concepts",
        "Silberschatz",
        "Database",
        "9780078022159",
        2019
    ),
    (
        "Designing Data-Intensive Applications",
        "Martin Kleppmann",
        "Database",
        "9781449373320",
        2017
    ),

    (
        "Computer Networking",
        "Andrew S. Tanenbaum",
        "Computer Science",
        "9780132126953",
        2011
    ),
    (
        "Operating System Concepts",
        "Silberschatz",
        "Computer Science",
        "9781119456339",
        2018
    ),
    (
        "Computer Organization",
        "Carl Hamacher",
        "Computer Science",
        "9780073523690",
        2011
    ),
    (
        "Artificial Intelligence",
        "Stuart Russell",
        "Computer Science",
        "9780134610993",
        2021
    ),
    (
        "Introduction to Algorithms",
        "Cormen, Leiserson, Rivest",
        "Computer Science",
        "9780262046305",
        2022
    )
]


# --------------------------------------------------
# Seed Database
# --------------------------------------------------

def seed():
    if Book.query.count() == 0:
        for title, author, category, isbn, year in BOOKS:
            db.session.add(
                Book(
                    title=title,
                    author=author,
                    category=category,
                    isbn=isbn,
                    year=year
                )
            )

        db.session.commit()


# --------------------------------------------------
# Dashboard Counts
# --------------------------------------------------

@app.context_processor
def counts():
    return {
        "book_count": Book.query.count(),
        "member_count": Member.query.count(),
        "issued_count": Book.query.filter_by(
            status="Issued"
        ).count(),
        "available_count": Book.query.filter_by(
            status="Available"
        ).count()
    }


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def index():

    cats = [
        (
            "Programming",
            "Code, Python, JavaScript and software development."
        ),
        (
            "Cloud & DevOps",
            "Linux, Docker, AWS and DevOps fundamentals."
        ),
        (
            "Database",
            "SQL, PostgreSQL and database design."
        ),
        (
            "Computer Science",
            "Algorithms, OS, networking and AI."
        )
    ]

    recent_books = (
        Book.query
        .order_by(Book.id.desc())
        .limit(6)
        .all()
    )

    return render_template(
        "index.html",
        categories=cats,
        recent_books=recent_books
    )


# --------------------------------------------------
# Books
# --------------------------------------------------

@app.route("/books")
def books():

    category = request.args.get(
        "category",
        ""
    ).strip()

    q = request.args.get(
        "q",
        ""
    ).strip()

    query = Book.query

    if category:
        query = query.filter(
            Book.category == category
        )

    if q:

        like = f"%{q}%"

        query = query.filter(
            db.or_(
                Book.title.ilike(like),
                Book.author.ilike(like),
                Book.category.ilike(like),
                Book.isbn.ilike(like)
            )
        )

    all_categories = sorted(
        {
            book.category
            for book in Book.query.all()
        }
    )

    return render_template(
        "books.html",
        books=query.order_by(Book.title).all(),
        categories=all_categories,
        selected_category=category,
        q=q
    )


# --------------------------------------------------
# Add Book
# --------------------------------------------------

@app.route(
    "/books/add",
    methods=["GET", "POST"]
)
def add_book():

    if request.method == "POST":

        f = request.form

        isbn = f.get(
            "isbn",
            ""
        ).strip()

        if Book.query.filter_by(
            isbn=isbn
        ).first():

            flash(
                "A book with this ISBN already exists.",
                "error"
            )

            return redirect(
                url_for("add_book")
            )

        year = (
            int(f["year"])
            if f.get("year")
            else None
        )

        book = Book(
            title=f.get("title", "").strip(),
            author=f.get("author", "").strip(),
            category=f.get("category", "").strip(),
            isbn=isbn,
            year=year
        )

        db.session.add(book)
        db.session.commit()

        flash(
            "Book added successfully.",
            "success"
        )

        return redirect(
            url_for("books")
        )

    return render_template(
        "add_book.html"
    )


# --------------------------------------------------
# Members
# --------------------------------------------------

@app.route("/members")
def members():

    members_list = (
        Member.query
        .order_by(Member.id.desc())
        .all()
    )

    return render_template(
        "members.html",
        members=members_list
    )


# --------------------------------------------------
# Add Member
# --------------------------------------------------

@app.route(
    "/members/add",
    methods=["GET", "POST"]
)
def add_member():

    if request.method == "POST":

        print(
            "MEMBER FORM:",
            request.form.to_dict(),
            flush=True
        )

        f = request.form

        name = f.get(
            "name",
            ""
        ).strip()

        email = f.get(
            "email",
            ""
        ).strip()

        phone = re.sub(
            r"\D",
            "",
            f.get("phone", "")
        )

        address = f.get(
            "address",
            ""
        ).strip()

        membership = f.get(
            "membership",
            "Standard"
        ).strip()

        # Required fields
        if not name or not email or not address:

            flash(
                "Please complete all required member details.",
                "error"
            )

            return redirect(
                url_for("add_member")
            )

        # Phone validation
        if not re.fullmatch(
            r"[0-9]{10}",
            phone
        ):

            flash(
                "Mobile number must contain exactly 10 digits.",
                "error"
            )

            return redirect(
                url_for("add_member")
            )

        # Email validation
        if not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email
        ):

            flash(
                "Please enter a valid email address.",
                "error"
            )

            return redirect(
                url_for("add_member")
            )

        # Create member
        member = Member(
            name=name,
            email=email,
            phone=phone,
            address=address,
            membership=membership
        )

        db.session.add(member)
        db.session.commit()

        flash(
            "Membership created successfully.",
            "success"
        )

        return redirect(
            url_for("members")
        )

    return render_template(
        "add_member.html"
    )


# --------------------------------------------------
# Issue Book
# --------------------------------------------------

@app.route(
    "/issue",
    methods=["GET", "POST"]
)
def issue_book():

    if request.method == "POST":

        book = db.session.get(
            Book,
            int(request.form["book_id"])
        )

        member = db.session.get(
            Member,
            int(request.form["member_id"])
        )

        if not book or not member:

            flash(
                "Please select a valid book and member.",
                "error"
            )

        elif book.status != "Available":

            flash(
                "That book is currently issued.",
                "error"
            )

        else:

            issue = Issue(
                book=book,
                member=member,
                issue_date=date.today(),
                due_date=date.today() + timedelta(days=14)
            )

            db.session.add(issue)

            book.status = "Issued"

            db.session.commit()

            flash(
                "Book issued successfully.",
                "success"
            )

        return redirect(
            url_for("issue_book")
        )

    available_books = (
        Book.query
        .filter_by(status="Available")
        .order_by(Book.title)
        .all()
    )

    members_list = (
        Member.query
        .order_by(Member.name)
        .all()
    )

    return render_template(
        "issue_book.html",
        available_books=available_books,
        members=members_list
    )


# --------------------------------------------------
# Issue History
# --------------------------------------------------

@app.route("/issues")
def issues():

    issue_list = (
        Issue.query
        .order_by(Issue.id.desc())
        .all()
    )

    return render_template(
        "issues.html",
        issues=issue_list
    )


# --------------------------------------------------
# Return Book
# --------------------------------------------------

@app.post(
    "/issues/<int:issue_id>/return"
)
def return_book(issue_id):

    issue = db.session.get(
        Issue,
        issue_id
    )

    if not issue or issue.return_date:

        flash(
            "This issue record is already closed.",
            "error"
        )

    else:

        issue.return_date = date.today()

        issue.book.status = "Available"

        db.session.commit()

        flash(
            "Book returned successfully.",
            "success"
        )

    return redirect(
        url_for("issues")
    )


# --------------------------------------------------
# Initialize Database
# --------------------------------------------------

with app.app_context():

    db.create_all()
    seed()


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv(
                "PORT",
                "5000"
            )
        ),
        debug=True
    )
