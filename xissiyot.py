import cv2
import numpy as np
from deepface import DeepFace
import time
CAMERA_ID = 0        
FONT = cv2.FONT_HERSHEY_SIMPLEX
ANALYZE_EVERY_N = 15   
EMOTION_COLORS = {
    "happy":    (0, 220, 120),   # yashil
    "sad":      (200, 80, 50),   # ko'k-qizil
    "angry":    (0, 50, 220),    # qizil
    "surprise": (0, 200, 220),  # sariq
    "fear":     (160, 0, 200),   # binafsha
    "disgust":  (0, 160, 80),    # to'q yashil
    "neutral":  (180, 180, 180), # kulrang
}
EMOTION_UZ = {
    "happy":    "Xursand 😊",
    "sad":      "G'amgin 😢",
    "angry":    "G'azablangan 😡",
    "surprise": "Hayron 😲",
    "fear":     "Qo'rqinchli 😨",
    "disgust":  "Nafratlanish 🤢",
    "neutral":  "Neutral 😐"
}
def draw_info_bar(frame, emotion, confidence, fps):
    """Ekranning pastki qismida ma'lumot paneli"""
    h, w = frame.shape[:2]
    bar_h = 60
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - bar_h), (w, h), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    label = EMOTION_UZ.get(emotion, emotion)
    color = EMOTION_COLORS.get(emotion, (200, 200, 200))
    cv2.putText(frame, label, (12, h - 30),
                FONT, 0.75, color, 2, cv2.LINE_AA)
    cv2.putText(frame, f"Aniqlik: {confidence:.0f}% | FPS: {fps:.0f}",
                (12, h - 10), FONT, 0.45, (180, 180, 180), 1, cv2.LINE_AA)
def draw_emotion_bars(frame, scores: dict):
    """O'ng tomonda hissiyot grafigi (gorizontal barlar)"""
    h, w = frame.shape[:2]
    bar_w_max = 130
    x0 = w - bar_w_max - 12
    y0 = 20
    row_h = 22
    for i, (em, sc) in enumerate(sorted(scores.items(),
                                       key=lambda x: x[1], reverse=True)):
        y = y0 + i * row_h
        color = EMOTION_COLORS.get(em, (200, 200, 200))
        filled = int(bar_w_max * sc / 100)
        cv2.rectangle(frame, (x0, y), (x0 + bar_w_max, y + 14),
                      (60, 60, 60), -1)
        if filled > 0:
            cv2.rectangle(frame, (x0, y), (x0 + filled, y + 14),
                          color, -1)
        short = em[:3].upper()
        cv2.putText(frame, f"{short} {sc:4.0f}%",
                    (x0 - 72, y + 11), FONT, 0.38,
                    (220, 220, 220), 1, cv2.LINE_AA)
def main():
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        print("Kamera topilmadi! CAMERA_ID ni tekshiring.")
        return
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    current_emotion = "neutral"
    current_scores = {e: 0 for e in EMOTION_COLORS}
    current_confidence = 0.0
    frame_count = 0
    prev_time = time.time()
    print("Dastur ishga tushdi. Chiqish uchun 'q' bosing.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)       
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80)
        )
        if frame_count % ANALYZE_EVERY_N == 0 and len(faces) > 0:
            try:
                result = DeepFace.analyze(
                    frame, actions=["emotion"],
                    enforce_detection=False, silent=True
                )
                r = result[0] if isinstance(result, list) else result
                current_emotion = r["dominant_emotion"]
                current_scores = r["emotion"]       
                current_confidence = current_scores.get(current_emotion, 0)
            except Exception:
                pass
        for (x, y, fw, fh) in faces:
            color = EMOTION_COLORS.get(current_emotion, (200, 200, 200))
            cv2.rectangle(frame, (x, y), (x + fw, y + fh), color, 2)
            cv2.putText(frame, EMOTION_UZ.get(current_emotion, ""),
                        (x, y - 8), FONT, 0.55, color, 1, cv2.LINE_AA)
        now = time.time()
        fps = 1 / (now - prev_time + 1e-9)
        prev_time = now
        draw_info_bar(frame, current_emotion, current_confidence, fps)
        draw_emotion_bars(frame, current_scores)
        h_fr = frame.shape[0]
        cv2.putText(frame, "Computer Vision - Hissiyot aniqlovchi",
                    (10, 22), FONT, 0.55, (220, 220, 220), 1, cv2.LINE_AA)
        cv2.putText(frame, "Roboschool | 14-16 yosh",
                    (10, 42), FONT, 0.42, (140, 140, 140), 1, cv2.LINE_AA)
        cv2.imshow("Hissiyot Aniqlovchi", frame)
        frame_count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Dastur yopildi.")
if __name__ == "__main__":
    main()
import cv2
import numpy as np
from deepface import DeepFace
import time
CAMERA_ID = 0        
FONT = cv2.FONT_HERSHEY_SIMPLEX
ANALYZE_EVERY_N = 15  
EMOTION_COLORS = {
    "happy":    (0, 220, 120),   # yashil
    "sad":      (200, 80, 50),   # ko'k-qizil
    "angry":    (0, 50, 220),    # qizil
    "surprise": (0, 200, 220),  # sariq
    "fear":     (160, 0, 200),   # binafsha
    "disgust":  (0, 160, 80),    # to'q yashil
    "neutral":  (180, 180, 180), # kulrang
}
EMOTION_UZ = {
    "happy":    "Xursand 😊",
    "sad":      "G'amgin 😢",
    "angry":    "G'azablangan 😡",
    "surprise": "Hayron 😲",
    "fear":     "Qo'rqinchli 😨",
    "disgust":  "Nafratlanish 🤢",
    "neutral":  "Neutral 😐"
}
def draw_info_bar(frame, emotion, confidence, fps):
    h, w = frame.shape[:2]
    bar_h = 60
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - bar_h), (w, h), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    label = EMOTION_UZ.get(emotion, emotion)
    color = EMOTION_COLORS.get(emotion, (200, 200, 200))
    cv2.putText(frame, label, (12, h - 30),
                FONT, 0.75, color, 2, cv2.LINE_AA)
    cv2.putText(frame, f"Aniqlik: {confidence:.0f}% | FPS: {fps:.0f}",
                (12, h - 10), FONT, 0.45, (180, 180, 180), 1, cv2.LINE_AA)
    