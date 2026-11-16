import torch
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from torchvision.models import ResNet18_Weights, resnet18

# Load a model already trained on ImageNet (1000 classes). Done once, when the server starts.
weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights).eval()
preprocess = weights.transforms()  # resize, crop, normalize: same steps used in training
labels = weights.meta["categories"]

app = FastAPI(title="Image Classifier API")

# Side note: lets the web page (port 5500) call this API (port 8000).
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])



@app.post("/predict")
def predict(file: UploadFile):
    # Don't trust the file name or type the client sends: try to open it as an image
    try:
        image = Image.open(file.file).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Please upload an image")

    # Preprocess the image and add a batch dimension: [3, 224, 224] -> [1, 3, 224, 224]
    batch = preprocess(image).unsqueeze(0)

    # Run inference without tracking gradients (saves memory and speeds up prediction)
    with torch.no_grad():
        probabilities = model(batch).softmax(dim=1)[0]

    # Get the highest probability prediction
    confidence, index = probabilities.max(dim=0)

    return {
        "label": labels[index.item()],
        "confidence": round(confidence.item(), 4),
    }
