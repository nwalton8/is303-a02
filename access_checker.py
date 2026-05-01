'''
Noah Walton
IS 303 - A02

Access Checker
Determines access level based on role and clearance.
Different access for admin/employee/visitor, modified by clearance level or time of day

Inputs:
- User name (string)
- User role (string)
- Time of day (string)

Processes:
- Validate role (must be one of the supported roles)
- Validate time (must be "open" or "closed")
- Determine access level based on role and time

Outputs:
- Print access level
- Print error message if any input is invalid
'''

#Input: Get user information
user_name = input("Enter your name: ")
user_role = input("Enter your role (admin, employee, visitor): ").lower()
if user_role not in ["admin", "employee", "visitor"]:
    print("Error: Please enter 'admin', 'employee', or 'visitor'.")
else:
    current_time = input("Enter 'open' or 'closed' based on the time (open hours is 10 AM - 10 PM): ").lower()
    if current_time not in ["open", "closed"]:
        print("Error: Please enter 'open' or 'closed'.")
    else:
        #Process: Determine access level
        if user_role == "admin":
            access_level = "full access (lvl 5 clearance)"
        elif user_role == "employee":
            if current_time == "open":
                access_level = "partial access (lvl 3 clearance)"
            else:
                access_level = "no access"
        else:  # visitor
            if current_time == "open":
                access_level = "visitor access (lvl 1 clearance)"
            else:
                access_level = "no access"
        #Output: Print access level
        print(f"{user_name}, as the museum is {current_time} and you are a {user_role}, your current access level is: {access_level}.")
        