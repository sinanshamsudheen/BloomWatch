"""
AI Agents Package for BloomWatch
Implements agentic architecture using CrewAI
"""
from .orchestrator import get_orchestrator, BloomExplanationOrchestrator
from .explanation_agent import generate_explanation
from .web_search_agent import perform_web_search

__all__ = [
    'get_orchestrator',
    'BloomExplanationOrchestrator',
    'generate_explanation',
    'perform_web_search'
]
