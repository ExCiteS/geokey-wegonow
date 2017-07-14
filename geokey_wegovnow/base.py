'''Base for geokey-wegovnow extension.'''
# -*- coding: UTF-8 -*-

# Ontomap models we want to provide information
# Note that while it is possible to transmit the information relating to a new Field added to a category, this isn't built in at the OntoMap end 
# so as there is no mapping it will fail - so removed this option from the list
# ONTOMAP_MODELS = ['Project', 'Observation', 'Comment', 'MediaFile', 'Category', 'Field']
ONTOMAP_MODELS = ['Project', 'Observation', 'Comment', 'MediaFile', 'Category']

# OntoMap urls
ONTOMAP_URLS = {
    'event': 'https://api.ontomap.eu/api/v1/logger/events',
    'mapping': 'https://api.ontomap.eu/api/v1/logger/mappings',
}

# OntoMap event (json)
#  created_json = '''{'event_list': [
#     {
#         'actor': $uwum_user_id$,
#        'timestamp': $timestamp$,
#         'activity_type': '$activity_type$',
#         'activity_objects': [
#             {
#                 'type': 'Feature',
#                 'geometry': $geometry$,
#                 'properties': {
#                     'hasType': '$hasType$',
#                     'external_url': '$external_url$',
#                     'additionalProperties': $additional_prop$
#                 }

#             }
#         ],
#         'visibility_details': [{
#             'external_url': '$external_url$',
#             'hidden': $hidden$
#         }],
#         'details': [{
#             'task': 'newProjectCreated',
#             'projectID': 26
#         }]
#     }
# ]
# }''' 

# NB: the string needs to be on one line otherwise there will be extra \n in the string!
created_json = "{'event_list': [{'actor': $uwum_user_id$,'timestamp': $timestamp$,'activity_type': '$activity_type$','activity_objects': [{'type': 'Feature','geometry': $geometry$,'properties': {'hasType': '$hasType$','external_url': '$external_url$','additionalProperties': $additional_prop$}}],'visibility_details': [{'external_url': '$external_url$','hidden': $hidden$}],'details': {'task': 'newProjectCreated','projectID': 26}}]}"


# OntoMap mapping (json)
mappingjson = '''{
    'mappings':
    [
        {
            'app_concept': 'Project',
            'ontomap_concept': 'Project',
            'properties':
            [
                {
                    'app_property': 'name',
                    'ontomap_property': 'hasName'
                },
                {
                    'app_property': 'description',
                    'ontomap_property': 'hasDescription'
                }
            ]
        },
        {
            'app_concept': 'Collection',
            'ontomap_concept': 'Collection',
            'properties':
            [
                {
                    'app_property': 'name',
                    'ontomap_property': 'hasName'
                },
                {
                    'app_property': 'description',
                    'ontomap_property': 'hasDescription'
                }
            ]
        },
        {
            'app_concept': 'Contribution',
            'ontomap_concept': 'AtomicThing',
            'properties':
            [
                {
                    'app_property': 'name',
                    'ontomap_property': 'hasName'
                },
                {
                    'app_property': 'description',
                    'ontomap_property': 'hasDescription'
                },
                {
                    'app_property': 'category',
                    'ontomap_property': 'hasCategoryName'
                }
            ]
        },
        {
            'app_concept': 'MediaFile',
            'ontomap_concept': 'Document',
            'properties':
            [
                {
                    'app_property': 'name',
                    'ontomap_property': 'hasName'
                },
                {
                    'app_property': 'description',
                    'ontomap_property': 'hasDescription'
                }
            ]
        },
        {
            'app_concept': 'Comment',
            'ontomap_concept': 'Comment',
            'properties':
            [
                {
                    'app_property': 'name',
                    'ontomap_property': 'hasName'
                },
                {
                    'app_property': 'description',
                    'ontomap_property': 'hasDescription'
                }
            ]
        },
        {
            'app_concept': 'Category',
            'ontomap_concept': 'Category',
            'properties':
            [
                {
                    'app_property': 'name',
                    'ontomap_property': 'hasName'
                },
                {
                    'app_property': 'description',
                    'ontomap_property': 'hasDescription'
                }
            ]
        }
    ]
}'''

# GeoKey api call to be replaced on external_url.
api_call = {
    'Category': '/api/projects/$project_id$/categories/$category_id$/',
    'Project': '/api/projects/$project_id$/',
    'Field': '/api/projects/$project_id$/categories/$category_id$/fields/$field_id$',
    'Observation': '/api/projects/$project_id$/contributions/$contri_id$',
    'Comment': '/api/projects/$project_id$/contributions/$contri_id$/comments/',
    'MediaFile': '/api/projects/$project_id$/contributions/$contri_id$/media/$media_id$',
}
