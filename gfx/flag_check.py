import os

def validate_flags(folder_path, tags):
    """
    Validates the presence of required .tga files for a given list of tags in a specified folder.
    
    Args:
        folder_path (str): The path to the folder containing the .tga files.
        tags (list): A list of 3-letter country tags to validate.
    
    Returns:
        None
    """
    # Define the required flag formats
    required_flags = [
        "{tag}.tga",
        "{tag}_fascist.tga",
        "{tag}_communist.tga",
        "{tag}_monarchy.tga",
        "{tag}_republic.tga"
    ]
    
    missing_flags = []  # List to store missing flags

    # Loop through each tag and check for required files
    for tag in tags:
        for flag_template in required_flags:
            flag_file = flag_template.format(tag=tag)  # Replace {tag} with the actual tag
            flag_path = os.path.join(folder_path, flag_file)
            if not os.path.isfile(flag_path):  # Check if the file exists
                missing_flags.append(flag_file)

    # Output results
    if missing_flags:
        print("The following flag files are missing:")
        for flag in missing_flags:
            print(f"- {flag}")
        print("\nPlease review the missing files and add them to the folder.")
    else:
        print("All required flag files are present!")

# Example usage
if __name__ == "__main__":
    # Path to the folder containing .tga files
    folder_path = input("Enter the path to the folder containing the flag files: ").strip()
    
    # List of country tags to validate
    tags = input("Enter the list of 3-letter tags (separated by spaces): ").strip().split()
    
    # Validate the flags
    validate_flags(folder_path, tags)