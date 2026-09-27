import asyncio
import os
import shutil
import glob
from playwright.async_api import async_playwright

ARTIFACT_DIR = "/config/.gemini/antigravity/brain/5df8e501-c233-4058-8ffa-a8a60aa9c842"
RECORD_DIR = os.path.join(ARTIFACT_DIR, "video_temp")

async def record_demo():
    os.makedirs(RECORD_DIR, exist_ok=True)
    async with async_playwright() as p:
        print("Launching Chromium browser for recording...", flush=True)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            record_video_dir=RECORD_DIR,
            record_video_size={"width": 1280, "height": 800}
        )
        
        page = await context.new_page()
        print("Navigating to http://localhost:8080...", flush=True)
        await page.goto("http://localhost:8080", wait_until="networkidle")
        await asyncio.sleep(2)
        
        # 1. First interaction: Click example prompt chip for property search
        print("Submitting Prompt 1: Property Search...", flush=True)
        # Find prompt chip or type in input
        chip = page.locator(".prompt-chip").first
        if await chip.count() > 0:
            await chip.click()
        else:
            await page.fill("#input", "Find 3-bedroom houses under $750k in Austin with top-rated schools")
            await page.click("button:has-text('Send')")
            
        print("Waiting for Agent response to Prompt 1...", flush=True)
        await asyncio.sleep(14)
        
        # 2. Second interaction: Rich prompt for mortgage calculation & virtual staging image
        print("Submitting Prompt 2: Mortgage calculation & Virtual Staging Image...", flush=True)
        rich_prompt = "Calculate estimated monthly mortgage for a $650k house with 20% down, and generate a virtual staging photo for a modern living room."
        await page.fill("#input", rich_prompt)
        await asyncio.sleep(1)
        await page.click("form button")
        
        print("Waiting for Agent response to Prompt 2 (tools + image generation)...", flush=True)
        await asyncio.sleep(20)
        
        print("Closing browser context to finalize recording...", flush=True)
        await context.close()
        await browser.close()

        # Find generated video
        videos = glob.glob(os.path.join(RECORD_DIR, "*.webm"))
        if videos:
            target_path = os.path.join(ARTIFACT_DIR, "demo_recording.webm")
            shutil.copy(videos[0], target_path)
            print(f"DEMO VIDEO RECORDED SUCCESSFULLY: {target_path}", flush=True)
        else:
            print("ERROR: No video file found in recording directory.", flush=True)

if __name__ == "__main__":
    asyncio.run(record_demo())
