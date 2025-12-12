# HEXT Text to ASCII Banner Generator

**Version:** 1.3.0
**Author:** K0NxT3D

## Overview
HEXT is a single-file Python3 Flask web application that converts text into ASCII banners using pyfiglet.
It provides a modern, dark hacker aesthetic UI and supports selecting from all installed pyfiglet fonts.

## Prerequisites
- Python 3.12+ (tested on Ubuntu 24 LTS / Raspberry Pi)
- pip3 installed

## Installation
1. Clone or download the HEXT repository.
2. Install dependencies:

pip3 install -r requirements.txt

## Running HEXT
python3 hext.py

The app will start on port 22800.
It will attempt to auto-open your default browser to http://127.0.0.1:22800/.
Accessible over LAN via http://<RPi_IP>:22800/.

## Usage

1. Enter the text you want to convert in the "Text" field.
2. Select the font from the dropdown menu.
3. Click Render to update the ASCII banner.

- Optional:
  - Copy button: copy the ASCII banner to clipboard.
  - Download button: save the banner as a .txt file.

## Notes
- Maximum text length: 300 characters.
- All pyfiglet fonts installed on the system are available in the dropdown.
- Designed to work on both desktop and mobile.

## ✨ Features

- ⚡ Web UI built with **Flask**
- 🔠 Over **400 pyfiglet fonts** available
- 🖥 Instant live preview
- 📋 Copy-to-clipboard support
- 📁 Downloadable `.txt` banners
- 🔄 API endpoint for automation
- 🌑 Custom dark UI with static-free typography
- 🖥 Automatic browser launch on start

---
