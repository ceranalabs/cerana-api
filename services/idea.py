import uuid
from datetime import datetime

ideas = {}

def submit_idea(founder_id, data):
    idea_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    idea = dict(data)
    idea['id'] = idea_id
    idea['founderId'] = founder_id
    idea['completenessScore'] = 80  # MVP: static
    idea['createdAt'] = now
    idea['updatedAt'] = now
    ideas[idea_id] = idea
    return idea

def get_idea(idea_id):
    return ideas.get(idea_id)

def update_idea(idea_id, data):
    idea = ideas.get(idea_id)
    if not idea:
        return None
    idea.update(data)
    idea['updatedAt'] = datetime.utcnow().isoformat()
    return idea
