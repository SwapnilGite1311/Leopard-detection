from twilio.rest import Client
from datetime import datetime
import threading

# â”€â”€â”€ TWILIO CONFIGURATION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ACCOUNT_SID = ""
AUTH_TOKEN = ""  # Replace with actual token
MESSAGING_SERVICE_SID = ""
OWNER_NUMBER = "+919028219138"  # Field owner's number

# â”€â”€â”€ INTERNAL SMS FUNCTION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def _send_sms_sync(confidence, timestamp):
    """
    Internal function that actually sends SMS
    This runs in a background thread
    """
    message_body = f"""ðŸš¨ LEOPARD ALERT!

Time: {timestamp}
Confidence: {confidence:.0%}
Location: Sugarcane Field

Take immediate action!"""
    
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        
        message = client.messages.create(
            messaging_service_sid=MESSAGING_SERVICE_SID,
            body=message_body,
            to=OWNER_NUMBER
        )
        
        print(f"   âœ… SMS delivered! SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"   âŒ SMS failed: {e}")
        return False

# â”€â”€â”€ PUBLIC ALERT FUNCTION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def send_sms_alert(confidence, timestamp=None):
    """
    Send SMS alert in background thread (non-blocking)
    
    Args:
        confidence: Detection confidence (0.0 to 1.0)
        timestamp: Optional timestamp string
    
    Returns:
        True (always - SMS sends in background)
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Launch SMS in background thread
    # daemon=True means thread closes when main program exits
    thread = threading.Thread(
        target=_send_sms_sync,
        args=(confidence, timestamp),
        daemon=True
    )
    thread.start()
    
    print("   ðŸ“± SMS queued (sending in background)...")
    return True  # Returns immediately

# â”€â”€â”€ TEST FUNCTION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if __name__ == "__main__":
    print("=" * 50)
    print("Testing SMS Alert System")
    print("=" * 50)
    
    print("\nðŸ”„ Sending test SMS...")
    send_sms_alert(confidence=0.85)
    
    print("âœ… SMS queued!")
    print("   Check your phone in 5-10 seconds...\n")
    
    # Keep script alive to let thread finish
    import time
    print("â³ Waiting for SMS to send...")
    time.sleep(15)
    print("\nâœ… Test complete!")
