"""WeGovNow extension base."""

# ###########################
# ONTOMAP LOG MODELS
# ###########################


LOG_MODELS = [
    'Project',
    'Category',
    'Observation',
    'Comment',
    'AudioFile',
    'ImageFile',
    'VideoFile'
]

# Only specific fields are being watched for OnToMap to trigger a new event
WATCHED_FIELDS = [
    'status',
    'isprivate',
    'name',
    'description',
    'properties'
]

# ###########################
# ONTOMAP MAPPINGS
# ###########################

PROJECT_MAPPING = {
    'app_concept': 'Project',
    'ontomap_concept': 'Project',
    'properties': [
        {
            'app_property': 'name',
            'ontomap_property': 'hasName'
        }
    ]
}

CATEGORY_MAPPING = {
    'app_concept': 'Category',
    'ontomap_concept': 'Category',
    'properties': [
        {
            'app_property': 'name',
            'ontomap_property': 'hasName'
        }
    ]
}

CONTRIBUTION_MAPPING = {
    'app_concept': 'Contribution',
    'ontomap_concept': 'AtomicThing',
    'properties': []
}

COMMENT_MAPPING = {
    'app_concept': 'Comment',
    'ontomap_concept': 'Comment',
    'properties': []
}

MEDIAFILE_MAPPING = {
    'app_concept': 'MediaFile',
    'ontomap_concept': 'Document',
    'properties': [
        {
            'app_property': 'name',
            'ontomap_property': 'hasName'
        }
    ]
}

# All mappings merged
MAPPINGS = [
    PROJECT_MAPPING,
    CATEGORY_MAPPING,
    CONTRIBUTION_MAPPING,
    COMMENT_MAPPING,
    MEDIAFILE_MAPPING
]
