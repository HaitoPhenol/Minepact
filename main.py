from chat import single_chat_request
import time

if __name__ == "__main__":
    while True:
        # use chat module's single_chat_request function to send a chat request to theseek api
        single_chat_request()
        time.sleep(3)
        print("\n"*5)
