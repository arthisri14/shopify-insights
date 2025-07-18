import uvicorn
import webbrowser
import time

if __name__ == "__main__":
    def open_browser():
        time.sleep(1)  
        webbrowser.open_new("http://127.0.0.1:8000/docs")

    import threading
    threading.Thread(target=open_browser).start()

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
