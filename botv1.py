import sys
import os
import time
import json
import websocket
from colorama import *


init(autoreset=True)



class PrickleBot:
    def __init__(self):
        with open("config.json", "r") as file:
          config_data = json.load(file)
          
        self.telegram_id = config_data['telegram_id']
        self.clicks = config_data['clicks']
        self.delay_click_in_ms = config_data['delay_click_in_ms']
        self.delay_empty_energy_in_second = config_data['delay_empty_energy_in_second']

        self.green = '\033[92m'
        self.white = '\033[97m'
        self.yellow = '\033[93m'
        self.red = '\033[91m'
        self.blue = '\033[94m'
        
        self.ws_url = "wss://swagerbyfalio.com/prick/ws"
        self.base_headers = [
          "User-Agent: Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
          "Origin: https://app.prick.lol",
        ]
        self.ws = None

    def log(self, message, type):
        year, mon, day, hour, minute, second, x, y, z = time.localtime()
        hour = str(hour).zfill(2)
        minute = str(minute).zfill(2)
        second = str(second).zfill(2)
        if type == "error":
            print(f"{self.red}|{hour}:{minute}:{second}| {message}")
        elif type == "info":
            print(f"{self.green}|{hour}:{minute}:{second}| {message}")
        elif type == "countdown":
            print(f"{self.blue}|{hour}:{minute}:{second}| {message}", end="\r")
            sys.stdout.flush()

    def countdown(self, time_arg):
        while time_arg:
            minute, second = divmod(time_arg, 60)
            hour, minute = divmod(minute, 60)
            hour = str(hour).zfill(2)
            minute = str(minute).zfill(2)
            second = str(second).zfill(2)
            self.log(f"Waiting until {hour}:{minute}:{second}", "countdown")
            time_arg -= 1
            time.sleep(1)

    def generate_time(self, count, delay_ms):
        timestamps = []

        for _ in range(count):
            current_time_ms = int(time.time() * 1000)
            timestamps.append(current_time_ms)
            time.sleep(delay_ms / 1000.0)

        return timestamps

    def connect_websocket(self):
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(self.ws_url, header=self.base_headers)
            self.log("WebSocket connection established", "info")
        except Exception as e:
            self.log(f"Error connecting to WebSocket: {str(e)}", "error")
            time.sleep(5)
            self.connect_websocket()

    def handle_message(self, message):
        try:
            res = json.loads(message)
            open(".http_request.log", "a").write(json.dumps(res) + "\n")
            return res
        except Exception as e:
            self.log(f"Error handling message: {str(e)}", "error")
            return None

    def check_energy(self):
        # Check energy before starting auto claim
        tap_data = {
            "action": "check_energy"
        }
        self.ws.send(json.dumps(tap_data))
        tap_result = self.ws.recv()
        tap_res = self.handle_message(tap_result)
        if tap_res and "action" in tap_res and tap_res["action"] == "user":
            data = tap_res["data"]
            return data
        else:
            self.log("Error checking energy", "error")
            return None

    def main(self):
        banner = f"""
           {self.red}Prickle Bot Auto Claim
           {self.blue}by: marylnrose
          """
        if "noclear" not in sys.argv:
          os.system("cls" if os.name == "nt" else "clear")
    
        print(banner)
        try:
            self.base_headers.append(f"Sec-Websocket-Protocol: {self.telegram_id}")
            self.connect_websocket()
            
            res = self.check_energy()
            if res is None:
                sys.exit()
            
            self.log(f"Current Energy: {res['energy']}", "info")

            username = res["username"]
            balance = res["balance"]
            energy = res["energy"]

            self.log(f"Logged in as: {username}", "info")
            self.log(f"Balance: {balance}", "info")
            print(f"-" * 70)

            if energy > 0:
                try:
                    while True:
                      # Generating 10 tap with 10ms delay
                        tap_data = {
                            "action": "tap",
                            "data": self.generate_time(self.clicks, self.delay_click_in_ms)
                        }
                        self.ws.send(json.dumps(tap_data))
                        
                        try:
                            while True:
                                tap_result = self.ws.recv()
                                tap_res = self.handle_message(tap_result)

                                if tap_res and "action" in tap_res:
                                    if tap_res["action"] == "result-tap":
                                        energy = tap_res["energy"]
                                        balance = tap_res["balance"]
                                        user_clicks = tap_res["userClicks"]

                                        self.log(f"Balance: {balance}", "info")
                                        self.log(f"User Clicks: {user_clicks}", "info")
                                        self.log(f"Energy Remains: {energy}", "info")

                                        # Check energy again
                                        if energy < 100:
                                            self.log("Energy is low. Waiting before continuing...", "info")
                                            self.countdown(self.delay_empty_energy_in_second)
                                            break
                                        else:
                                            self.log("Delay before continuing another action", "info")
                                            self.countdown(3)
                                            break
                                    elif tap_res["action"] == "energy_recovery":
                                        energy = tap_res["energy"]
                                        self.log(f"Energy recovered: {energy}", "info")
                                    else:
                                        self.log(f"Received unexpected action: {tap_res['action']}", "info")
                                else:
                                    self.log("Received invalid response", "error")
                        except KeyboardInterrupt:
                            print("Keyboard interrupt detected. Exiting...")
                            break
                except Exception as e:
                    self.log(f"Error: {str(e)}", "error")
                    open(".http_request.log", "a").write(str(e) + "\n")
            else:
                self.log("Empty energy. Waiting for energy to be fully restored", "info")
                self.countdown(self.delay_empty_energy_in_second)
        except Exception as e:
            self.log(f"Unhandled error: {str(e)}", "error")

if __name__ == "__main__":
    try:
      app = PrickleBot()
      app.main()
    except KeyboardInterrupt:
        sys.exit()
      
