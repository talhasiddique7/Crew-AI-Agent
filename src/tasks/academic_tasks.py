"""
Academic Tasks

This module contains tasks related to academic question answering.
"""

from .base_task import BaseTask
import logging

logger = logging.getLogger(__name__)

class AcademicQuestionTask(BaseTask):
    """
    Task for answering academic questions comprehensively.
    """
    
    def get_description(self) -> str:
        """Get the task description."""
        return (
            "Answer the following academic question comprehensively and educationally:\n\n"
            "Question: {question}\n"
            "Subject Area: {subject_area}\n\n"
            "Your response should include:\n"
            "1. A clear and direct answer to the question\n"
            "2. Detailed explanation of key concepts involved\n"
            "3. Relevant examples or applications\n"
            "4. Historical context or background (if applicable)\n"
            "5. Additional related information that enhances understanding\n"
            "6. Suggestions for further learning or research\n\n"
            "Ensure your answer is educational, accurate, and promotes deeper understanding."
        )
    
    def get_expected_output(self) -> str:
        """Get the expected output description."""
        return (
            "A comprehensive academic response with:\n"
            "- Direct answer to the question\n"
            "- Clear explanation of concepts\n"
            "- Practical examples or applications\n"
            "- Contextual information\n"
            "- Further learning suggestions\n"
            "The response should be well-structured, academically rigorous, "
            "and accessible to the target audience level."
        )
