
power = ['Individual', 'Team', 'Director', 'Enterprise', ]
management_levels = [
    'Individual',
    'Senior Individual',
    'Team',
    'Senior Team',
    'Director',
    'Senior Director',
    'Enterprise',
    'Senior Enterprise',
]
internal_cost_centers = ['Facilities', 'Experience', 'Talent', 'Enterprise', 'Legal', 'Technology',
                         'Marketing', 'Finance', 'BD', 'Global']

email_col = 'Email - Work'
level_col = 'Management Level'
cost_center_col = 'Cost Center'
identifiers = ['Employee Id', 'Worker', email_col, 'Preferred Name', ]
biz_details = [
    # 'businessTitle', 'Position', # businessTitle == Position?? - nope some diff
    'Active Status',
    'Cost Center',
    # 'Job Profile',
    'Job Family',
    # 'Craft Cohort',
    # 'Domain',
    'On Leave',
    'Management Level',
    'Time Type',
    'Worker Type',
    'Hire Date',
    'Region',
    'Location'
]
# BASED ON PAGE
general_info = ['Job Family', 'Time Type', 'Worker Type']

true_region_mapping = {
    'NA': ['Remote', 'Lion', 'Cambridge', 'Chicago', 'San Francisco'],
    'Asia': ['Tokyo', 'Shanghai', 'Singapore'],
    'Europe': ['Munich', 'London'],
}

studio_details = {
    'Cambridge': {'lat': 42.3668233, 'long': -71.1060706},
    'Chicago': {'lat': 41.883718, 'long': -87.632382},
    'San Francisco': {'lat': 37.73288916682891, 'long': -122.5024402141571},
    'London': {'lat': 51.5033466, 'long': -0.0793965},
    'Munich': {'lat': 48.1379879, 'long': 11.575182},
    'Shanghai': {'lat': 31.2203102, 'long': 121.4623931},
    'Singapore': {'lat': 1.351616, 'long': 103.808053},
    'Tokyo': {'lat': 35.689506, 'long': 139.6917},
}