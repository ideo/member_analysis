email_col = 'Email Work'
identifiers = ['Employee ID', 'Worker', email_col, 'Preferred Name', ]

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
    'location']

true_region_mapping = {
    'NA': ['Remote', 'Lion', 'Cambridge', 'Chicago', 'San Francisco'],
    'Asia': ['Tokyo', 'Shanghai', 'Singapore'],
    'Europe': ['Munich', 'London'],
}