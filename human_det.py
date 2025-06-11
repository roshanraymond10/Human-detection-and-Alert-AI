import cv2
import mediapipe as mp
import smtplib
import ssl
import winsound
from email.message import EmailMessage


SENDER_EMAIL = "roshanraymond10@gmail.com"
APP_PASSWORD = "lzob humb oqdi ctco"
RECEIVER_EMAIL = "roselittania@gmail.com"

ALERT_IMAGE = "alert_image.jpg"


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)
alert_sent = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)


    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if not alert_sent:
            print("[INFO] Human detected. Triggering alert...")


            cv2.imwrite(ALERT_IMAGE, frame)


            winsound.Beep(1000, 1000)  # frequency=1000Hz, duration=1000ms

            # Prepare the email
            msg = EmailMessage()
            msg['Subject'] = '🚨 Human Detected Alert'
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL
            msg.set_content('A human has been detected. Please see the attached image.')

            with open(ALERT_IMAGE, 'rb') as f:
                img_data = f.read()
                msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=ALERT_IMAGE)

            # Send the email
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                    server.login(SENDER_EMAIL, APP_PASSWORD)
                    server.send_message(msg)
                print("[INFO] Email sent successfully.")
            except Exception as e:
                print(f"[ERROR] Failed to send email: {e}")

            alert_sent = True 

    # Show frame in a window
    cv2.imshow('Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
