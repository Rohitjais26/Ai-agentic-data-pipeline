
def next_state(current_state, action_status):
    """
    Current state aur last action ke basis par
    next state decide karta hai.
    """

    if current_state == "start" and action_status == "sent":   #message have been sent , now wait for reply
        return "waiting_response"
    
    if current_state == "waiting_response" and action_status == "answered":
        return "engaged"


    if current_state == "waiting_response" and action_status == "missed":
        return "retry_later"


    return current_state