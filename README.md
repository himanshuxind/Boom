
# 💥 Boom


## 🌟 About

**Boom** is a terminal-based Python project created by **Himanshu** for call-based automation. It is built around a simple and interactive command-line experience, allowing users to interact with the application through a structured terminal interface rather than complex commands. The project is developed under the **HimaXcore** brand.

## ✨ What Boom Offers

### 🎨 Clean Terminal Interface
Boom focuses heavily on providing a clean and user-friendly terminal experience.
*   Simple menu-based navigation
*   Colored and styled output using `colorama`
*   Animated status messages and progress bars
*   Clear user prompts
*   ASCII-style branding with `pyfiglet`

### ⚙️ Automation Modes
The project provides several configurable automation workflows for orchestrating calls via the Telz API.
*   **Single Call**: Place a single call to a target number.
*   **Bulk Call**: Process a list of numbers from user input.
*   **Loop Call**: Repeatedly call a single number with a configurable delay.

### 📊 Statistics
Boom keeps track of useful runtime information for each session.
*   Total calls initiated
*   Successful and failed calls
*   Total API requests
*   Session duration

### 🐞 Debugging
Boom includes a debugging mode for development and testing. When enabled, it provides detailed server responses and error tracebacks to help identify problems.

### 🎛️ Settings
The application provides configurable settings to adjust runtime behavior without modifying the source code.
*   **Wait Time**: Adjust the rate-limiting cooldown period between calls to the same number.
*   **Debug Mode**: Toggle verbose debugging information.

## 🧰 Requirements
Before installing Boom, you need:
*   Python 3.x
*   Git
*   An active internet connection

The project relies on the following Python libraries:
```text
requests
colorama
pyfiglet
```

## 🚀 Installation

### Windows · Linux · macOS

1.  Clone the repository:
    ```bash
    git clone https://github.com/himanshuxind/Boom.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd Boom
    ```
3.  Install the required dependencies:
    ```bash
    pip install requests colorama pyfiglet
    ```
4.  Start the application:
    ```bash
    python main.py
    ```

### Termux

1.  Install Python and Git:
    ```bash
    pkg update -y
    pkg install python git -y
    ```
2.  Clone the repository:
    ```bash
    git clone https://github.com/himanshuxind/Boom.git
    ```
3.  Enter the project directory:
    ```bash
    cd Boom
    ```
4.  Install dependencies:
    ```bash
    pip install requests colorama pyfiglet
    ```
5.  Run Boom:
    ```bash
    python main.py
    ```

## ▶️ Using Boom
After launching the application, you will be presented with the main terminal interface, the **HimaXcore Console**.

The general flow is:
1.  **Launch** the script: `python main.py`
2.  **Choose an option** from the menu (e.g., `1` for Single Call).
3.  **Provide the required input** (e.g., a target phone number).
4.  **Boom validates** the input and initiates the pre-call sequence.
5.  The selected **operation runs**.
6.  **Results and statistics** are displayed.

The available menu options are:
*   **[1] Start Single Call**: Initiates one call to a specified number.
*   **[2] Start Bulk Call (List)**: Calls a list of numbers entered by the user.
*   **[3] Loop Call on One Number**: Repeatedly calls one number with a set delay.
*   **[4] Change Settings**: Modify wait time and debug mode.
*   **[5] Show Statistics**: Display statistics for the current session.
*   **[6] Exit**: Close the application.

## 🔧 Troubleshooting

### Python not found?
If the `python` command doesn't work, try using `python3`:
```bash
python3 main.py
```

### Missing module?
If you see an `ImportError`, reinstall the dependencies to ensure they are properly installed.
```bash
pip install requests colorama pyfiglet
```

### Git not found?
You must install Git on your system before you can clone the repository. Please refer to the official Git documentation for installation instructions for your operating system.

## 🛡️ Responsible Use
Boom is intended for educational purposes, personal experimentation, and authorized testing only.
*   Do not use this project for harassment, sending unwanted communications, or any form of service disruption.
*   Only use this tool on numbers and services for which you have explicit permission to test.
*   You are solely responsible for your actions and for complying with all applicable laws and terms of service. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

## 👨‍💻 Creator
<p align="center">
  <strong>Himanshu</strong>
  <br>
  Creator & Developer
  <br>
  <br>
  <strong>HimaXcore</strong>
  <br>
  Project Brand
</p>
