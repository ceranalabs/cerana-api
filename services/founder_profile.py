from datetime import datetime

founder_profiles = {}

def create_or_update_founder_profile(user_id, data):
    now = datetime.utcnow().isoformat()
    profile = founder_profiles.get(user_id, {})
    profile.update(data)
    profile['id'] = user_id
    if 'email' in data:
        profile['email'] = data['email']
    profile['createdAt'] = profile.get('createdAt', now)
    profile['updatedAt'] = now
    founder_profiles[user_id] = profile
    return profile

def get_founder_profile(founder_id):
    return founder_profiles.get(founder_id)
