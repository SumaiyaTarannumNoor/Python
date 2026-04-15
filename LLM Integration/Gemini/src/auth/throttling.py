import time
from collections import defaultdict
from fastapi import HTTPException, status

# For authenticated users
AUTH_RATE_LIMIT = 5
AUTH_TIME_WINDOW_SECONDS = 60

# For unauthenticated "global" users
GLOBAL_RATE_LIMIT = 3
GLOBAL_TIME_WINDOW_SECONDS = 60

user_requests = defaultdict(list)

def apply_rate_limit(user_id: str):
    current_time = time.time()
    rate_limit = GLOBAL_RATE_LIMIT
    time_window = GLOBAL_TIME_WINDOW_SECONDS

    #Filter out requests older than the time window
    user_requests[user_id] = [
        t for t in user_requests[user_id] if t > current_time - time_window 
    ]
    
    if len(user_requests[user_id]) >= rate_limit:
        raise HTTPException(
            status_code = status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )

    user_requests[user_id].append(current_time)
    return True
