import cv2
from ultralytics import YOLO
import time
from datetime import datetime
import os
import sys

# Add parent directory to path for alert import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.alert import send_sms_alert

# ─── CONFIGURATION ────────────────────────────────────────────────
DROIDCAM_URL = "http://10.215.41.171:4747/video"  # Your DroidCam IP
MODEL_PATH = "../models/best.pt"                    # Our trained model
CONFIDENCE_THRESHOLD = 0.6                          # Higher = fewer false positives
SAVE_DIR = "../detections"                          # Where to save detected images
COOLDOWN_SECONDS = 30                               # Don't spam alerts
PROCESS_EVERY_N_FRAMES = 2                          # Process every 2nd frame (for speed)

# ─── SETUP ────────────────────────────────────────────────────────
# Create save directory
os.makedirs(SAVE_DIR, exist_ok=True)

print("=" * 60)
print("🐆 LEOPARD DETECTION SYSTEM")
print("=" * 60)

# Load our trained model
print("\n🔄 Loading trained model...")
try:
    model = YOLO(MODEL_PATH)
    print(f"✅ Model loaded: {MODEL_PATH}")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    exit()

# Connect to DroidCam
print(f"\n🔄 Connecting to DroidCam at {DROIDCAM_URL}...")
cap = cv2.VideoCapture(DROIDCAM_URL)

if not cap.isOpened():
    print(f"❌ ERROR: Cannot connect to DroidCam")
    print(f"   • Make sure DroidCam app is running on your phone")
    print(f"   • Check phone and laptop are on same WiFi")
    print(f"   • Verify URL: {DROIDCAM_URL}")
    exit()

print("✅ Connected to DroidCam!")

# Display settings
print("\n" + "─" * 60)
print("⚙️  SETTINGS:")
print(f"   • Confidence Threshold: {CONFIDENCE_THRESHOLD}")
print(f"   • Alert Cooldown: {COOLDOWN_SECONDS} seconds")
print(f"   • Processing: Every {PROCESS_EVERY_N_FRAMES} frames")
print(f"   • Save Location: {SAVE_DIR}")
print("─" * 60)

print("\n🚀 Starting detection...")
print("   Press 'Q' to quit\n")

# ─── DETECTION LOOP ───────────────────────────────────────────────
last_alert_time = 0
frame_count = 0
detection_count = 0
start_time = time.time()

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("⚠️  Lost connection to DroidCam. Reconnecting in 2 seconds...")
            time.sleep(2)
            cap = cv2.VideoCapture(DROIDCAM_URL)
            continue
        
        frame_count += 1
        
        # Process only every Nth frame for speed
        if frame_count % PROCESS_EVERY_N_FRAMES != 0:
            # Still show the frame but don't run detection
            cv2.imshow('Leopard Detection - Press Q to Quit', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        
        # Run detection
        results = model(frame, verbose=False)
        
        # Check for leopard detections
        leopard_detected = False
        max_confidence = 0
        best_box = None
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                confidence = box.conf[0].item()
                class_id = int(box.cls[0].item())
                
                if confidence > CONFIDENCE_THRESHOLD:
                    leopard_detected = True
                    if confidence > max_confidence:
                        max_confidence = confidence
                        best_box = box
        
        # Handle detection
        if leopard_detected:
            current_time = time.time()
            detection_count += 1
            
            # Draw detection on frame
            annotated_frame = results[0].plot()
            
            # Check cooldown before alerting
            if current_time - last_alert_time > COOLDOWN_SECONDS:
                print("\n" + "=" * 60)
                print(f"🚨 LEOPARD DETECTED!")
                print(f"   Confidence: {max_confidence:.1%}")
                print(f"   Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
                
                # Save image with detection
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(SAVE_DIR, f"leopard_{timestamp}_conf{max_confidence:.2f}.jpg")
                cv2.imwrite(filename, annotated_frame)
                print(f"   💾 Saved: {filename}")
                
                # Send SMS alert
                print("   📱 Sending SMS alert...")
                try:
                    sms_sent = send_sms_alert(
                        confidence=max_confidence,
                        timestamp=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    )
                    
                    if sms_sent:
                        print("   ✅ SMS sent successfully!")
                    else:
                        print("   ⚠️  SMS failed to send")
                except Exception as e:
                    print(f"   ❌ SMS error: {e}")
                
                print(f"   ⏸️  Alert cooldown: {COOLDOWN_SECONDS}s")
                print("=" * 60 + "\n")
                
                last_alert_time = current_time
            else:
                # Detection but still in cooldown
                time_remaining = int(COOLDOWN_SECONDS - (current_time - last_alert_time))
                print(f"🐆 Leopard detected ({max_confidence:.1%}) - Cooldown: {time_remaining}s remaining")
            
            # Show annotated frame
            cv2.imshow('Leopard Detection - Press Q to Quit', annotated_frame)
        else:
            # No detection - show regular frame
            cv2.imshow('Leopard Detection - Press Q to Quit', frame)
        
        # Show stats every 60 frames (every ~2 seconds)
        if frame_count % 60 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            print(f"📊 Stats: {frame_count} frames | {detection_count} detections | {fps:.1f} FPS")
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n\n⚠️  Interrupted by user")

finally:
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    # Final stats
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print("✅ DETECTION STOPPED")
    print("=" * 60)
    print(f"📊 Session Statistics:")
    print(f"   • Total frames: {frame_count}")
    print(f"   • Detections: {detection_count}")
    print(f"   • Runtime: {elapsed/60:.1f} minutes")
    print(f"   • Average FPS: {frame_count/elapsed:.1f}")
    print(f"   • Images saved: Check {SAVE_DIR}/")
    print("=" * 60)