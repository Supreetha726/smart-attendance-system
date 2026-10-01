import os
import cv2
import pickle
import torch
import numpy as np
from facenet_pytorch import InceptionResnetV1

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def get_embedding(face_img):
    face_img = cv2.resize(face_img, (160, 160))
    face_img = face_img / 255.0
    face_img = (face_img - 0.5) / 0.5

    face_img = torch.tensor(face_img).permute(2,0,1).float().unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = model(face_img)

    return embedding.cpu().numpy()[0]

known_embeddings = []
known_names = []

folder = "known_faces"

for file in os.listdir(folder):
    path = os.path.join(folder, file)
    img = cv2.imread(path)

    if img is None:
        continue

    emb = get_embedding(img)

    known_embeddings.append(emb)
    known_names.append(os.path.splitext(file)[0])

data = {
    "embeddings": np.array(known_embeddings),
    "names": known_names
}

with open("embeddings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Embeddings saved successfully!")