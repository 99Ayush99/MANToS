import os 


def get_database_info():
    """Return database information from environment variables."""
    folder_path = "spider_data/database"

    folders = [
        name for name in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, name))
    ]
    folders.sort()
    return folders

# if __name__ == "__main__":
#     get_database_info()