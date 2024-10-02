import os
from dotenv import load_dotenv
import asyncio
import csv
from twikit import Client
from datetime import datetime

###########################################
# Load environment variables
load_dotenv()

# X.com credentials
USERNAME = os.getenv("TWIKIT_USERNAME")
EMAIL = os.getenv("TWIKIT_EMAIL")
PASSWORD = os.getenv("TWIKIT_PASSWORD")

# X accounts to check and their custom sizes
CUSTOM_SIZES = {
    'sleeperpickshq': [{'width': 1350, 'height': 1350}, {'width': 2400, 'height': 2400}, {'width': 1200, 'height': 1200}],
    'prizepicks': [{'width': 1080, 'height': 1350}],
    'underdogpicks': [{'width': 1080, 'height': 1350}],
    'betrpicks': [{'width': 2410, 'height': 2410}, {'width': 1080, 'height': 1350}],
    'parlay_play': [{'width': 1000, 'height': 995}],
    'chalkboardhq': [{'width': 1400, 'height': 1481}],
}

# CSV file for storing media URLs
CSV_FILE = 'media_urls.csv'

# Ensure the client is initialized
client = Client('en-US')

# Function to append data to CSV
def save_to_csv(timestamp, username, media_url):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'username', 'media_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write header only if file doesn't exist

        writer.writerow({'timestamp': timestamp, 'username': username, 'media_url': media_url})
        print(f"Saved to CSV: {timestamp}, {username}, {media_url}")

# Function to check if the image matches custom size for the given sportsbook
def check_image_dimensions(media, username):
    # Get the list of valid sizes for this account
    valid_sizes = CUSTOM_SIZES.get(username, [])
    if not valid_sizes:
        return False  # No size specifications for this account
    
    # Check the 'large' size
    sizes = media.get('sizes', {})
    large_size = sizes.get('large', {})
    width = large_size.get('w')
    height = large_size.get('h')

    # Check if the current dimensions match any of the valid sizes
    for size in valid_sizes:
        if width == size['width'] and height == size['height']:
            return True  # If any size matches, return True
    
    return False  # No matching sizes found

# Main function to process the tweets
async def main():
    try:
        # Log in to the Twikit client
        await client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD
        )
    except Exception as e:
        print(f"Error during login: {e}")
        return
    
    # Iterate through the list of X accounts
    for account, sizes in CUSTOM_SIZES.items():
        try:
            user = await client.get_user_by_screen_name(account)
            print(f"Fetching tweets for {user.name} (@{account})...")

            # Get the 100 most recent tweets with media
            user_tweets = await user.get_tweets('Media', count=100)
            
            if not user_tweets:
                print(f"No tweets found for {account}.")
                continue

            # Process and save media URLs only if valid
            for tweet in user_tweets:
                if tweet.media:
                    for media in tweet.media:
                        if media.get('type') == 'photo':  # Check if the media type is 'photo'
                            media_url = media.get('media_url_https')
                            
                            # Separate the checks for media URL and dimensions
                            if not media_url:
                                print(f"Tweet {tweet.id} from {account} has no valid media URL.")
                            elif not check_image_dimensions(media, account):
                                print(f"Tweet {tweet.id} from {account} has valid media URL but dimensions don't match.")
                            else:
                                # All checks passed: URL is valid and dimensions match
                                timestamp = tweet.created_at  # Use the tweet's timestamp as a string directly
                                save_to_csv(timestamp, account, media_url)
                        else:
                            print(f"Tweet {tweet.id} from {account} media type is not 'photo', skipping.")
                else:
                    print(f"Tweet {tweet.id} from {account} has no media.")

        except Exception as e:
            print(f"Error fetching or processing tweets for {account}: {e}")

# Run the main function in an asyncio event loop
asyncio.run(main())