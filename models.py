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
