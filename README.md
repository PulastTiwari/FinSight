# Financial Transaction Analyzer

# Financial Transaction Analyzer

This MVP uses machine learning to categorize financial transactions and detect anomalies in real time. It features a Flask backend and a React + Material-UI frontend.

## Features

- ML-powered categorization (TF-IDF + Random Forest)
- Real-time anomaly detection (Isolation Forest)
- Interactive dashboard with charts and analytics
- AI workflow automation with confidence scoring

## Getting Started

### Backend

1. Create and activate a Python virtual environment:
   ```bash
   cd backend
   python3 -m venv ../.venv
   source ../.venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend:
   ```bash
   python app.py
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the frontend:
   ```bash
   npm start
   ```

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
