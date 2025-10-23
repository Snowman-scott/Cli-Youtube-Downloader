import os
import yt_dlp
from yt_dlp import YoutubeDL
from Functions import clear_terminal
from Functions import get_browser_choice
from Functions import get_format_choice
from Functions import filter_formats
from Functions import display_formats
from Save_location_grabber import get_download_path



def main():
    print("YouTube Video Downloader")
    print("\nNote: This currently only supports YouTube.")
    print("If you get Error 403 Yt-dlp may be out of date! Plese refer to the README!")
    print("All audio downloads can be converted to MP3 format.")
    print("FFmpeg is Requiered to convert Audio files to MP3s")
    print("\nThank you for using this tool!\n")

    url = input("\n\n\nEnter URL of Video you want to Download: ")
    while not url or ("youtu.be/" not in url and "youtube.com/watch?v=" not in url):
        print("Invalid URL. Please Enter a Valid Youtube URL")
        url = input("Enter URL of Video you want to Download: ")

    print("\nValid URL")

    # Get browsrr choice
    browser = get_browser_choice()
    if browser:
        ydl_opts = {'cookiesfrombrowser': (browser,)}
    else:
        ydl_opts = {}

    # Extract the video info
    clear_terminal()
    print("Fetching Video information...")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        clear_terminal()
        print(f"Error: Could not fetch video information")
        print(f"Details: {e}")
        print("\nPossible reasons:")
        print("- Invalid or unsupported URL")
        print("- Video is private, deleted, or region-restricted")
        print("- Network connection issues")
        if browser:
            print("- Browser cookies couldn't be accessed (try 'Skip' option)")
        return
    except Exception as e:
        clear_terminal()
        print(f"Unexpected error: {e}")
        return


    if not info.get('formats'):
        print("Error: No formats available for this video")
        return
    
    clear_terminal()

    # Get format preferances
    format_type = get_format_choice()
    valid_formats = filter_formats(info['formats'], format_type)

    if not valid_formats:
        print(f"\nNo {format_type} formats found for this video.")
        return
    
    print(f"Avalible {format_type} formats:\n")
    display_formats(valid_formats)


    # user selects format
    while True:
        try:
            choice = int(input(f"Enter option number (0-{len(valid_formats)-1}): "))
            if 0 <= choice < len(valid_formats):
                break
            else:
                print(f"Invalid choice.\nPlease enter a number between 0 and {len(valid_formats) -1}.")
        except ValueError:
            print("Please enter a valid number.")

    selected_format = valid_formats[choice]
    print(f"\nSelected: {selected_format.get('resolution','audio only')} ({selected_format['ext']})")

    save_path = get_download_path()
    clear_terminal()

    download_opts = {
        'format': selected_format['format_id'],
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
    }

    if browser:
        download_opts['cookiesfrombrowser'] = (browser,)

    # Audio conversion handeling
    print("MP3 conversion can only be done IF you have FFmpeg installed on your system!")
    if format_type in ['audio', 'a']:
        while True:
            convert = input("Convert to an MP3? (y/n)").strip().lower()
            if convert in ['y', 'yes']:
                audio_bitrate = selected_format.get('abr', 192)
                download_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': str(int(audio_bitrate)),
                }]
                print(f"(Audio will be converted to MP3 at {audio_bitrate} kbps)")
                break
            elif convert in ['n','no']:
                break
            else:
                print("Please enter 'y' or 'n'")

    try:
        clear_terminal()
        with YoutubeDL(download_opts) as ydl:
            ydl.download([url])
            clear_terminal()
        print("\n✓ Download completed successfully!")
        print(f"Saved to: {save_path}")
    except yt_dlp.utils.DownloadError as e:
        clear_terminal()
        print(f"\n✗ Download failed: {e}")
        print("\nPossible reasons:")
        print("- Video may be restricted or unavailable in your region")
        print("- Video may be age-restricted or private")
        print("- URL may be Broken! Try grabbing new URL")
        print("- Yt-dlp may be out of date. Get a new version of application")
    except Exception as e:
        clear_terminal()
        print(f"\n✗ Unexpected Error: {e}")

if __name__ == "__main__":
    main()