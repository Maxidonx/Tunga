from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for blog posts
posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            return render_template('create_post.html', error="Title and Content are required!")

        post = {
            "id": len(posts) + 1,
            "title": title,
            "content": content
        }
        posts.append(post)
        return redirect(url_for('index'))

    return render_template('create_post.html')

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return "Post not found!", 404
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return "Post not found!", 404

    if request.method == 'POST':
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")
        return redirect(url_for('index'))

    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p["id"] != post_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
