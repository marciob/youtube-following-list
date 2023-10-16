import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json

# Initialize YouTube API client
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

# Get OAuth 2.0 credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    "HERE_PLACE_THE_CLIENT_SECRET_FILE_NAME_GOT_FROM_GOOGLE.json", 
    ["https://www.googleapis.com/auth/youtube.readonly"]
)

credentials = flow.run_console()
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

def get_all_subscriptions(youtube, max_results=50):
    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=max_results
    )

    all_subscriptions = []
    while request is not None:
        response = request.execute()
        all_subscriptions.extend(response["items"])
        request = youtube.subscriptions().list_next(request, response)

    return all_subscriptions

# Fetch all subscriptions
all_subscriptions = get_all_subscriptions(youtube)

# Save subscriptions to a JSON file
subscriptions_data = []
for item in all_subscriptions:
    channel_title = item['snippet']['title']
    channel_id = item['snippet']['resourceId']['channelId']
    channel_url = f"https://www.youtube.com/channel/{channel_id}"
    subscriptions_data.append({"Channel title": channel_title, "Channel URL": channel_url})
    print(f"{channel_title}, {channel_url}")

with open('subscriptions.json', 'w', encoding='utf-8') as f:
    json.dump(subscriptions_data, f, ensure_ascii=False, indent=4)
