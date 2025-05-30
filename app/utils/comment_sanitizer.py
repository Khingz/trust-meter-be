def sanitize_user(user: dict):
    return {
        "id": user.get("id"),
        "name": user.get("name"),
        "email": user.get("email"),
    }

def sanitize_comment(comment: dict):
    return {
        "id": comment.get("id"),
        "user_id": comment.get("user_id"),
        "review_id": comment.get("review_id"),
        "content": comment.get("content"),
        "created_at": comment.get("created_at"),
        "updated_at": comment.get("updated_at"),
        "user": sanitize_user(comment.get("user", {})),
        "likes": comment.get("likes", [])
    }
