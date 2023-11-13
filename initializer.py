from fastapi import FastAPI

from app.client.repositories.candidate_repository import CandidateRepository
from app.client.repositories.customer_repository import CustomerRepository
from app.health.controllers import health_controller
from app.health.services.health_service import HealthService
from app.interview.controllers import interview_controller
from app.interview.services.interview_service import InterviewService
from app.position.controllers import position_controller
from app.position.services.position_service import PositionService


class Initializer:
    def __init__(self, app: FastAPI):
        self.app = app

    def setup(self):
        self.init_health_module()
        self.init_interview_module()
        self.init_position_module()

    def init_health_module(self):
        health_service = HealthService()
        health_controller.initialize(health_service)
        self.app.include_router(health_controller.router)

    def init_position_module(self):
        print("Initializing position module")
        candidate_repository = CandidateRepository()
        customer_repository = CustomerRepository()
        position_service = PositionService(candidate_repository, customer_repository)
        position_controller.initialize(position_service)
        self.app.include_router(position_controller.router)

    def init_interview_module(self):
        print("Initializing interview module")
        candidate_repository = CandidateRepository()
        customer_repository = CustomerRepository()
        interview_service = InterviewService(candidate_repository, customer_repository)
        interview_controller.initialize(interview_service)
        self.app.include_router(interview_controller.router)