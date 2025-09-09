import os
from google.cloud import vision

class ProductIdentifier:
    def __init__(self):
        # Correct path to your JSON key
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\PC\Web-Application-for-Product-Price-Comparison-Across-E-Commerce-Sites_August_2025\google-vision-key.json"
        self.client = vision.ImageAnnotatorClient()

    def identify_product(self, image_path):
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations
        if labels:
            return labels[0].description
        return "No product detected"
