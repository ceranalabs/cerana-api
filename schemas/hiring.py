from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from enum import Enum

# Enums for validation
class WorkAuthStatus(str, Enum):
    citizen = "citizen"
    permanent_resident = "permanent_resident"
    visa_holder = "visa_holder"
    needs_sponsorship = "needs_sponsorship"

class Availability(str, Enum):
    actively_looking = "actively_looking"
    open_to_opportunities = "open_to_opportunities"
    not_looking = "not_looking"

class EmploymentStatus(str, Enum):
    employed = "employed"
    unemployed = "unemployed"
    freelancing = "freelancing"
    student = "student"

class ExperienceLevel(str, Enum):
    entry = "entry"
    mid = "mid"
    senior = "senior"
    lead = "lead"
    principal = "principal"
    executive = "executive"

class EmploymentType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    internship = "internship"

class JobStatus(str, Enum):
    active = "active"
    paused = "paused"
    closed = "closed"

class EquityUnit(str, Enum):
    percentage = "percentage"
    basis_points = "basis_points"

# Base schemas
class SalaryRange(BaseModel):
    min: float = Field(..., ge=0)
    max: float = Field(..., ge=0)
    currency: str = Field(default="USD")

class EquityRange(BaseModel):
    min: float = Field(..., ge=0)
    max: float = Field(..., ge=0)
    unit: EquityUnit

class WorkExperience(BaseModel):
    id: Optional[str] = None
    title: str
    company: str
    role_description: str = Field(..., alias="roleDescription")
    start_date: date = Field(..., alias="startDate")
    end_date: Optional[date] = Field(None, alias="endDate")
    is_current: bool = Field(default=False, alias="isCurrent")
    skills: Optional[List[str]] = None

    class Config:
        populate_by_name = True

class Education(BaseModel):
    id: Optional[str] = None
    degree: str
    institution: str
    field_of_study: str = Field(..., alias="fieldOfStudy")
    graduation_year: Optional[int] = Field(None, alias="graduationYear")
    gpa: Optional[float] = None

    class Config:
        populate_by_name = True

class CandidateProfile(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    location: str
    work_auth_status: WorkAuthStatus = Field(..., alias="workAuthStatus")
    availability: Availability
    employment_status: EmploymentStatus = Field(..., alias="employmentStatus")
    salary_expectations: Optional[SalaryRange] = Field(None, alias="salaryExpectations")
    skills: List[str]
    experience_level: ExperienceLevel = Field(..., alias="experienceLevel")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    class Config:
        populate_by_name = True

class DetailedCandidateProfile(CandidateProfile):
    work_experience: List[WorkExperience] = Field(..., alias="workExperience")
    bio: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = Field(None, alias="linkedinUrl")
    portfolio_url: Optional[HttpUrl] = Field(None, alias="portfolioUrl")
    education: List[Education]
    certifications: Optional[List[str]] = None

# Job schemas
class JobPostingInput(BaseModel):
    title: str = Field(..., max_length=200)
    job_description: str = Field(..., max_length=5000, alias="jobDescription")
    required_skills: List[str] = Field(..., min_items=1, max_items=20, alias="requiredSkills")
    preferred_skills: Optional[List[str]] = Field(None, max_items=20, alias="preferredSkills")
    experience_level: ExperienceLevel = Field(..., alias="experienceLevel")
    location: str
    is_remote: bool = Field(default=False, alias="isRemote")
    salary_range: SalaryRange = Field(..., alias="salaryRange")
    equity: Optional[EquityRange] = None
    employment_type: EmploymentType = Field(..., alias="employmentType")
    department: str
    team: Optional[str] = None

    class Config:
        populate_by_name = True

class JobPosting(JobPostingInput):
    id: str
    founder_id: str = Field(..., alias="founderId")
    status: JobStatus = JobStatus.active
    posted_at: datetime = Field(..., alias="postedAt")
    updated_at: datetime = Field(..., alias="updatedAt")

# Search schemas
class JobRequirements(BaseModel):
    title: Optional[str] = None
    job_description: Optional[str] = Field(None, alias="jobDescription")
    required_skills: List[str] = Field(..., alias="requiredSkills")
    preferred_skills: Optional[List[str]] = Field(None, alias="preferredSkills")
    experience_level: ExperienceLevel = Field(..., alias="experienceLevel")
    location: Optional[str] = None
    is_remote: bool = Field(default=False, alias="isRemote")

    class Config:
        populate_by_name = True

class SearchFilters(BaseModel):
    availability: Optional[List[Availability]] = None
    work_auth_status: Optional[List[WorkAuthStatus]] = Field(None, alias="workAuthStatus")
    salary_range: Optional[SalaryRange] = Field(None, alias="salaryRange")
    location: Optional[str] = None
    max_distance: Optional[float] = Field(None, alias="maxDistance")

    class Config:
        populate_by_name = True

class MatchingCriteria(BaseModel):
    skill_match_threshold: float = Field(default=70, ge=0, le=100, alias="skillMatchThreshold")
    min_match_score: float = Field(default=60, ge=0, le=100, alias="minMatchScore")
    use_ai_ranking: bool = Field(default=True, alias="useAIRanking")

    class Config:
        populate_by_name = True

class SearchPagination(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)

class SearchSort(BaseModel):
    field: str = Field(default="match_score", pattern="^(match_score|experience|name|availability)$")
    order: str = Field(default="desc", pattern="^(asc|desc)$")

class CandidateSearchRequest(BaseModel):
    job_requirements: JobRequirements = Field(..., alias="jobRequirements")
    filters: Optional[SearchFilters] = None
    matching: Optional[MatchingCriteria] = None
    pagination: Optional[SearchPagination] = None
    sort: Optional[SearchSort] = None

    class Config:
        populate_by_name = True

# Match scoring schemas
class SkillsMatch(BaseModel):
    score: float = Field(..., ge=0, le=100)
    matched_skills: List[str] = Field(..., alias="matchedSkills")
    missing_skills: List[str] = Field(..., alias="missingSkills")
    matched_count: int = Field(..., alias="matchedCount")
    total_required: int = Field(..., alias="totalRequired")

    class Config:
        populate_by_name = True

class ExperienceMatch(BaseModel):
    score: float = Field(..., ge=0, le=100)
    reasoning: str

class LocationMatch(BaseModel):
    score: float = Field(..., ge=0, le=100)
    distance: Optional[float] = None

class AvailabilityMatch(BaseModel):
    score: float = Field(..., ge=0, le=100)
    status: str

class AIRanking(BaseModel):
    score: float = Field(..., ge=0, le=100)
    reasoning: str

class MatchBreakdown(BaseModel):
    skills_match: SkillsMatch = Field(..., alias="skillsMatch")
    experience_match: ExperienceMatch = Field(..., alias="experienceMatch")
    location_match: LocationMatch = Field(..., alias="locationMatch")
    availability_match: AvailabilityMatch = Field(..., alias="availabilityMatch")
    ai_ranking: Optional[AIRanking] = Field(None, alias="aiRanking")

    class Config:
        populate_by_name = True

class MatchedCandidate(CandidateProfile):
    match_score: float = Field(..., ge=0, le=100, alias="matchScore")
    match_breakdown: MatchBreakdown = Field(..., alias="matchBreakdown")
    recent_experience: Optional[List[WorkExperience]] = Field(None, max_items=3, alias="recentExperience")

# Response schemas
class Pagination(BaseModel):
    page: int = Field(..., ge=1)
    limit: int = Field(..., ge=1)
    total: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=0, alias="totalPages")
    has_next: bool = Field(..., alias="hasNext")
    has_prev: bool = Field(..., alias="hasPrev")

    class Config:
        populate_by_name = True

class SearchMetadata(BaseModel):
    total_matches: int = Field(..., alias="totalMatches")
    search_time: float = Field(..., alias="searchTime")
    applied_filters: Dict[str, Any] = Field(..., alias="appliedFilters")
    matching_criteria: Dict[str, Any] = Field(..., alias="matchingCriteria")

    class Config:
        populate_by_name = True

class CandidateSearchResponse(BaseModel):
    candidates: List[MatchedCandidate]
    pagination: Pagination
    search_metadata: SearchMetadata = Field(..., alias="searchMetadata")

    class Config:
        populate_by_name = True

# Saved search schemas
class SavedSearchInput(BaseModel):
    name: str = Field(..., max_length=100)
    search_criteria: CandidateSearchRequest = Field(..., alias="searchCriteria")

    class Config:
        populate_by_name = True

class SavedSearch(BaseModel):
    id: str
    founder_id: str = Field(..., alias="founderId")
    name: str
    search_criteria: CandidateSearchRequest = Field(..., alias="searchCriteria")
    created_at: datetime = Field(..., alias="createdAt")
    last_used: Optional[datetime] = Field(None, alias="lastUsed")

    class Config:
        populate_by_name = True

# List response schemas
class CandidateListResponse(BaseModel):
    candidates: List[CandidateProfile]
    pagination: Pagination

class JobListResponse(BaseModel):
    jobs: List[JobPosting]
    pagination: Pagination