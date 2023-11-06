from config import app, api
from flask import request, jsonify
from models import Post, Comment
from flask_restful import Resource
from sqlalchemy import func

# create routes here:
class Posts(Resource):
  def get(self):
    posts = [p.to_dict() for p in Post.query.all()]

    return posts, 200 

class SortedPosts(Resource):
  def get(self):
    posts = [p.to_dict() for p in Post.query.all()]
    sorted_posts = sorted(posts, key=lambda p: p['title'])
    
    return sorted_posts, 200

class PostsByAuthor(Resource):
  def get(self, author):
    posts = Post.query.filter(func.lower(Post.author)==author.lower()).all()
    posts_dict = [p.to_dict() for p in posts]
    
    return posts_dict, 200

class SearchPosts(Resource):
  def get(self, title):
    posts = Post.query.filter(Post.title.ilike(f"%{title}%")).all()
    # posts = Post.query.filter(func.lower(Post.title).contains(title.lower())).all()
    posts_dict = [p.to_dict() for p in posts]

    return posts_dict, 200
  
class PostsOrderedByComments(Resource):
  def get(self):
    posts = [p.to_dict() for p in Post.query.all()]
    sorted_posts = sorted(posts, key=lambda p: len(p['comments']), reverse=True)
    
    return sorted_posts, 200
  
class MostPopularCommenter(Resource):
  def get(self):
    comment_counts = {}
    most_popular_commenter = None
    most_comments = 0
    for post in Post.query.all():
      for comment in post.comments:
        commenter = comment.commenter
        if commenter in comment_counts:
          comment_counts[commenter] += 1
        else:
          comment_counts[commenter] = 1
        if comment_counts[commenter] > most_comments:
          most_comments = comment_counts[commenter]
          most_popular_commenter = commenter

    return { 'commenter': most_popular_commenter, 'count': most_comments }, 200


    

api.add_resource(Posts, '/api/posts')
api.add_resource(SortedPosts, '/api/sorted_posts')
api.add_resource(PostsByAuthor, '/api/posts_by_author/<string:author>')
api.add_resource(SearchPosts, '/api/search_posts/<string:title>')
api.add_resource(PostsOrderedByComments, '/api/posts_ordered_by_comments')
api.add_resource(MostPopularCommenter, '/api/most_popular_commenter')

if __name__ == "__main__":
  app.run(port=5555, debug=True)