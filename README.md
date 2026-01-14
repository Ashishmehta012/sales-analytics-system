Sales Analytics System 📊
A modular Python-based ETL (Extract, Transform, Load) pipeline designed for an AI Data Architecture assignment. This system processes local sales data, validates business rules, enriches records via the DummyJSON API, and generates comprehensive business intelligence reports.

📝 Project Overview
This project demonstrates a robust "Hybrid Data Architecture" by combining local file processing with cloud-based API enrichment. It is designed to be modular, scalable, and fault-tolerant.

Core Capabilities
File I/O & Encoding: Reads raw data handling various encodings (UTF-8, Latin-1, CP1252) without using high-level libraries like Pandas for the extraction phase.

Data Cleaning: Manually parses pipe-delimited strings, cleans currency/numerical formats (removing commas), and enforces data types.

Validation & Filtering: Implements business rules (e.g., TransactionIDs must start with 'T') and allows user-interactive filtering by Region or Amount.

API Integration: Connects to the DummyJSON API to fetch real-time product data (Brand, Category, Rating) and enriches the local dataset.

Reporting: Automatically generates a formatted text report (output/sales_report.txt) summarizing revenue, trends, and top performers.

📁 Project Architecture
The system follows a strict modular design pattern to separate concerns:

sales-analytics-system/ ├── main.py # Orchestrator: Manages the 10-step execution flow ├── requirements.txt # Dependencies (requests, pandas, matplotlib) ├── README.md # Project Documentation ├── data/ │ ├── sales_data.txt # Input: Raw Transaction Data (Pipe-separated) │ └── enriched_sales_data.txt # Output: Data enriched with API columns ├── utils/ │ ├── init.py # Package Initialization │ ├── file_handler.py # Handles file reading, writing, and encoding errors │ ├── data_processor.py # Core logic: Parsing, Validation, Analytics, Reporting │ └── api_handler.py # Connects to DummyJSON API for data enrichment └── output/ ├── sales_report.txt # Final Executive Summary Report └── cleaned_sales_data.csv # Final Cleaned Dataset

🚀 Setup & Installation
Prerequisites
Python 3.8 or higher

Git (for version control)

Internet connection (required for API enrichment)

Installation Steps
Clone the Repository git clone https://github.com/your-username/sales-analytics-system.git cd sales-analytics-system

Install Dependencies The project uses requests for API calls and pandas/matplotlib for final data export and visualization. pip install -r requirements.txt

💻 How to Run
Execute the main script from the root directory:

python main.py

Execution Workflow (What Happens When You Run It)
[1/10] Reading Data: The system loads data/sales_data.txt, automatically detecting the correct file encoding.

[2/10] Parsing: Converts raw text lines into Python dictionaries, handling data type conversion (Strings -> Int/Float).

[3/10] User Interaction:

The system displays available Regions and the Price Range.

Prompt: Do you want to filter data? (y/n)

If y, you can filter by specific Region (e.g., 'North') or Price bounds.

[4/10] Validation: Checks data integrity. Records with missing fields, negative prices, or incorrect ID prefixes (T/P/C) are flagged and excluded.

[5/10] Analysis: Calculates metrics like Total Revenue, Average Order Value, and Top Selling Products.

[6/10] API Fetching: Connects to dummyjson.com/products to download external product data.

[7/10] Enrichment: Merges local transaction data with API data based on Product ID.

[8/10] Saving Enriched Data: Saves the combined dataset to data/enriched_sales_data.txt.

[9/10] Reporting: Generates a detailed text report in output/sales_report.txt containing all analytics tables.

[10/10] Completion: Final clean data is exported to CSV.

📊 Evaluation Criteria & Implementation Details
Part 1: File Handling & Preprocessing
Manual Parsing: Implemented in utils/file_handler.py and data_processor.py.

Encoding: Specifically handles UnicodeDecodeError by trying multiple encodings.

Validation: Filters out transactions where Quantity <= 0 or IDs don't match the standard format.

Part 2: Data Processing & Analytics
Aggregations: Functions in data_processor.py calculate region-wise sales and identify peak sales days.

Sorting: All tables (Top Products, Customers) are sorted dynamically by revenue or quantity.

Part 3: API Integration
Hybrid Pipeline: Implemented in utils/api_handler.py.

Enrichment Logic: Maps local ProductID (e.g., 'P1') to API id (1) to append 'Brand' and 'Rating' fields.

Fault Tolerance: Includes try-except blocks to handle API timeouts or connection failures gracefully.

Part 4: Report Generation
Automated Reporting: The generate_sales_report function builds a formatted text file with headers, timestamps, and aligned columns for professional readability.

Part 5: Main Application
Orchestration: main.py serves as the controller, managing the flow between modules and handling user inputs and global exceptions.

📧 Contact
For any queries regarding this architecture assignment, please contact the repository owner.
