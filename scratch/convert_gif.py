import imageio
from PIL import Image

WEBM_PATH = "/config/.gemini/antigravity/brain/5df8e501-c233-4058-8ffa-a8a60aa9c842/demo_recording.webm"
GIF_PATH = "/config/Desktop/gemini/real-estate-finder/demo.gif"

print("Reading WEBM video...", flush=True)
reader = imageio.get_reader(WEBM_PATH)
fps = reader.get_meta_data().get('fps', 20)

frames = []
# Subsample frames to keep GIF size reasonable (e.g., skip every 2 frames)
for i, frame in enumerate(reader):
    if i % 3 == 0:  # Take 1 out of every 3 frames (~6-7 fps)
        img = Image.fromarray(frame)
        # Resize to max width 800
        w, h = img.size
        if w > 800:
            new_h = int(h * (800 / w))
            img = img.resize((800, new_h), Image.Resampling.LANCZOS)
        frames.append(img)

print(f"Captured {len(frames)} frames. Writing GIF to {GIF_PATH}...", flush=True)
if frames:
    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=150,  # ~6.6 fps
        loop=0
    )
    print("GIF CONVERSION COMPLETED SUCCESSFULLY!", flush=True)
