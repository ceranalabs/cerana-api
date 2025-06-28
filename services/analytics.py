def get_pipeline_analytics(filters):
    # Return sample analytics data
    return {
        'overview': {
            'totalDeals': 10,
            'activeDeals': 5,
            'averageDaysToClose': 32.5,
            'conversionRate': 0.25
        },
        'stageBreakdown': [
            {'stage': 'sourced', 'count': 3, 'averageDays': 5},
            {'stage': 'due-diligence', 'count': 2, 'averageDays': 12},
            {'stage': 'closed', 'count': 5, 'averageDays': 60}
        ],
        'sectorPerformance': [
            {'sector': 'AI/ML', 'dealCount': 4, 'successRate': 0.5},
            {'sector': 'SaaS', 'dealCount': 6, 'successRate': 0.33}
        ],
        'monthlyTrends': [
            {'month': '2024-01', 'dealsAdded': 2, 'dealsClosed': 1, 'averageMatchScore': 90},
            {'month': '2024-02', 'dealsAdded': 3, 'dealsClosed': 2, 'averageMatchScore': 88}
        ]
    }

def get_market_intelligence(filters):
    # Return sample market intelligence data
    return {
        'sectorTrends': [
            {'sector': 'AI/ML', 'momentum': 'hot', 'averageValuation': 15000000, 'dealVolume': 12, 'topCompanies': ['TechFlow AI', 'DataSense']},
            {'sector': 'SaaS', 'momentum': 'warm', 'averageValuation': 10000000, 'dealVolume': 8, 'topCompanies': ['CloudOps', 'BizSuite']}
        ],
        'competitiveLandscape': [
            {'company': 'TechFlow AI', 'stage': 'series-a', 'lastFunding': 2000000, 'investors': ['VC Firm', 'Angel Group']}
        ],
        'fundingTrends': {
            'averageCheckSize': 500000,
            'medianValuation': 12000000,
            'timeToClose': 45,
            'hotSectors': ['AI/ML', 'FinTech']
        }
    }
