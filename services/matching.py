def discover_founders(filters, founders):
    # For MVP, ignore filters and return all founders
    return {'founders': list(founders.values()), 'pagination': {'total': len(founders), 'limit': 20, 'offset': 0, 'hasMore': False}}

def get_founder_profile(founder_id, founders):
    return founders.get(founder_id)
