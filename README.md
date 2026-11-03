# Matrix COSEC Manager

A modular Python utility to connect, monitor, and interact with **Matrix COSEC** biometric access control and time-attendance terminals (e.g., Matrix COSEC VEGA, COSEC DOOR).

---

## Features

- **Automated Device Probing**: Checks HTTP/HTTPS connectivity and validates terminal response.
- **Device Metadata Extraction**: Fetches hardware model, firmware status, and assigned door identifiers.
- **Secure Architecture**: All local network configurations (IPs, credentials, ports) are kept private via environment variables (`.env`).
- **Cryptographic Handshake Support**: Interacts with the Matrix CGI endpoint (`/cgi-bin/submit`) and negotiates temporary AES keys for secure authentication.

---

## Project Structure

```text
matrix-cosec-manager/
├── .env.example          # Environment variables template
├── .gitignore            # Git exclusion rules (protects credentials & logs)
├── config.py             # Configuration loader
├── matrix_client.py      # Core Matrix COSEC API client
├── main.py               # CLI entry point
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Getting Started

### 1. Prerequisites

- Python 3.8 or later
- Ethernet connection to the terminal or local network access to the device

### 2. Installation

Clone this repository and install the dependencies:

```bash
git clone https://github.com/prinspatel8055/matrix-cosec-manager.git
cd matrix-cosec-manager
pip install -r requirements.txt
```

### 3. Configuration

Copy `.env.example` to `.env` and fill in your device's network details:

```bash
cp .env.example .env
```

Edit `.env`:

```env
MATRIX_DEVICE_IP=192.168.1.20
MATRIX_DEVICE_PORT=80
MATRIX_ADMIN_PIN=1234
REQUEST_TIMEOUT_SECONDS=5
```

> **Security Note:** The `.env` file is excluded in `.gitignore` to ensure device credentials and private IP addresses are never exposed to remote repositories.

---

### 4. Usage

Run the connection test and device inspection tool:

```bash
python main.py
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
