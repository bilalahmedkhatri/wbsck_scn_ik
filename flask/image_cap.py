from PIL import ImageGrab
import time

# The number of screenshots we want to capture
num_screenshots = 10

# The list to hold our screenshot data
screenshots = []

# Capture the screenshots as quickly as possible
start_time = time.time()
for i in range(num_screenshots):
    screenshot = ImageGrab.grab()
    screenshots.append(screenshot)

end_time = time.time()

# Calculate the time taken and the capture rate
time_taken = end_time - start_time
capture_rate = num_screenshots / time_taken

print(f"Captured {num_screenshots} screenshots in {time_taken:.2f} seconds at a rate of {capture_rate:.2f} screenshots per second.")

# Save the screenshots (optional)
for idx, screenshot in enumerate(screenshots):
    screenshot.save(f"screenshot_{idx}.jpg", "JPEG", quality=50)


# Output the result
if capture_rate >= 10:
    print("Success: Captured 10 screenshots in one second.")
else:
    print("Failed to capture 10 screenshots in one second.")
