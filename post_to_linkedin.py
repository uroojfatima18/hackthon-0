import time
import os
from playwright.sync_api import sync_playwright

post_content = (
    "Just wrapped up my latest hackathon project, and I'm thrilled to share what I've built!\n\n"
    "I've successfully created a Personal AI Employee - a local-first, agent-driven system "
    "designed to manage personal and business affairs, 24/7. My secret sauce? Claude Code and Obsidian.\n\n"
    "I believe AI isn't just about large-scale solutions; it's also about empowering individuals. "
    "This project is a testament to the power of combining cutting-edge AI with personal productivity tools.\n\n"
    "What are your thoughts on AI personal assistants? Let me know in the comments!\n\n"
    "#AI #Automation #AIEmployee #Hackathon #BuildInPublic"
)

user_data_dir = os.path.join(os.getcwd(), ".playwright_data")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        slow_mo=500
    )
    page = browser.new_page()
    print("Opening LinkedIn...")
    page.goto("https://www.linkedin.com/feed/")
    page.wait_for_load_state("networkidle", timeout=15000)
    print("Page loaded.")
    time.sleep(3)

    if "login" in page.url or "signup" in page.url:
        print("NOT LOGGED IN - Please login manually in the browser window!")
        print("Waiting 90 seconds for manual login...")
        time.sleep(90)

    print("Looking for Start a Post button...")
    selectors = [
        "button:has-text(\"Start a post\")",
        "[aria-label=\"Start a post\"]",
        ".share-box-feed-entry__trigger",
    ]

    clicked = False
    for sel in selectors:
        try:
            page.wait_for_selector(sel, timeout=5000)
            page.click(sel)
            clicked = True
            print(f"Clicked: {sel}")
            break
        except Exception:
            continue

    if not clicked:
        print("Could not find post button. Browser is open - click Start a Post manually then press Enter here.")
        input("Press Enter when you've clicked Start a Post...")

    time.sleep(2)
    print("Typing post content...")

    try:
        # Instead of looking for a specific textbox class, just click the modal and type
        # Or wait a bit and type directly since it should be focused
        page.wait_for_timeout(2000)
        print("Typing via keyboard...")
        page.keyboard.type(post_content, delay=10)
        print("Content typed! Waiting 5 seconds...")
        time.sleep(5)

        post_buttons = [
            "button.share-actions__primary-action",
            "button:has-text(\"Post\")",
        ]
        posted = False
        for btn in post_buttons:
            try:
                page.click(btn, timeout=5000)
                print("POST BUTTON CLICKED! Post published!")
                posted = True
                time.sleep(3)
                break
            except Exception:
                continue

        if not posted:
            print("Could not find Post button automatically.")
            input("Please click the Post button manually, then press Enter...")

        print("SUCCESS! Check your LinkedIn profile.")
    except Exception as e:
        print(f"Error: {e}")
        input("Please complete posting manually, then press Enter to close...")

    browser.close()
    print("Browser closed.")
