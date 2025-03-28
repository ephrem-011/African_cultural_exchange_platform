from django.db import models
from users.models import userProfiles
class Post(models.Model):
    Title = models.CharField(max_length=300)
    user_id = models.ForeignKey(userProfiles, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_number_of_likes(self):
        return Like.objects.filter(post_id = self.id).count()

    def __str__(self):
        return self.Title
class Like(models.Model):
    user_id = models.ForeignKey(userProfiles, on_delete=models.CASCADE)
    post_id = models.ForeignKey (Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'post_id'], name='unique_like')
        ]
class Comment(models.Model):
    user_id = models.ForeignKey(userProfiles, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def get_post_id(self):
        return self.post_id
    class Meta:
        constraints = [models.UniqueConstraint(fields=['user_id', 'post_id', 'created_at'], name = 'unique_comment')]
