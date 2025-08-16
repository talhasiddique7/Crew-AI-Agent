"""
Simple Academic Service without CrewAI dependencies
"""
import os
from groq import Groq
from ..config import Config

class AcademicService:
    def __init__(self):
        """Initialize the service with Groq client."""
        self.config = Config()
        self.client = Groq(api_key=self.config.GROQ_API_KEY)
        
    async def process_question(self, question: str, subject: str = "General") -> str:
        """
        Process academic question using Groq API directly.
        
        Args:
            question: The academic question to answer
            subject: The subject area (optional)
            
        Returns:
            The AI response as a string
        """
        try:
            # Create a comprehensive prompt for academic assistance
            system_prompt = f"""You are an expert academic assistant specializing in {subject}. 
            Provide comprehensive, educational, and well-structured answers to academic questions.
            
            Guidelines:
            - Give detailed explanations with clear reasoning
            - Include relevant examples when helpful
            - Break down complex concepts into understandable parts
            - Use proper academic tone and terminology
            - Cite concepts or principles when relevant
            - If the question is unclear, ask for clarification
            
            Subject Focus: {subject}"""
            
            # Make API call to Groq
            response = self.client.chat.completions.create(
                model=self.config.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=2000,
                top_p=0.9
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error processing question: {str(e)}")
