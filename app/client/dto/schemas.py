from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class SoftSkillData(BaseModel):
    description: str
    id: int
    name: str


class TechSkillData(BaseModel):
    id: int
    name: str


# Datos asociados a un candidato para una posición
class PositionCandidate(BaseModel):
    candidate_id: int
    technical_score: Optional[int]
    softskill_score: Optional[int]
    general_score: Optional[int]


# Datos de candidato consultado
class CandidateData(BaseModel):
    user_id: int
    fullname: str
    soft_skills: List[SoftSkillData]
    tech_skills: List[TechSkillData]


# Respuesta servicio consulta de detalle de candidatos
class CandidatesResponse(BaseModel):
    data: List[CandidateData]
    total_pages: int


# Elemento base respuesta orquestación candidatos para posición
class PositionCandidateDetail(BaseModel):
    user_id: int
    fullname: str
    soft_skills: List[SoftSkillData]
    tech_skills: List[TechSkillData]

# Item base de entrevista
class InterviewBase(BaseModel):
    customer_id: int
    candidate_id: int
    subject: str
    realization_date: datetime
    score: Optional[int]
    open_position_id: Optional[int]


# Item con datos de entrevista respuesta
class InterviewResponseData(InterviewBase):
    id: int


# Respuesta servicio consulta de entrevistas
class InterviewsResponse(BaseModel):
    data: List[InterviewResponseData]
    total_pages: int

# Elemento base respuesta orquestación entrevistas
class InterviewData(BaseModel):
    subject: str
    client_name: str
    realization_date: datetime
    score: Optional[int]

# Elemento base cliente
class CustomerBase(BaseModel):
    user_id: int
    name: str

# Respuesta servicio consulta de detalle empresas cliente
class CustomersResponse(BaseModel):
    data: List[CustomerBase]
    total_pages: int


# Respuesta orquestación entrevistas
class InterviewsDetailsResponse(BaseModel):
    data: List[InterviewData]
    total_pages: int