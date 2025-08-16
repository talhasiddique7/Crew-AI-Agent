"""
Academic Agent for specialized academic assistance
"""

import logging
from typing import Dict, Any
from crewai import Agent
from langchain_groq import ChatGroq
from ..config import config

logger = logging.getLogger(__name__)

class AcademicAgent:
    """Specialized agent for academic questions and research assistance"""
    
    def __init__(self):
        """Initialize the Academic Agent"""
        self.llm = ChatGroq(
            groq_api_key=config.GROQ_API_KEY,
            model_name=config.GROQ_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS
        )
        self.agent = self._create_agent()
        logger.info("Academic Agent initialized")
    
    def _create_agent(self) -> Agent:
        """Create the CrewAI agent"""
        return Agent(
            role="Academic Research Assistant",
            goal=(
                "Provide comprehensive, accurate, and educational answers to "
                "academic questions across multiple disciplines. Help students "
                "and researchers understand complex concepts with clear explanations, "
                "examples, and structured responses."
            ),
            backstory=(
                "You are a distinguished academic researcher and educator with "
                "expertise spanning multiple disciplines including science, "
                "mathematics, literature, history, philosophy, and social sciences. "
                "You have years of experience in teaching and research, with a "
                "talent for breaking down complex concepts into understandable "
                "explanations. You always provide context, examples, and encourage "
                "critical thinking while maintaining academic rigor and accuracy."
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def answer_question(self, question: str, subject: str = "General") -> Dict[str, Any]:
        """
        Answer an academic question
        
        Args:
            question: The academic question to answer
            subject: Subject area (e.g., Mathematics, Physics, etc.)
            
        Returns:
            Dictionary containing the answer and metadata
        """
        try:
            # Create a detailed prompt for the academic question
            prompt = self._create_academic_prompt(question, subject)
            
            # Generate response using the LLM directly
            response = self.llm.generate(prompt)
            
            return {
                "success": True,
                "question": question,
                "subject": subject,
                "answer": response,
                "metadata": {
                    "agent": "Academic Research Assistant",
                    "confidence": "High"
                }
            }
            
        except Exception as e:
            logger.error(f"Error answering academic question: {e}")
            return {
                "success": False,
                "error": str(e),
                "question": question,
                "subject": subject
            }
    
    def _create_academic_prompt(self, question: str, subject: str) -> str:
        """Create a structured prompt for academic questions"""
        return f"""
As an Academic Research Assistant with expertise in {subject}, please provide a comprehensive answer to the following question:

**Question:** {question}
**Subject Area:** {subject}

Please structure your response as follows:

1. **Direct Answer:** Provide a clear, concise answer to the question.

2. **Detailed Explanation:** Break down the key concepts involved with clear explanations.

3. **Examples:** Provide relevant examples or applications to illustrate the concepts.

4. **Context:** Include any relevant historical context, background information, or theoretical frameworks.

5. **Further Learning:** Suggest additional topics, resources, or questions for deeper understanding.

Ensure your response is:
- Academically rigorous and accurate
- Well-structured and easy to follow
- Educational and engaging
- Appropriate for the subject level
- Free from bias and speculation

Please provide a thorough, educational response that promotes deeper understanding of the topic.
"""
