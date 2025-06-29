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

# In-memory data stores
investors = {}
founders = {}
pipeline = {}

# Sample investor
investor_id = str(uuid.uuid4())
investors[investor_id] = {
    'id': investor_id,
    'name': 'Jane Doe',
    'email': 'jane@vcfirm.com',
    'firmName': 'VC Firm',
    'title': 'Partner',
    'investmentThesis': {
        'stageFocus': ['seed', 'series-a'],
        'sectorPreferences': ['AI/ML', 'SaaS'],
        'geographicFocus': 'national',
        'checkSizeRange': '100k-500k',
        'investmentStyle': 'lead',
        'dealFlowPreference': 'curated',
        'dueDiligenceStyle': 'hands-on',
        'valueAddAreas': ['go-to-market', 'fundraising'],
        'investmentsPerYear': 5
    },
    'linkedinUrl': 'https://linkedin.com/in/janedoe',
    'accredited': True,
    'createdAt': datetime.utcnow().isoformat(),
    'updatedAt': datetime.utcnow().isoformat()
}

# Sample founder
founder_id = str(uuid.uuid4())
founders[founder_id] = {
    'id': founder_id,
    'name': 'Sarah Chen',
    'title': 'CEO',
    'companyName': 'TechFlow AI',
    'matchScore': 94,
    'problemStatement': 'AI-powered invoice processing',
    'fundingStage': 'series-a',
    'raisingAmount': '$2M',
    'location': 'San Francisco',
    'traction': {
        'revenue': '$50K MRR',
        'growth': '15% monthly',
        'customers': '45 SMB clients',
        'retention': '95%',
        'partnerships': '3 major integrators'
    },
    'whyThisFits': [
        'B2B SaaS in your sweet spot',
        'Strong product-market fit signals',
        'Technical founder with domain expertise'
    ],
    'riskFlags': ['Competitive pressure'],
    'opportunities': ['Strong unit economics'],
    'avatarUrl': None,
    'lastUpdated': datetime.utcnow().isoformat()
}

# Sample pipeline deal
pipeline_id = str(uuid.uuid4())
pipeline[pipeline_id] = {
    'id': pipeline_id,
    'founderId': founder_id,
    'founderName': 'Sarah Chen',
    'companyName': 'TechFlow AI',
    'stage': 'due-diligence',
    'status': 'active',
    'daysInStage': 12,
    'nextAction': 'Reference calls',
    'nextActionDue': datetime.utcnow().isoformat(),
    'matchScore': 94,
    'keyMetrics': founders[founder_id]['traction'],
    'riskFlags': ['Competitive pressure'],
    'opportunities': ['Strong unit economics'],
    'notes': [],
    'addedAt': datetime.utcnow().isoformat(),
    'updatedAt': datetime.utcnow().isoformat()
}
