# # pylint: disable=C

# from flask import Blueprint, jsonify, request

# from models.bookmark import Bookmark
# from src import db

# bookmark_bp = Blueprint("bookmark", __name__)


# @bookmark_bp.route("/bookmarks", methods=["GET"])
# def get_bookmarks():
#     bookmarks = Bookmark.query.all()
#     return jsonify([{"id": b.id, "title": b.title, "url": b.url} for b in bookmarks])


# @bookmark_bp.route("/bookmarks", methods=["POST"])
# def add_bookmark():
#     data = request.json
#     new_bookmark = Bookmark(
#         title=data["title"], url=data["url"], user_id=data["user_id"]
#     )
#     db.session.add(new_bookmark)
#     db.session.commit()
#     return jsonify({"message": "Bookmark added successfully"}), 201


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
#     app.run(debug=True)
