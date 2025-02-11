# Instagram Follower & Following Tracker

This script is designed to track changes in your Instagram followers and followings using Selenium and JSON data storage.

## Features

- Logs in to Instagram using provided credentials.
- Fetches and stores the current list of followers and followings.
- Compares new data with previously stored data to detect changes.
- Saves differences (new followers, lost followers, new followings, unfollowed users) in a JSON file.

## How It Works

1. **First Run:**

   - The program logs into Instagram and fetches the current list of followers and followings.
   - It saves this data in `username.json` (where `username` is the provided Instagram username).
   - No comparison is made on the first run since there is no previous data available.

2. **Subsequent Runs:**

   - The script fetches the latest follower and following data.
   - Compares it with the previously saved data.
   - Identifies new and removed followers/followings.
   - Saves the updated data and the detected differences.

## Requirements

- Python 3.x
- Selenium
- Firefox & GeckoDriver
- jsondiff

## Installation

1. Install required dependencies:
   ```sh
   pip install selenium jsondiff
   ```
2. Ensure Firefox and GeckoDriver are installed and properly configured.
3. Create an `account.py` file containing your Instagram credentials:
   ```python
   instauser = "your_username"
   instapass = "your_password"
   ```

## Usage

Run the script:

```sh
python script.py
```

- On the first run, the script will only store the existing followers and followings.
- On subsequent runs, it will compare the new data with previously stored data and print the differences.

## Author

Özgür Alagöz

