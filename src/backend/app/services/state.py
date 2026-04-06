status = {
    "running": False,
    "stage": None,
    "progress": None,
    "done": False,
    "error": None
}

def reset_status():
    # resets status
    global status
    status["running"] = False
    status["stage"] = None
    status["progress"] = None
    status["done"] = False
    status["error"] = None