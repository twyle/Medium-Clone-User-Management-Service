

def validate_user_data(user_data: dict, profile_pic):
    """Validate user data."""
    if not user_data:
        raise ValueError("The authors data must be provided!")
    if not isinstance(user_data, dict):
        raise ValueError("The author data must be a dictionary!")
    valid_keys = [
        "First Name",
        "Last Name",
        "Email Address",
        "Nickname",
        "Password",
    ]
    for key in user_data.keys():
        if key not in valid_keys:
            raise ValueError(f"The only valid keys are {valid_keys}")
    if "First Name" not in user_data.keys():
        raise ValueError("The First Name must be provided")
    if "Last Name" not in user_data.keys():
        raise ValueError("The Last Name must be provided")
    if not user_data["First Name"]:
        raise ValueError("The First Name must be provided")
    if not user_data["Last Name"]:
        raise ValueError("The Last Name must be provided")
    if "Password" not in user_data.keys():
        raise ValueError("The password must be provided!")
    if not user_data["Password"]:
        raise ValueError("The password must be provided!")
    if "Email Address" not in user_data.keys():
        raise ValueError("The Emai address must be provide!")
    if not user_data["Email Address"]:
        raise ValueError("The Email address must be provide!")