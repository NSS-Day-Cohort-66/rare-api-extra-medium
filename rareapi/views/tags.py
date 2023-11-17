from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from rareapi.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "label"]


class TagViewSet(viewsets.ViewSet):
    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        label = request.data.get("label")

        # Create a comment database row first, so you have a
        # primary key to work with
        tag = Tag.objects.create(
            # maybe issues with label /  request.user
            label=label
        )

        serializer = TagSerializer(tag, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this tag?
            self.check_object_permissions(request, tag)

            serializer = TagSerializer(data=request.data)
            if serializer.is_valid():
                tag.label = serializer.validated_data["label"]
                # tag.created_on = serializer.validated_data["created_on"]
                tag.save()

                serializer = TagSerializer(tag, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)
            self.check_object_permissions(request, tag)
            tag.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
