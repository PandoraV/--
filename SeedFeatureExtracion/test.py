from ultralytics import YOLO

# Load model
model = YOLO('best_eye_crack.pt')

# file_path = 

# Run inference
# results = model('test_images/seed/seed_1.jpg')
results = model('test_images/cr_ey/3.png')

# Print image.jpg results in JSON format
print(results[0].tojson())