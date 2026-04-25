"""
🚀 SOCIAL MEDIA AUTO-POSTER (GOLD TIER)
Uses Playwright to automatically post content from /Approved folder.
"""

import os
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
import asyncio
from playwright.sync_api import sync_playwright

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [POSTER] - %(message)s')
logger = logging.getLogger('SocialPoster')

class SocialMediaPoster:
    def __init__(self, vault_path: str):
        self.approved_folder = Path(vault_path) / "Approved"
        self.done_folder = Path(vault_path) / "Done"
        self.approved_folder.mkdir(exist_ok=True)
        self.done_folder.mkdir(exist_ok=True)

    def post_to_linkedin(self, content):
        """Simple mockup for automation - In real world, needs cookie/session or login."""
        logger.info("Opening Browser for LinkedIn Posting...")
        with sync_playwright() as p:
            # Using persistent context to keep login session
            user_data_dir = os.path.join(os.getcwd(), ".playwright_data")
            browser = p.chromium.launch_persistent_context(user_data_dir, headless=False)
            page = browser.new_page()
            
            try:
                page.goto("https://www.linkedin.com/feed/")
                logger.info("Waiting for page load and checking login...")

                # Try multiple common LinkedIn post button selectors
                post_selectors = [
                    "button.share-box-feed-entry__trigger", 
                    "button.share-mb-launcher",
                    "text='Start a post'",
                    "button:has-text('Start a post')",
                    "[aria-label='Start a post']"
                ]
                
                button_found = False
                for selector in post_selectors:
                    try:
                        logger.info(f"Trying selector: {selector}")
                        page.wait_for_selector(selector, timeout=5000)
                        page.click(selector)
                        button_found = True
                        break
                    except:
                        continue
                
                if not button_found:
                    logger.warning("Could not find Post button automatically. Please click it manually!")

                # Fill the post content (Try different editor selectors)
                page.wait_for_selector(".ql-editor, .editor-content", timeout=10000)
                page.fill(".ql-editor, .editor-content", content)
                
                logger.info("Ready to Post! (Please login if needed. Waiting 60 seconds...)")
                # page.click("button.share-actions__primary-action") # Uncomment to fully automate
                time.sleep(60) # Give user enough time to login and see
                
                return True
            except Exception as e:
                logger.error(f"Failed to post: {e}")
                return False
            finally:
                # browser.close() # Commented out for debugging
                logger.info("Browser kept open for user observation.")

    def run(self):
        logger.info("Social Poster Service Started. Monitoring /Approved folder...")
        while True:
            approved_files = list(self.approved_folder.glob("*.md"))
            for file in approved_files:
                logger.info(f"Detected approved post: {file.name}")
                content = file.read_text(encoding='utf-8')
                
                success = self.post_to_linkedin(content)
                if success:
                    # Move to Done
                    file.rename(self.done_folder / file.name)
                    logger.info(f"Task completed and moved to Done: {file.name}")
            
            time.sleep(30) # Check every 30 seconds

if __name__ == "__main__":
    POSTER = SocialMediaPoster("D:/Urooj/Hackthon 0/AI_Employee_Vault")
    POSTER.run()
