# api/crewai/crew_setup.py
from api.crewai.agents import TutorAgents
from api.crewai.tasks import TeachingTasks
from crewai import Crew

import os
from textwrap import dedent
from dotenv import load_dotenv
from crewai import Crew
from .agents import TutorAgents
from .tasks import TeachingTasks
from .tools.pdf_processing_tool import PDFManagementTool
from django.conf import settings
from api.models import User, Lesson, TaskResult, QuizResult

import threading

load_dotenv()

# Create output_files directory if it doesn't exist
if not os.path.exists('output_files'):
    os.makedirs('output_files')

class TutorCrew:
    def __init__(self, user_id, lesson_id, quiz_results=None):
        self.user = User.objects.get(id=user_id)
        self.lesson = Lesson.objects.get(id=lesson_id)
        
        self.student_name = self.user.username
        self.student_class = self.user.learning_class
        self.student_level = self.user.learning_level
        self.student_learning_preferences = self.user.lesson_types
        self.feedback = None
        self.existing_state = None
        self.quiz_results = quiz_results

        # Fetch lesson text or process PDF
        if self.lesson.lesson_text:
            self.lesson_content = self.lesson.lesson_text
        elif self.lesson.lesson_pdf:
            self.lesson_content = PDFManagementTool.process_pdf(self.lesson.lesson_pdf.path)

        # Instantiate your custom agents and tasks
        self.agents = TutorAgents()
        self.tasks = TeachingTasks()

        # Create instances of your agents
        self.agent_dict = {
            "learning_path_tutor": self.agents.learning_path_tutor(),
            "practical_tutor": self.agents.practical_tutor(),
            "profiler": self.agents.profiler(),
            "digital_teacher": self.agents.digital_teacher(),
            "communication_chatbot": self.agents.communication_chatbot()
        }

    def run_all_tasks(self):
        self.task_results = {}
        self.tasks_list = {
            "learning_path_tutor": self.tasks.adapt_learning_path(
                self.agent_dict["learning_path_tutor"],
                self.student_name,
                self.lesson_content,
                self.student_class,
                self.student_level,
                self.student_learning_preferences,
                self.feedback,
            ),
            "practical_tutor": self.tasks.apply_practical_knowledge(
                self.agent_dict["practical_tutor"],
                self.student_name,
                self.lesson_content,
                self.student_class,
                self.student_level,
                self.student_learning_preferences,
                self.feedback,
                self.quiz_results  # Pass quiz results to the task
            ),
            "profiler": self.tasks.profile_student(
                self.agent_dict["profiler"],
                self.student_name,
                self.lesson_content,
                self.student_class,
                self.student_level,
                self.student_learning_preferences,
                self.feedback,
            ),
            "digital_teacher": self.tasks.generate_report(
                self.agent_dict["digital_teacher"],
                self.student_name,
                self.student_class,
                self.student_level,
                self.student_learning_preferences,
                self.feedback,
                self.existing_state,
            ),
            "communication_chatbot": self.tasks.communicate_with_student(
                self.agent_dict["communication_chatbot"],
                self.student_name,
                self.lesson_content,
                self.student_class,
                self.student_level,
                self.student_learning_preferences,
                self.feedback,
            )
        }

        # Run tasks asynchronously
        thread = threading.Thread(target=self.execute_tasks)
        thread.start()

        # Return the path of the generated PDF file
        pdf_path = os.path.join('/output_files', 'compiled_materials.pdf')
        return pdf_path

    def execute_tasks(self):
        # Define the crew with all agents and tasks
        crew = Crew(
            agents=list(self.agent_dict.values()),
            tasks=list(self.tasks_list.values()),
            verbose=True,
        )

        # Execute the crew's tasks and store the results
        crew_results = crew.kickoff()

        # Store results in the database
        for task, result in zip(self.tasks_list.keys(), crew_results):
            task_result = TaskResult.objects.create(
                lesson=self.lesson,
                task_type=task,
                result=result
            )
            self.task_results[task] = task_result

    def execute_agent_task(self, agent_key, task_type, feedback):
        selected_agent_instance = self.agent_dict[agent_key]
        selected_task = None

        if agent_key == "practical_tutor":
            if task_type == "create_exercise":
                selected_task = self.tasks.apply_practical_knowledge(
                    selected_agent_instance,
                    self.student_name,
                    self.lesson_content,
                    self.student_class,
                    self.student_level,
                    self.student_learning_preferences,
                    feedback,
                    self.quiz_results
                )
            elif task_type == "correct_exercise":
                selected_task = self.tasks.correct_exercise(
                    selected_agent_instance,
                    self.student_name,
                    self.lesson_content,
                    self.student_class,
                    self.student_level,
                    self.student_learning_preferences,
                    feedback,
                    self.quiz_results  # Pass quiz results to the task
                )
        else:
            if agent_key == "learning_path_tutor":
                selected_task = self.tasks.adapt_learning_path(
                    selected_agent_instance,
                    self.student_name,
                    self.lesson_content,
                    self.student_class,
                    self.student_level,
                    self.student_learning_preferences,
                    feedback,
                )
            elif agent_key == "profiler":
                selected_task = self.tasks.profile_student(
                    selected_agent_instance,
                    self.student_name,
                    self.lesson_content,
                    self.student_class,
                    self.student_level,
                    self.student_learning_preferences,
                    feedback,
                )
            elif agent_key == "communication_chatbot":
                selected_task = self.tasks.communicate_with_student(
                    selected_agent_instance,
                    self.student_name,
                    self.lesson_content,
                    self.student_class,
                    self.student_level,
                    self.student_learning_preferences,
                    feedback,
                )

        # Execute the updated task
        crew = Crew(
            agents=[selected_agent_instance],
            tasks=[selected_task],
            verbose=False,
        )
        updated_result = crew.kickoff()

        # Ensure task_type is set correctly
        if task_type is None:
            task_type = agent_key  # Default to agent_key if task_type is None

        # Store the updated result in the database
        task_result = TaskResult.objects.create(
            lesson=self.lesson,
            task_type=task_type,
            result=updated_result
        )

        # Return the updated result
        return updated_result if updated_result else "No output from task."