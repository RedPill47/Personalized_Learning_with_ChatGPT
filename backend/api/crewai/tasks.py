from crewai import Task
from textwrap import dedent

class TeachingTasks:
    def __init__(self):
        self.tip_section = "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def adapt_learning_path(self, agent, student_name, lesson, student_class, student_level, student_learning_preferences, feedback):
        return Task(
            description=dedent(f"""
                **Task**: Fully Develop and Customize Learning Materials
                **Description**: Create a comprehensive and engaging course based on the provided lesson and tailor it 
                               according to the student's learning preferences. 
                               Then, develop detailed educational flashcards that supplement the course materials. 
                               Both the course and flashcards should be fully developed and ready for use by the student.
                **Expected Output**:
                    - A detailed course in LaTex format. This should include sections, key points, and interactive elements tailored to enhance learning.
                    - A complete set of flashcards in a JSON file with 'front' and 'back', where each flashcard includes a term and a definition related to the course content.
                    - A compiled PDF of the LaTeX document.
                **Actions**:
                    - Develop the course material to be complete and ready-to-deliver — not just an outline but filled with detailed, educational content.
                    - Create flashcards that are directly usable for study and revision, emphasizing the key concepts of the lesson.
                    - Create the files "compiled_materials.tex" and "flashcards.json"
                    - Compile the LaTeX document into a PDF format for easy distribution and use.
                **Feedback Mechanism**:
                    - Provide the profiler with a sample of the course and flashcards to receive initial feedback on their alignment with learning preferences.
                **Parameters**:
                    - Student Name: {student_name}
                    - Lesson: {lesson}
                    - Student Class: {student_class}
                    - Student Level: {student_level}
                    - Student Learning Preferences: {student_learning_preferences}
                    - Student Feedback: {feedback}
                **Note**: Please do NOT put in the file "LaTeX content as shown above" or "content from above" or "LaTeX content from above", JUST DO IT.
                This task involves both the creation of the course, the development of supplementary materials and compiling the LaTeX file into a PDF file with 'front' and 'back'. 
                Ensure all components are finalized and ready for student use.
                {self.tip_section}
            """),
            expected_output="A detailed and complete course in PDF format containing the course and a complete set of flashcards in a JSON file.",
            agent=agent,
            actions=[
                lambda inputs: agent.tools[-1](inputs['compiled_materials'], 'compiled_materials.tex'),
                lambda inputs: agent.tools[-1](inputs['flashcards_content'], 'flashcards.json')
            ]
        )

    def apply_practical_knowledge(self, agent, student_name, lesson, student_class, student_level, student_learning_preferences, feedback, quiz_results):
        return Task(
            description=dedent(f"""
                **Task**: Develop Quiz
                **Description**: Create an engaging quiz that test and reinforce the theoretical knowledge covered in the lesson, 
                               tailored to the student's learning preferences.
                **Expected Output**:
                    - A list of quiz questions in JSON format, each containing a question string, an array of options, and the index of the correct option ('question', 'options', 'correct').
                **Actions**:
                    - Develop a variety of questions that challenge the student's understanding of the lesson.
                    - Create the file "quiz.json" containing the quiz questions in JSON format.
                **Feedback Mechanism**:
                    - Initial feedback from students to be collected and analyzed for improvement suggestions.
                **Parameters**:
                    - Student Name: {student_name}
                    - Lesson: {lesson}
                    - Student Class: {student_class}
                    - Student Level: {student_level}
                    - Student Learning Preferences: {student_learning_preferences}
                    - Student Feedback: {feedback}
                    - Quiz Results: {quiz_results} 
                **Note**: {self.tip_section}
            """),
            expected_output="A list of quiz questions in JSON format, each containing a question string, an array of options, and the index of the correct option.",
            agent=agent,
            actions=[
                lambda inputs: agent.tools[-1](inputs['quiz_content'], 'quiz.json')
            ]
        )

    def correct_exercise(self, agent, student_name, lesson, student_class, student_level, student_learning_preferences, feedback, quiz_results):
        return Task(
            description=dedent(f"""
                **Task**: Correct the Provided Exercises
                **Description**: Collect and review the quiz answers provided. 
                                Provide detailed feedback on each question and suggest improvements.
                **Expected Output**:
                    - Detailed feedback on each question, explaining the correct answer and any misconceptions.
                **Actions**:
                    - Collect the quiz answers provided by the student.
                    - Provide detailed feedback on each question, explaining the correct answer and any misconceptions.
                **Feedback Mechanism**:
                    - Feedback from the student on the corrections provided.
                **Parameters**:
                    - Student Name: {student_name}
                    - Lesson: {lesson}
                    - Student Class: {student_class}
                    - Student Level: {student_level}
                    - Student Learning Preferences: {student_learning_preferences}
                    - Provided Exercises: {feedback}  # Using feedback to pass the exercises for correction
                    - Quiz Results: {quiz_results}  # Using quiz_result to pass the quiz answers for correction
                **Note**: DO NOT STORE IN A FILE. Provide the feedback directly in the response.
                {self.tip_section}
            """),
            expected_output="Detailed feedback on each question, explaining the correct answer and any misconceptions.",
            agent=agent,
        )

    def profile_student(self, agent, student_name, lesson, student_class, student_level, student_learning_preferences, feedback):
        return Task(
            description=dedent(f"""
                **Task**: Analyze Student Learning Preferences
                **Description**: Collect and analyze data on the student's learning preferences to better tailor future educational content.
                **Expected Output**:
                    - Comprehensive report on student learning preferences.
                **Actions**:
                    - Analyze the student's feedback and performance to identify patterns in learning preferences.
                    - Create a detailed report outlining the student's strengths, weaknesses, and preferred learning methods in a file 'profile.txt'.
                **Feedback Mechanism**:
                    - Feedback from other agents on the accuracy and usability of the analysis.
                **Parameters**:
                    - Student Name: {student_name}
                    - Lesson: {lesson}
                    - Student Class: {student_class}
                    - Student Level: {student_level}
                    - Student Learning Preferences: {student_learning_preferences}
                    - Student Feedback: {feedback}
                **Note**: {self.tip_section}
            """),
            expected_output="Comprehensive report in a txt file ('profile.txt') on student learning preferences.",
            agent=agent,
            actions=[
                lambda inputs: agent.tools[-1](inputs['profile_content'], 'profile.txt')
            ]
        )
    
    def generate_report(self, agent, student_name, student_class, student_level, student_learning_preferences, feedback, existing_state):
        return Task(
            description=dedent(f"""
                **Task**: Generate Comprehensive Report
                **Description**: Verify and coordinate all agents, ensuring they complete their tasks as expected, and compile their outputs into a comprehensive report.
                **Expected Output**:
                    - A comprehensive report in a txt file ('report.txt') summarizing the outputs and feedback from all agents.
                **Actions**:
                    - Verify the outputs from all agents.
                    - Compile the outputs into a report.
                    - Store the report in a file named "report.txt".
                **Parameters**:
                    - Student Name: {student_name}
                    - Student Class: {student_class}
                    - Student Level: {student_level}
                    - Student Learning Preferences: {student_learning_preferences}
                    - Feedback: {feedback}
                    - Existing State: {existing_state}
                **Note**: {self.tip_section}
            """),
            expected_output="A comprehensive report in a txt file ('report.txt') summarizing the outputs and feedback from all agents.",
            agent=agent,
            actions=[
                lambda inputs: agent.tools[-1](inputs['report_content'], 'report.txt')
            ]
        )

    def communicate_with_student(self, agent, student_name, lesson, student_class, student_level ,student_learning_preferences, feedback):
        return Task(
            description=dedent(f"""
                **Task**: Facilitate Feedback and Communication
                **Description**: Tutor AI, the chatbot that engage with the student to collect feedback on the learning materials and overall learning experience, addressing any concerns promptly.
                **Expected Output**:
                    - Immediate Response to Student Query.
                **Feedback Mechanism**:
                    - Immediate response to student queries based on feedback.
                **Parameters**:
                    - Student Name: {student_name}
                    - Lesson: {lesson}
                    - Student Class: {student_class}
                    - Student Level: {student_level}
                    - Student Learning Preferences: {student_learning_preferences}
                    - Student Feedback: {feedback}
                **Note**: {self.tip_section}
            """),
            expected_output="Immediate Response to Student Query.",
            agent=agent,
        )