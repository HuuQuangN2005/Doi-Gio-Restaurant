from restaurant.database.realtime.models import FirebaseModel

class User(FirebaseModel):
    
    FIREBASE_NODE = 'users'

    def __init__(self, username, email, country=None, key=None):
        super().__init__(key=key, username=username, email=email, country=country)

class Post(FirebaseModel):
    
    FIREBASE_NODE = 'posts'

    def __init__(self, title, content, authorId, key=None):
        super().__init__(key=key, title=title, content=content, authorId=authorId)

    def get_author(self):

        return User.get(self.authorId)
    
if __name__ == "__main__":
    new_user = User(username="admin", email="admin@ou.edu.vn", country="VN")
    new_user.save()
    user_key = new_user.key
    new_post = Post(
        title="ORM testing",
        content="123",
        authorId=user_key 
    )
    new_post.save()
    post_key = new_post.key

    fetched_post = Post.get(post_key)
    
    if fetched_post:
        print(f"post title: {fetched_post.title} (ID: {fetched_post.key})")
        
        author = fetched_post.get_author()
        if author:
            print(f"Author: {author.username} ({author.email})")

        fetched_post.title = "new info"
        fetched_post.save()
        print(f"post title: {Post.get(post_key).title}")


    all_users = User.all()
    print(f"user nums: {len(all_users)}")
    for u in all_users:
        print(f"- {u.username}, Email: {u.email}")