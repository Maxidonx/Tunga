from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for blog posts
posts = []

@app.route('/', methods=['GET'])
def homepage():
    return "This is my Home Page"

# CREATE a new blog post
@app.route('/create-post', methods=['POST'])
def create_post():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Title and content required"}), 400

    post = {
        "id": len(posts) + 1,
        "title": data["title"],
        "content": data["content"]
    }
    posts.append(post)
    return jsonify(post), 201

# READ all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

# READ a single blog post
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if post:
        return jsonify(post)
    return jsonify({"error": "Post not found"}), 404

# UPDATE a blog post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    for post in posts:
        if post["id"] == post_id:
            post["title"] = data.get("title", post["title"])
            post["content"] = data.get("content", post["content"])
            return jsonify(post)
    return jsonify({"error": "Post not found"}), 404

# DELETE a blog post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p["id"] != post_id]
    return jsonify({"message": "Post deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
