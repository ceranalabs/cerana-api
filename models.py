from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    founder_profile = db.relationship('FounderProfile', backref='user', uselist=False)
    investor_profile = db.relationship('InvestorProfile', backref='user', uselist=False)

class FounderProfile(db.Model):
    __tablename__ = 'founder_profiles'
    id = db.Column(db.String(36), db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    background = db.Column(db.String(64), nullable=False)
    experience_level = db.Column(db.String(32), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    focus_areas = db.Column(db.ARRAY(db.String(128)), nullable=False)
    linkedin_url = db.Column(db.String(255), nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    funding_stage = db.Column(db.String(64), nullable=True)
    title = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InvestorProfile(db.Model):
    __tablename__ = 'investor_profiles'
    id = db.Column(db.String(36), db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    firm_name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    # InvestmentThesis fields
    stage_focus = db.Column(db.ARRAY(db.String(64)), nullable=False)
    sector_preferences = db.Column(db.ARRAY(db.String(64)), nullable=False)
    geographic_focus = db.Column(db.String(255), nullable=False)
    check_size_range = db.Column(db.String(64), nullable=False)
    investment_style = db.Column(db.String(64), nullable=False)
    deal_flow_preference = db.Column(db.String(255))
    due_diligence_style = db.Column(db.String(255))
    value_add_areas = db.Column(db.ARRAY(db.String(128)))
    investments_per_year = db.Column(db.Integer)
    linkedin_url = db.Column(db.String(255), nullable=True)
    accredited = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    founder_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    founder_name = db.Column(db.String(255), nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    meeting_type = db.Column(db.String(64), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True, default=30)
    status = db.Column(db.String(32), nullable=False, default='requested')
    agenda = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    meeting_url = db.Column(db.String(255), nullable=True)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='meetings', foreign_keys=[founder_id])

class PipelineDeal(db.Model):
    __tablename__ = 'pipeline_deals'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    founder_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    founder_name = db.Column(db.String(255), nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    stage = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(32), nullable=False, default='active')
    next_action = db.Column(db.String(255), nullable=True)
    next_action_due = db.Column(db.DateTime, nullable=True)
    match_score = db.Column(db.Integer, nullable=True)
    key_metrics = db.Column(db.JSON, nullable=True)
    risk_flags = db.Column(db.ARRAY(db.String(255)), nullable=True)
    opportunities = db.Column(db.ARRAY(db.String(255)), nullable=True)
    notes = db.Column(db.ARRAY(db.Text), nullable=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    investor = db.relationship('User', backref='pipeline_deals_as_investor', foreign_keys=[investor_id])
    founder = db.relationship('User', backref='pipeline_deals_as_founder', foreign_keys=[founder_id])

# Hiring Platform Models
class CandidateProfile(db.Model):
    __tablename__ = 'candidate_profiles'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(255), nullable=False)
    work_auth_status = db.Column(db.String(32), nullable=False)  # citizen, permanent_resident, visa_holder, needs_sponsorship
    availability = db.Column(db.String(32), nullable=False)  # actively_looking, open_to_opportunities, not_looking
    employment_status = db.Column(db.String(32), nullable=False)  # employed, unemployed, freelancing, student
    salary_expectations = db.Column(db.JSON, nullable=True)  # {min, max, currency}
    skills = db.Column(db.ARRAY(db.String(128)), nullable=False)
    experience_level = db.Column(db.String(32), nullable=False)  # entry, mid, senior, lead, principal, executive
    bio = db.Column(db.Text, nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    portfolio_url = db.Column(db.String(255), nullable=True)
    certifications = db.Column(db.ARRAY(db.String(255)), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    work_experience = db.relationship('WorkExperience', backref='candidate', lazy='dynamic', cascade='all, delete-orphan')
    education = db.relationship('Education', backref='candidate', lazy='dynamic', cascade='all, delete-orphan')

class WorkExperience(db.Model):
    __tablename__ = 'work_experience'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id = db.Column(db.String(36), db.ForeignKey('candidate_profiles.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    role_description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_current = db.Column(db.Boolean, default=False)
    skills = db.Column(db.ARRAY(db.String(128)), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id = db.Column(db.String(36), db.ForeignKey('candidate_profiles.id'), nullable=False)
    degree = db.Column(db.String(255), nullable=False)
    institution = db.Column(db.String(255), nullable=False)
    field_of_study = db.Column(db.String(255), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=True)
    gpa = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    founder_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.ARRAY(db.String(128)), nullable=False)
    preferred_skills = db.Column(db.ARRAY(db.String(128)), nullable=True)
    experience_level = db.Column(db.String(32), nullable=False)  # entry, mid, senior, lead, principal, executive
    location = db.Column(db.String(255), nullable=False)
    is_remote = db.Column(db.Boolean, default=False)
    salary_range = db.Column(db.JSON, nullable=False)  # {min, max, currency}
    equity = db.Column(db.JSON, nullable=True)  # {min, max, unit}
    employment_type = db.Column(db.String(32), nullable=False)  # full_time, part_time, contract, internship
    department = db.Column(db.String(255), nullable=False)
    team = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(32), nullable=False, default='active')  # active, paused, closed
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    founder = db.relationship('User', backref='job_postings', foreign_keys=[founder_id])

class SavedSearch(db.Model):
    __tablename__ = 'saved_searches'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    founder_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    search_criteria = db.Column(db.JSON, nullable=False)  # Complete search request as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, nullable=True)

    # Relationships
    founder = db.relationship('User', backref='saved_searches', foreign_keys=[founder_id])
