import os
import shutil
import re


def read_tags_from_file(file_path):
    """
    Reads 3-letter country tags from a countries.txt file.
    Ignores comment lines (starting with #).

    Args:
        file_path (str): Path to the countries.txt file.

    Returns:
        list: List of 3-letter country tags.
    """
    tags = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Skip comments and empty lines
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Extract the first 3 characters as the tag
                tag_match = re.match(r'([A-Z0-9]{3})\s*=', line)
                if tag_match:
                    tag = tag_match.group(1)
                    tags.append(tag)
    except Exception as e:
        print(f"Error reading tags file: {e}")
        return []

    return tags


def validate_flags(folder_path, tags, auto_fix=False):
    """
    Validates the presence of required .tga files for a given list of tags in a specified folder.
    Can also automatically fix missing files by copying a template file.

    Args:
        folder_path (str): The path to the folder containing the .tga files.
        tags (list): A list of 3-letter country tags to validate.
        auto_fix (bool): Whether to automatically fix missing files.

    Returns:
        list: List of missing flags (empty if all files are present)
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

    return missing_flags


def create_missing_flags(folder_path, missing_flags):
    """
    Creates missing flag files by copying a template file (GHO.tga).

    Args:
        folder_path (str): The path to the folder containing the flag files.
        missing_flags (list): List of missing flag files to create.

    Returns:
        bool: True if all files were created successfully, False otherwise.
    """
    template_file = os.path.join(folder_path, "GHO.tga")

    # Check if template file exists
    if not os.path.isfile(template_file):
        print(f"Error: Template file '{template_file}' not found.")
        return False

    success = True
    created_files = []

    # Copy template to create missing files
    for flag_file in missing_flags:
        target_path = os.path.join(folder_path, flag_file)
        try:
            shutil.copy2(template_file, target_path)
            created_files.append(flag_file)
        except Exception as e:
            print(f"Error creating {flag_file}: {e}")
            success = False

    if created_files:
        print("\nCreated the following flag files:")
        for flag in created_files:
            print(f"- {flag}")

    return success


# Example usage
if __name__ == "__main__":
    # Path to the folder containing .tga files
    folder_path = input("Enter the path to the folder containing the flag files: ").strip()

    # Path to the countries.txt file
    countries_file = input("Enter the path to the countries.txt file: ").strip()

    # Read tags from the countries file
    tags = read_tags_from_file(countries_file)

    if not tags:
        print("No valid country tags found in the file. Exiting.")
    else:
        print(f"Found {len(tags)} country tags: {', '.join(tags)}")

        # First validation
        print("\n=== Initial Flag Check ===")
        missing_flags = validate_flags(folder_path, tags)

        # Create missing flags if needed
        if missing_flags:
            create_missing = input("\nDo you want to create the missing flags? (y/n): ").strip().lower()
            if create_missing == 'y':
                print("\n=== Creating Missing Flags ===")
                if create_missing_flags(folder_path, missing_flags):
                    # Run the validation again to verify
                    print("\n=== Verification Flag Check ===")
                    validate_flags(folder_path, tags)
                else:
                    print("\nSome files could not be created. Please check the errors above.")
        else:
            print("\nNo need to create any missing files.")