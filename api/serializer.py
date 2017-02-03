from extuser.models import MyUser as User
from models import Post
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'date_of_birth',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'likes', 'authorName', )
        write_only_fields = ('title','text',)
        read_only_fields = ('id', 'likes', 'authorName', 'url',)
        depth = 1


    def get_validation_exclusions(self):
        exclusions = super(PostSerializer, self).get_validation_exclusions()
        return exclusions + ['author']


    def create(self, validated_data):
        user = self.context['request'].user
        post = Post.objects.create(
            title=validated_data['title'],
            text=validated_data['text'],
            author=user,
            authorName=str(user.last_name +" "+ user.first_name),
        )
        post.save()

        return post
