import googleapiclient.discovery, googleapiclient.errors
import webbrowser

def open_browser(url):
    webbrowser.open_new_tab(url)


def search_video(query):
    api_service_name = "youtube"
    api_version = "v3"
    api_key = "AIzaSyBlqD7bRth9-C3vFIKq_NiMW-4Z65PX2sY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    request = youtube.search().list(
        part="id",
        q=query,
        type="video",
        videoDefinition="high",
        maxResults=1
    )
    response = request.execute()

    video_id = response['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return video_url