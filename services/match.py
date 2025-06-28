import uuid

matches = {}

# Seed with a sample match
sample_match_id = str(uuid.uuid4())
matches[sample_match_id] = {
    'id': sample_match_id,
    'type': 'advisor',
    'name': 'Sarah Chen',
    'title': 'Ex-VP Product, Stripe',
    'company': 'Stripe',
    'location': 'San Francisco',
    'matchScore': 95,
    'reasoning': ['8 years in FinTech product', 'Led 0-to-1 payment solutions', 'Expertise in regulatory compliance'],
    'valueAdd': 'Product strategy, Go-to-market, Fundraising',
    'nextStep': 'Request Introduction',
    'avatarUrl': None,
    'linkedinUrl': None,
    'expertise': ['FinTech', 'Payments']
}

def get_matches(match_type=None, min_score=None, limit=20, offset=0):
    filtered = list(matches.values())
    if match_type:
        filtered = [m for m in filtered if m['type'] == match_type]
    if min_score:
        filtered = [m for m in filtered if m['matchScore'] >= min_score]
    return {
        'matches': filtered[offset:offset+limit],
        'pagination': {
            'total': len(filtered),
            'limit': limit,
            'offset': offset,
            'hasMore': offset+limit < len(filtered)
        }
    }

def get_match(match_id):
    return matches.get(match_id)
