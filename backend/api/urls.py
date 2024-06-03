from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from django.urls import path
from .views import UserUpdateView


urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('test/', views.testEndPoint, name='test'),
    path('', views.getRoutes),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),

    # Get profile
    path("profile/<int:pk>/", views.ProfileDetail.as_view()),

    # Crew AI
    path('submit-lesson/', views.SubmitLessonView.as_view(), name='submit_lesson'),
    path('get-task-results/<int:lesson_id>/', views.GetTaskResultsView.as_view(), name='get_task_results'),
    path('provide-feedback/<int:lesson_id>/', views.ProvideFeedbackView.as_view(), name='provide_feedback'),

    # Quiz and Flashcards Data
    path('quiz-data/', views.get_quiz_data, name='quiz-data'),
    path('submit-quiz-result/', views.SubmitQuizResultView.as_view(), name='submit-quiz-result'),
    path('fetch-quiz-results/', views.FetchQuizResultsView.as_view(), name='fetch-quiz-results'),
    path('flashcards-data/', views.get_flashcards_data, name='flashcards-data'),

    # Chatbot
    path('chatbot-response/', views.chatbot_response, name='chatbot-response'),
]