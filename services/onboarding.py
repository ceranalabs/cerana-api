import uuid
from datetime import datetime

def create_or_update_investor(data, investors, user_id=None):
    # For MVP, use user_id as key if provided, else generate
    investor_id = user_id or str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    investor = investors.get(investor_id, {})
    investor.update(data)
    investor['id'] = investor_id
    investor['createdAt'] = investor.get('createdAt', now)
    investor['updatedAt'] = now
    investors[investor_id] = investor
    return investor

def get_investor(investor_id, investors):
    return investors.get(investor_id)
