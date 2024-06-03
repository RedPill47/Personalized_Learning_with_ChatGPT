from api.models import User, Profile, Lesson, TaskResult, Feedback, QuizResult
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'learning_class', 'learning_level', 'lesson_types')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['verified'] = user.profile.verified
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    learning_class = serializers.CharField(max_length=50, required=False)
    learning_level = serializers.CharField(max_length=50, required=False)
    lesson_types = serializers.JSONField(required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'learning_class', 'learning_level', 'lesson_types' ,'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            learning_class=validated_data.get('learning_class', ''),
            learning_level=validated_data.get('learning_level', ''),
            lesson_types=validated_data.get('lesson_types', [])
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.learning_class = validated_data.get('learning_class', instance.learning_class)
        instance.learning_level = validated_data.get('learning_level', instance.learning_level)
        instance.lesson_types = validated_data.get('lesson_types', instance.lesson_types)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [ 'id',  'user',  'full_name' ]
    
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


# Crew AI serializers

class LessonSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'lesson_text', 'lesson_pdf', 'student']

class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ['id', 'lesson', 'task_type', 'result']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'student', 'task_result', 'feedback_text']

class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = '__all__'