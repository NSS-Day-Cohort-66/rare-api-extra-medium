from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comment, RareUser, Post
from .users import RareUserSerializer
from .posts import PostSerializer

class CommentSerializer(serializers.ModelSerializer):
    # !Unsure of which user serializer to use. Don't forget to import UserSerializer from .users
    # user = UserSerializer(many=False)
    author = RareUserSerializer(many=False)
    is_owner = serializers.SerializerMethodField()
    post = PostSerializer(many=False)

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context["request"].user == obj.author.user

    class Meta:
        model = Comment
        fields = [
            "id",
            # "user",
            "post",
            "author",
            "content",
            "is_owner",
        ]
        # read_only_field = ["user"]


class CommentViewSet(viewsets.ViewSet):
    def list(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(
            comments, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={"request": request})
            return Response(serializer.data)

        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        post = Post.objects.get(pk=request.data["post"])
        author = RareUser.objects.get(pk=request.data["author"])
        content = request.data.get("content")
        created_on = request.data.get("created_on")

        # Create a comment database row first, so you have a
        # primary key to work with
        comment = Comment.objects.create(
            # maybe issues with post /  request.user
            post=post,
            author=author,
            content=content,
            created_on=created_on,
        )

        serializer = CommentSerializer(comment, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this comment?
            self.check_object_permissions(request, comment)

            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                comment.post = serializer.validated_data["post"]
                comment.author = serializer.validated_data["author"]
                comment.content = serializer.validated_data["content"]
                comment.created_on = serializer.validated_data["created_on"]
                comment.save()

                serializer = CommentSerializer(comment, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            self.check_object_permissions(request, comment)
            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
