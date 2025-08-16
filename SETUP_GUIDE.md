# FinSightAI Setup Guide

This guide will help you set up and run FinSightAI locally for development or demo purposes.

## Prerequisites

- Node.js (v16+ recommended)
- Python 3.8+
- Git

## 1. Clone the Repository

```bash
git clone https://github.com/PulastTiwari/FinSight.git
cd FinSight
```

## 2. Backend Setup (Flask)

1. Go to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv ../.venv
   source ../.venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   python app.py
   ```
   The backend runs at `http://localhost:5002`.

## 3. Frontend Setup (React)

1. Open a new terminal and go to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend server:
   ```bash
   npm start
   ```
   The frontend runs at `http://localhost:3000`.

## 4. Usage

- Open your browser at `http://localhost:3000`
- Use the dashboard, analytics, and AI assistant features
- Test with sample transactions for anomaly detection and categorization

## 5. Troubleshooting

- Ensure both backend and frontend servers are running
- If ports are busy, change them in the respective config files
- For Python errors, check your virtual environment and package versions
- For Node errors, delete `node_modules` and run `npm install` again

## 6. Additional Resources

- [README.md](./README.md) for project overview
- [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines
- [LICENSE](./LICENSE) for license details

---

For questions or help, open an issue on GitHub!
