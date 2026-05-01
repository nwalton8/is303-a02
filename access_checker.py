'''
Noah Walton
IS 303 - A02

Access Checker
Determines access level based on role and clearance.
Different access for admin/employee/visitor, modified by clearance level or time of day

Inputs:
- User role (string)
- User clearance level (integer)
- Current time (string)

Processes:
- Validate role (must be one of the supported roles)
- Validate clearance level (must be between 1 and 5)
- Validate time (must be in HH:MM format)
- Determine access level based on role, clearance, and time

Outputs:
- Print access level
- Print error message if any input is invalid
'''



