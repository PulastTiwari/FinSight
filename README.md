# FinSightAI: Smart Financial Operations Platform

FinSightAI is an open-source platform for advanced financial operations, providing AI-driven analytics, anomaly detection, and a modern interactive dashboard. It is suitable for hackathons, enterprise demonstrations, and full-stack AI development.

## Key Features

- **AI Chatbot Assistant**: Natural language financial advisor for transaction queries and insights
- **Smart Insights Dashboard**: Automated recommendations and analytics based on financial data
- **Modern UI/UX**: Built with Ant Design and Framer Motion, supporting dark and light modes
- **Advanced Analytics**: Interactive charts and data visualizations using Recharts
- **Real-time Notifications**: User feedback via toast notifications
- **Anomaly Detection**: Machine learning-based transaction analysis for outlier detection

## Architecture

- **Backend**: Flask (Python), pandas, scikit-learn
- **Frontend**: React (JavaScript), Ant Design, Framer Motion, Recharts

## Technical Overview

**Transaction Categorization:**
Uses TF-IDF vectorization and a Random Forest classifier to predict transaction categories.

**Anomaly Detection:**
Employs Isolation Forest to identify anomalous transactions.

**Full-Stack Workflow:**
The React frontend communicates with the Flask backend via RESTful APIs, sending transaction data and receiving predictions and analytics for real-time display.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/PulastTiwari/FinSight.git
cd FinSight
```

### 2. Backend Setup (Python/Flask)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a Python virtual environment:
   ```bash
   python3 -m venv ../.venv
   source ../.venv/bin/activate
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5002`.

### 3. Frontend Setup (React)

1. Open a new terminal and navigate to the frontend directory:
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
   The frontend will be available at `http://localhost:3000`.

### 4. Usage

- Access the dashboard at `http://localhost:3000`.
- Use the analytics and charting features.
- Interact with the AI Assistant for financial queries.
- Analyze transactions for categorization and anomaly detection.

### 5. Example Transactions

Sample inputs for testing in the Analyze tab:

- Description: `HUGE EQUIPMENT PURCHASE`, Amount: `25000` (expected: anomaly)
- Description: `MONTHLY SALARY PAYMENT`, Amount: `3500` (expected: normal)
- Description: `ELECTRIC COMPANY BILL`, Amount: `150` (expected: utilities)

## Contributing

Contributions are welcome. Please refer to `CONTRIBUTING.md` for guidelines on submitting features, bug fixes, or documentation improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Concepts Explained

**Categorization:**
We use TF-IDF (text feature extraction) and a Random Forest classifier to predict the category of a transaction based on its description and amount.

**Anomaly Detection:**
We use Isolation Forest, a popular ML algorithm, to flag transactions that are unusual compared to typical spending patterns.

**Full-Stack Workflow:**
Frontend (React) sends transaction data to the backend (Flask), which returns predictions and analytics. The frontend displays charts and results in real time.

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/PulastTiwari/FinSight.git
cd FinSight
```

### 2. Set Up the Backend (Python)

1. Go to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment (recommended):
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
   The backend will run at `http://localhost:5000`.

### 3. Set Up the Frontend (React)

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
   The frontend will run at `http://localhost:3000` (or another port if 3000 is busy).

### 4. Try It Out!

- Open your browser and go to `http://localhost:3000`.
- Use the dashboard to view analytics and charts.
- Use the "Analyze Transaction" tab to test with your own transaction descriptions and amounts.

### 5. Example Transactions

Try these in the Analyze tab:

- Description: `HUGE EQUIPMENT PURCHASE`, Amount: `25000` (should be flagged as anomaly)
- Description: `MONTHLY SALARY PAYMENT`, Amount: `3500` (should be normal)
- Description: `ELECTRIC COMPANY BILL`, Amount: `150` (should be utilities)

## Contributing

We welcome contributions! If you want to add features, fix bugs, or improve documentation:

- Fork the repo and create a branch
- Make your changes and submit a pull request
- For big changes, open an issue first to discuss ideas

## License

This project is licensed under the MIT License. See the LICENSE file for details.
