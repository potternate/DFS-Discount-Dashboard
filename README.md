# DFS Discount Dashboard

This project is a **DFS Discount Dashboard** that collects and processes DFS player prop discount data, uploading it to Google BigQuery. The data is then connected to **Looker**, where users can interact with a dashboard that visualizes the discounts and betting lines.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Data Flow](#data-flow)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [License](#license)

## Features
- Collects DFS player prop discount data.
- Processes and uploads data to BigQuery.
- Connected to a Looker dashboard for easy data visualization and analysis.
- Filterable by date, player, sport, discount percentage, and other metrics.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/potternate/dfs-discount-dashboard.git
    cd dfs-discount-dashboard
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the project root with your environment variables (e.g., Google Cloud credentials, BigQuery credentials, etc.).

## Data Flow

1. **Data Collection**: The main application script (`main.py`) collects DFS player prop discount data from various sources (e.g., APIs or CSV files).
2. **BigQuery Integration**: The collected data is processed and uploaded to **Google BigQuery**.
3. **Looker Dashboard**: The data in BigQuery is connected to **Looker**, where it is visualized in an interactive dashboard. The dashboard is accessible at (https://lookerstudio.google.com/s/kRaXfNvh_OA).

## Usage

1. After installation, run the data collection script:
    ```bash
    python main.py
    ```

2. The collected data will be automatically uploaded to BigQuery with tables integrated in a Looker Studio report.

3. Visit the Looker dashboard at (https://lookerstudio.google.com/s/kRaXfNvh_OA) to interact with the data.

## Project Structure

.
├── main.py                  # Main script for data collection and uploading to BigQuery
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not included in version control)
└── README.md                 # Project documentation

## Technologies

- **Python**: Main language for data collection and processing
- **Google BigQuery**: Cloud-based data warehouse for storing DFS data
- **Looker**: Business intelligence platform for visualizing data
- **GitHub**: Code hosting and version control

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
