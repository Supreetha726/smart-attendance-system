import cv2
import numpy as np
import pickle
import torch
import sys
from facenet_pytorch import InceptionResnetV1, MTCNN

from database import mark_attendance
from alerts import send_email

# -------------------- Setup --------------------
device = 'cuda' if torch.cuda.is_available() else 'cpu'

mtcnn = MTCNN(keep_all=True, device=device)

facenet = InceptionResnetV1(
    pretrained='vggface2'
).eval().to(device)

# -------------------- Load Embeddings --------------------
with open("embeddings.pkl", "rb") as f:
    data = pickle.load(f)

known_embeddings = data["embeddings"]
known_names = data["names"]

# -------------------- Webcam --------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot access webcam")
    sys.exit()

# -------------------- Duplicate Prevention --------------------
marked_once = set()

# -------------------- Threshold --------------------
THRESHOLD = 0.95

print("🚀 Smart Attendance Running... Press Q or ESC to quit")

# -------------------- Main Loop --------------------
try:

    while True:

        ret, frame = cap.read()

        if not ret:
            print("❌ Camera error")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        boxes, _ = mtcnn.detect(rgb_frame)

        if boxes is not None:

            for box in boxes:

                x1, y1, x2, y2 = map(int, box)

                # Crop face
                face = rgb_frame[y1:y2, x1:x2]

                if face.size == 0:
                    continue

                # -------------------- Preprocess --------------------
                face = cv2.resize(face, (160, 160))

                face = face / 255.0
                face = (face - 0.5) / 0.5

                face_tensor = torch.tensor(face)\
                    .permute(2, 0, 1)\
                    .float()\
                    .unsqueeze(0)\
                    .to(device)

                # -------------------- Generate Embedding --------------------
                with torch.no_grad():
                    emb = facenet(face_tensor).cpu().numpy()[0]

                # -------------------- Compare --------------------
                distances = np.linalg.norm(
                    known_embeddings - emb,
                    axis=1
                )

                min_dist = np.min(distances)

                # -------------------- Recognition --------------------
                if min_dist < THRESHOLD:

                    name = known_names[
                        np.argmin(distances)
                    ].strip()

                    # Attendance only once
                    if name not in marked_once:

                        if mark_attendance(name):
                            send_email(name)

                        marked_once.add(name)

                    # -------------------- Draw --------------------
                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    # Show Name
                    cv2.putText(
                        frame,
                        f"{name}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                # 🔥 Ignore unknown faces completely
                # No Unknown label displayed

        cv2.imshow("Smart Attendance System", frame)

        # -------------------- Exit --------------------
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == 27:
            print("👋 Exiting...")
            break

except KeyboardInterrupt:
    print("🛑 Stopped manually")

finally:

    print("🔻 Releasing camera...")

    cap.release()

    cv2.destroyAllWindows()

    sys.exit(0)