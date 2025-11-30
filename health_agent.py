from agents.base_agent import BaseAgent

class HealthcareAgent(BaseAgent):
    def __init__(self, api_key):
        super().__init__("HealthcareAgent", api_key)
