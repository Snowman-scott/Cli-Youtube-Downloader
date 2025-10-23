import os

def clear_terminal():
    """Clear terminal on Windows, Mac, and Linux"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_browser_choice():
    print("\nTo avoid YouTube bot detection, we'll use your browser's cookies.")
    print("Which browser are you using?")
    print("1. Chrome")
    print("2. Firefox")
    print("3. Edge")
    print("4. Safari")
    print("5. Skip (may not work)")

    browser_map = {
        '1': 'chrome',
        '2': 'firefox',
        '3': 'edge',
        '4': 'safari',
        '5': None
    }
    choice = input("Enter number (1-5): ").strip()
    return browser_map.get(choice, 'chrome')

def get_format_choice():
    while True:
        choice = input("Do you want to download just the audio or video with audio? (audio/video) ").strip().lower()
        if choice in ['audio', 'a']:
            return 'audio'
        elif choice in ['both','b','v','video']:
            return 'video'
        else:
            print("Please enter audio or video")

def filter_formats(formats, format_type):
    valid_formats = []
    
    for fmt in formats:
        if format_type == 'audio':
            if fmt.get('acodec', 'none') != 'none' and fmt.get('vcodec', 'none') == 'none':
                valid_formats.append(fmt)
        else:
            if fmt.get('vcodec', 'none') != 'none' and fmt.get('acodec', 'none') != 'none':
                valid_formats.append(fmt)
    return valid_formats

def display_formats(formats):
    for idx, fmt in enumerate(formats):
        print(f"\nOption {idx}: ")
        print(f"  Resolution: {fmt.get('resolution', 'audio only')}")
        print(f"  Format ID: {fmt['format_id']}")
        print(f"  Extension: {fmt['ext']}")
        if 'abr' in fmt and fmt['abr']:
            print(f"  Audio bitrate: {fmt['abr']} kbps")