# Flask Chatbot

A simple chatbot built with Flask, allowing user interactions and storing conversation history using server-side sessions.

# How the Chatbot Works
When you type a message and click "Send," the message is sent to the server.

The server processes the message, checks for predefined responses, and returns the bot's reply.

Both the user's message and the bot's reply are stored in the session for persistence across interactions.

## Requirements

- Python 3.x
- pip (Python's package installer)

## Installation Steps

### 1. Clone the Repository

Clone this repository to your local machine:

```
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```
### 2. In bash environment run this which will setup everything automatically.
```
sh install.sh
```
### 3. To start the Flask app, use the following command:
```
python app.py
```
### 4. Open the Chatbot in Your Browser
```
http://127.0.0.1:5000
```
### 5. This project is licensed under the MIT License
### 6. Common issues while project setup
##### A: Failed building wheel for llama-cpp-python
CMake Error: CMAKE_C_COMPILER not set, after EnableLanguage
      CMake Error: CMAKE_CXX_COMPILER not set, after EnableLanguage
      -- Configuring incomplete, errors occurred!
      CMake configuration failed
      [end of output]
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for llama-cpp-python
```
Solution:
1. Install Visual Studio Build Tools (Required)
Download Visual Studio 2022 Build Tools.

Run the installer and select:

"Desktop development with C++" (required for nmake and MSVC compiler).

Ensure "MSVC (Microsoft C++ Compiler)" and "Windows SDK" are checked.

Click Install.
```