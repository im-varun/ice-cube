# ❄️ IceCube: NHL Analytics Engine

**A crystalline database management system for high-performance hockey analytics.**

---

## 📖 Overview

**IceCube** is a Database Management System (DBMS) interface engineered to extract deep insights from NHL game data. Built for the 2019-2020 season, it transforms raw statistical data into actionable intelligence through a robust, layered architecture.

Designed with a focus on **security**, **modularity**, and **user experience**, IceCube provides a terminal-based interface (TUI) that feels as smooth as fresh ice.

---

## 🏗️ System Architecture

IceCube follows a strict **3-Tier Architecture** to ensure separation of concerns, maintainability, and security.

### 1. Presentation Layer (UI)

* **Framework**: Built using `Textual` for a rich, interactive terminal experience.
* **Screens**:
  * **Home Screen**: The landing dashboard with quick access to features.
  * **Analytics Screen**: A hub for running predefined, complex analytical queries.
  * **Search Screen**: An advanced interface for constructing custom SQL queries safely.
* **Widgets**: Modular components like `QueryCard` for displaying options and `DataTable` for rendering results.
* **Styles**: CSS-driven styling (`.tcss`) ensures a consistent, premium aesthetic across the application.

### 2. Application Layer (Controllers)

* **Role**: Acts as the middleware between the UI and the Database.
* **Key Components**:
  * **`QueryController`**: Orchestrates query execution and data retrieval.
  * **`DataFormatter`**: Transforms raw database tuples into human-readable formats (e.g., parsing `2019030121` into "Oct 12, 2019").
  * **`PayloadFirewall`**: A dedicated security module for input validation.

### 3. Data Layer (Database)

* **Role**: Handles direct interaction with the SQL database.
* **Key Components**:
  * **`QueryEngine`**: Executes raw SQL queries safely.
  * **`ConnectionManager`**: Manages database connections and transactions.

---

## 🛡️ Security & Robustness

Security is a core pillar of IceCube. We implement a defense-in-depth strategy to prevent SQL Injection (SQLi) and ensure data integrity.

### 🧱 PayloadFirewall

Located in `src/controllers/payload_firewall.py`, this module acts as a gatekeeper for all user inputs.

* **Pattern Matching**: Uses compiled Regex to detect and block common SQLi patterns (e.g., `OR 1=1`, `UNION SELECT`).
* **Keyword Blacklisting**: Blocks dangerous SQL keywords (`DROP`, `DELETE`, `ALTER`) in user inputs.
* **Encoding Detection**: Detects and blocks obfuscated attacks using Hex or Base64 encoding.
* **Strict Mode**: Optional strict validation to allow only alphanumeric characters.

### 🔒 Safe Query Construction

* **Parameterization**: Wherever possible, queries use parameterized inputs to prevent injection.
* **Input Sanitization**: All inputs are normalized (Unicode normalization) and stripped of dangerous meta-characters before processing.

---

## 📂 Project Structure

The project is organized to promote scalability and ease of navigation.

```text
icecube/
├── src/
│   ├── ui/                     # Presentation Layer
│   │   ├── screens/            # Home, Analytics, Search screens
│   │   ├── widgets/            # Reusable UI components
│   │   └── styles/             # Textual CSS files
│   │
│   ├── controllers/            # Application Layer
│   │   ├── payload_firewall.py # Security validation
│   │   ├── query_controller.py # Logic orchestration
│   │   └── data_formatter.py   # Response formatting
│   │
│   └── database/               # Data Layer
│       ├── query_engine.py     # SQL execution engine
│       └── queries/            # SQL query definitions
│
├── data/                       # Data storage
├── tests/                      # Unit and integration tests
└── main.py                     # Application entry point
```

---

## ✨ Key Features

IceCube offers a comprehensive suite of 12 powerful queries tailored for hockey enthusiasts and analysts:

### ⚔️ Head-to-Head & Rivalries

* **Duel Tracker**: Compare stats between any two players (e.g., "Crosby vs. Ovechkin") to settle G.O.A.T. debates.
* **Revenge Game Effect**: Analyze if players perform better when facing their former teams.
* **Home Rink Advantage**: Quantify the impact of starting on a specific side of the rink.

### � Player Insights

* **Lone Wolfs**: Identify players who score goals but rarely assist (pure finishers).
* **Top Scoring Players**: Rank players by total offensive production while filtering for discipline (penalty threshold).
* **Most Penalized Players**: List players with the highest total penalty minutes.
* **Most Assists**: Celebrate the playmakers with the highest assist totals.

### ⏱️ Game & Performance Analysis

* **Longest Average Shifts**: Discover the endurance athletes who stay on the ice the longest per shift.
* **Longest Games**: Rank games by total elapsed time, finding those epic overtime battles.
* **Birthday Curse Analysis**: Determine if playing on a birthday affects a player's performance.

### � Team & Strategic Trends

* **Top Shooting Teams**: Rank teams by shooting percentage and shot volume.
* **Most Common Play Types**: Analyze the frequency of different shot types (e.g., wrist shots, tip-ins) to understand game flow.

---

## 🔎 Search Screen

For users who need more than predefined queries, the **Search Screen** provides a powerful interface for custom data exploration.

* **Custom Query Construction**: Build SQL queries interactively without writing raw code.
* **Dynamic Table Selection**: Choose from available database tables to explore specific datasets.
* **Smart Column Filtering**: Dynamically select columns based on the chosen table.
* **Secure Input**: All custom inputs are passed through the `PayloadFirewall` to prevent SQL injection attacks.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* Terminal with True Color support (e.g., iTerm2, Windows Terminal)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/icecube.git
   cd icecube
   ```
2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**

   ```bash
   python src/main.py
   ```

---

## 🤝 Contributing

Contributions are welcome! Please ensure all new features pass the `PayloadFirewall` checks and adhere to the 3-tier architecture.

1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/amazing-stat`).
3. Commit your changes.
4. Open a Pull Request.

---

**IceCube** — *Crystal clear insights for the coolest game on earth.*
