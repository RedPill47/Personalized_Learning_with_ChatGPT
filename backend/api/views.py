import os
import json
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Profile, Lesson, TaskResult, Feedback, QuizResult
from .serializer import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer, UserSerializer, LessonSerializer, TaskResultSerializer, FeedbackSerializer, QuizResultSerializer
from .crewai.crew_setup import TutorCrew
from django.conf import settings

logger = logging.getLogger(__name__)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulations {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "Hello buddy"
        data = f'Congratulations your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# Crew AI views

class SubmitLessonView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = request.user.profile
        lesson_data = request.data.copy()
        lesson_serializer = LessonSerializer(data=lesson_data)
        
        if lesson_serializer.is_valid():
            lesson = lesson_serializer.save(student=profile)
            
            tutor_crew = TutorCrew(user_id=profile.user.id, lesson_id=lesson.id)
            pdf_path = tutor_crew.run_all_tasks()
            
            task_results = TaskResult.objects.filter(lesson=lesson)
            serialized_results = TaskResultSerializer(task_results, many=True)

            print(f"Generated PDF Path: {pdf_path}")
            
            return Response({
                'task_results': serialized_results.data,
                'pdf_path': pdf_path,
                'lesson_id': lesson.id  # Make sure to return the lesson ID
            }, status=status.HTTP_201_CREATED)
        else:
            # Log the validation errors
            print("Validation Errors:", lesson_serializer.errors)
            return Response(lesson_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetTaskResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lesson_id):
        task_results = TaskResult.objects.filter(lesson_id=lesson_id)
        serializer = TaskResultSerializer(task_results, many=True)
        return Response(serializer.data)

class ProvideFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        profile = request.user.profile
        lesson = Lesson.objects.get(id=lesson_id)
        feedback_data = request.data.get('feedback')
        agent_key = request.data.get('agent_key')
        task_type = request.data.get('task_type')

        tutor_crew = TutorCrew(user_id=profile.user.id, lesson_id=lesson.id)

        updated_result = tutor_crew.execute_agent_task(agent_key, task_type, feedback_data)

        task_result = TaskResult.objects.create(
            lesson=lesson,
            task_type=task_type,
            result=updated_result
        )

        feedback = Feedback.objects.create(
            student=profile,
            task_result=task_result,
            feedback_text=feedback_data
        )

        return Response(TaskResultSerializer(task_result).data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz_data(request):
    logger.info("get_quiz_data called")
    try:
        file_path = os.path.join('output_files', 'quiz.json')
        if not os.path.exists(file_path):
            logger.error(f"Quiz file not found: {file_path}")
            return Response({'error': 'Quiz data not found.'}, status=status.HTTP_404_NOT_FOUND)
        with open(file_path) as quiz_file:
            quiz_data = json.load(quiz_file)
        return JsonResponse(quiz_data, safe=False)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing quiz data: {e}")
        return Response({'error': 'Error parsing quiz data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SubmitQuizResultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        quiz_data = request.data.get('quiz_data')
        score = request.data.get('score')
        
        # Create a new QuizResult object
        quiz_result = QuizResult.objects.create(user=user, quiz_data=quiz_data, score=score)
        
        return Response({'message': 'Quiz results saved successfully!'}, status=status.HTTP_201_CREATED)

class FetchQuizResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        quiz_results = QuizResult.objects.filter(user=user)
        serializer = QuizResultSerializer(quiz_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_flashcards_data(request):
    logger.info("get_flashcards_data called")
    try:
        file_path = os.path.join('output_files', 'flashcards.json')
        if not os.path.exists(file_path):
            logger.error(f"Flashcards file not found: {file_path}")
            return Response({'error': 'Flashcards data not found.'}, status=status.HTTP_404_NOT_FOUND)
        with open(file_path) as flashcards_file:
            flashcards_data = json.load(flashcards_file)
        return JsonResponse(flashcards_data, safe=False)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing flashcards data: {e}")
        return Response({'error': 'Error parsing flashcards data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot_response(request):
    logger.info("chatbot_response called")
    user_message = request.data.get('message')
    user_id = request.user.id
    lesson_id = request.data.get('lesson_id')
    agent_key = request.data.get('agent_key')
    task_type = request.data.get('task_type')
    quiz_results = request.data.get('quiz_results')

    if not user_message:
        return Response({'error': 'No message provided.'}, status=status.HTTP_400_BAD_REQUEST)
    if not lesson_id:
        return Response({'error': 'No lesson_id provided.'}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve user data
    user = request.user
    profile = user.profile

    try:
        # Create the TutorCrew instance for communication chatbot
        tutor_crew = TutorCrew(
            user_id=user_id,
            lesson_id=lesson_id,
            quiz_results=quiz_results  # Pass quiz results to the TutorCrew
        )
        # Execute the communication_chatbot task if no specific agent or task type is provided
        if not agent_key and not task_type:
            response = tutor_crew.execute_agent_task(
                agent_key="communication_chatbot",
                task_type=None,
                feedback=user_message
            )
        else:
            response = tutor_crew.execute_agent_task(
                agent_key=agent_key,
                task_type=task_type,
                feedback=user_message
            )

        return JsonResponse({'response': response}, safe=False)
    except TypeError as e:
        logger.error(f"TypeError during chatbot response: {e}")
        return Response({'error': f"TypeError: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f"Error during chatbot response: {e}")
        return Response({'error': 'Error processing message.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)