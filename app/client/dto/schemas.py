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
