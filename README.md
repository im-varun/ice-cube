# ❄️ IceCube: NHL Analytics Engine

**A crystalline database management system for high-performance hockey analytics.**

IceCube is a terminal-based DBMS that makes digging through NHL stats *actually fun*. Built for the 2019-2020 season, it connects to a MySQL database and gives you a slick TUI (Text User Interface) with close to zero latency issues and proper data protection.

No bloated dashboards. No super slow queries. Just clean data, fast results.

---

## 🖼️ What It Looks Like

![Home page with database repopulation](assets/main%20home%20page%20with%20database%20repopulation.png)

![Analytics query screen](assets/Analytics%20query%20screen.png)

![Search database screen](assets/search%20database%20screen.png)

![UI theme menu options](assets/UI%20theme%20menu%20options.png)

---

## ⚡ Why IceCube?

| Problem | How IceCube Solves It |
|---------|----------------------|
| **Slow queries** | TUI built with Textual — responds instantly, no browser overhead |
| **SQL injection attacks** | PayloadFirewall validates every input before it touches the DB |
| **Messy raw data** | Data cleaning scripts handle duplicates, nulls, and format issues |
| **Inconsistent code style** | Pre-commit hooks with Ruff keep everything clean on every commit |
| **Ugly terminal apps** | Custom CSS styling for a polished, readable interface |

---

## 🔒 Security That Actually Works

All user input goes through a **PayloadFirewall** before any query runs:

- Blocks dangerous tokens like `; -- /* */`
- Catches SQL keywords like `DROP`, `DELETE`, `UNION`, `EXEC`
- Detects boolean injection patterns (`OR 1=1`)
- Flags hex-encoded and base64-encoded attack payloads
- Normalizes unicode to prevent sneaky whitespace tricks

![SQL injection successfully detected](assets/sql_injection_successfully%20detected.png)

When someone tries something shady, IceCube catches it and shows a friendly "nice try" message.

---

## 🧹 Data Pipeline

The raw data from Kaggle isn't ready to use out of the box. IceCube includes scripts that:

1. **Clean the data** — removes unwanted columns, fixes date formats, handles nulls, drops duplicate rows, and filters to the 2019-2020 season only
2. **Convert to SQL** — takes the cleaned CSVs and generates `INSERT` statements for your database

Both scripts are in the `scripts/` folder and run with a single command each.

---

## 📁 Project Structure

```
ice-cube/
├── .github/workflows/           # GitHub Actions CI with Ruff linting
│   └── ci.yml
│
├── .pre-commit-config.yaml      # Pre-commit hooks for code quality
├── pyproject.toml               # Project metadata
├── requirements.txt             # Python dependencies
│
├── assets/                      # Screenshots and diagrams
│   ├── Analytics query screen.png
│   ├── UI theme menu options.png
│   ├── er diagram.png
│   ├── main home page with database repopulation.png
│   ├── search database screen.png
│   └── sql_injection_successfully detected.png
│
├── data/                        # Data files (gitignored, you create these)
│   ├── raw/                     # Raw CSVs from Kaggle
│   └── clean/                   # Cleaned CSVs after running the script
│
├── scripts/                     # Utility scripts
│   ├── data_cleaning.py         # Cleans raw CSVs → outputs to data/clean/
│   └── csv_to_sql.py            # Converts cleaned CSVs → sql/populate.sql
│
├── sql/                         # Database scripts
│   ├── schema.sql               # Creates all 13 tables
│   ├── drop.sql                 # Drops all tables (for refresh)
│   └── populate.sql             # Generated INSERT statements (you create this)
│
└── src/                         # Main application code
    ├── main.py                  # Entry point — run this
    │
    ├── controllers/             # Business logic layer
    │   ├── query_controller.py  # Routes UI requests to database
    │   ├── payload_firewall.py  # SQL injection protection
    │   └── data_formatter.py    # Makes query results pretty
    │
    ├── database/                # Database layer
    │   └── query_engine.py      # All SQL queries live here
    │
    ├── query_registry.py        # Maps query names to metadata
    │
    └── ui/                      # UI layer (Textual)
        ├── screens/             # App screens
        │   ├── home_screen.py
        │   ├── analytics_screen.py
        │   └── search_screen.py
        │
        ├── widgets/             # Reusable components
        │   ├── data_table.py
        │   ├── query_card.py
        │   ├── stat_panel.py
        │   └── loading_spinner.py
        │
        ├── styles/              # CSS for the TUI
        │   ├── theme.tcss
        │   └── components.tcss
        │
        └── mocks/               # Mock data for testing without DB
            └── mock_controller.py
```

---

## 🚀 Running It Locally

### What You Need
- Python 3.8+
- Access to a MySQL Server (or MSSQL)
- The NHL dataset from Kaggle

### Step-by-Step Setup

**1. Clone and install**
```bash
git clone https://github.com/yourusername/ice-cube.git
cd ice-cube
pip install -r requirements.txt
```

**2. Get the data**

Download the NHL dataset from Kaggle and extract the CSV files into `data/raw/`.

**3. Clean the data**
```bash
python scripts/data_cleaning.py
```
This reads from `data/raw/` and outputs cleaned files to `data/clean/`.

**4. Generate SQL inserts**
```bash
python scripts/csv_to_sql.py
```
This creates `sql/populate.sql` with all the INSERT statements.

**5. Set up your environment**

Create a `.env` file in the project root:
```env
DB_SERVER=your_server_address
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_REPOPULATION_TIME=60
```

**6. Run the app**
```bash
python src/main.py
```

**7. Populate the database**

Once the app starts, press `r` (Restart) to drop and repopulate all tables. The app reads `sql/schema.sql` and `sql/populate.sql` to set everything up.

![Home page with database repopulation](assets/main%20home%20page%20with%20database%20repopulation.png)

---

## 🎯 Features & Queries

### Built-In Analytics

| Query | What It Does |
|-------|-------------|
| **Head-to-Head Duel** | Compare two players side by side |
| **Revenge Game Effect** | How players perform against old teams |
| **Home Rink Advantage** | Stats on home vs away performance |
| **Birthday Curse** | Do players choke on their birthday? |
| **Most Common Play Types** | What events happen most in games |
| **Top Shooting Teams** | Teams with the most shots |
| **Players with Most Assists** | Top playmakers |
| **Longest Games** | Epic overtime battles |

### Custom Search

Build your own queries with:
- Table selection dropdown
- Dynamic column picker
- WHERE clause input (protected by the firewall)
- Results displayed in a scrollable table

---

## 🧱 Architecture

IceCube uses a clean three-layer architecture:

| Layer | Responsibility | Key Files |
|-------|---------------|-----------|
| **UI** | Renders screens, handles keyboard input | `screens/`, `widgets/`, `styles/` |
| **Controllers** | Business logic, validation, formatting | `query_controller.py`, `payload_firewall.py` |
| **Database** | SQL execution, connection management | `query_engine.py` |

The UI never talks directly to the database. Everything flows through controllers.

---

## 🔧 Code Quality

Every commit goes through:

- **Ruff** — fast Python linter and formatter
- **Pre-commit hooks** — catches trailing whitespace, large files, YAML issues
- **GitHub Actions** — runs linting on every push

This keeps the codebase consistent across all contributors.

---

## 📐 ER Diagram
*Pls don't judge, its on paper rather than mermaid, but it covers the true essence of the dataset we used*

![ER Diagram](assets/er%20diagram.png)

---

## 🔀 Data Flow Diagram

```mermaid
flowchart TB
    subgraph External["External Sources"]
        Kaggle["Kaggle NHL Dataset"]
    end

    subgraph DataPipeline["Data Pipeline"]
        Raw["data/raw/*.csv"]
        Cleaning["scripts/data_cleaning.py"]
        Clean["data/clean/*.csv"]
        CSVtoSQL["scripts/csv_to_sql.py"]
        PopulateSQL["sql/populate.sql"]
    end

    subgraph Database["MySQL Database"]
        Schema["sql/schema.sql"]
        Tables["13 Database Tables"]
    end

    subgraph Application["IceCube Application"]
        subgraph UI["UI Layer"]
            Main["src/main.py"]
            HomeScreen["home_screen.py"]
            AnalyticsScreen["analytics_screen.py"]
            SearchScreen["search_screen.py"]
            Widgets["Widgets (DataTable, QueryCard)"]
            Styles["theme.tcss + components.tcss"]
        end

        subgraph Controllers["Controller Layer"]
            QueryController["query_controller.py"]
            PayloadFirewall["payload_firewall.py"]
            DataFormatter["data_formatter.py"]
        end

        subgraph DB["Database Layer"]
            QueryEngine["query_engine.py"]
            QueryRegistry["query_registry.py"]
        end
    end

    subgraph Config["Configuration"]
        ENV[".env"]
        PreCommit[".pre-commit-config.yaml"]
    end

    %% Data Pipeline Flow
    Kaggle -->|"download"| Raw
    Raw -->|"python"| Cleaning
    Cleaning -->|"outputs"| Clean
    Clean -->|"python"| CSVtoSQL
    CSVtoSQL -->|"generates"| PopulateSQL

    %% Database Setup Flow
    Schema -->|"CREATE tables"| Tables
    PopulateSQL -->|"INSERT data"| Tables

    %% Application Flow
    ENV -->|"credentials"| Main
    Main -->|"starts"| HomeScreen
    HomeScreen -->|"navigate"| AnalyticsScreen
    HomeScreen -->|"navigate"| SearchScreen
    AnalyticsScreen --> Widgets
    SearchScreen --> Widgets
    Widgets --> Styles

    %% Request/Response Flow
    AnalyticsScreen -->|"UIRequest"| QueryController
    SearchScreen -->|"UIRequest"| QueryController
    QueryController -->|"validate"| PayloadFirewall
    PayloadFirewall -->|"safe payload"| QueryController
    QueryController -->|"execute"| QueryEngine
    QueryEngine -->|"query"| Tables
    Tables -->|"results"| QueryEngine
    QueryEngine -->|"raw data"| QueryController
    QueryController -->|"format"| DataFormatter
    DataFormatter -->|"UIResponse"| AnalyticsScreen
    DataFormatter -->|"UIResponse"| SearchScreen

    %% Registry Lookup
    QueryRegistry -->|"query metadata"| AnalyticsScreen

    %% Code Quality
    PreCommit -->|"ruff"| Application

    %% Refresh Flow
    HomeScreen -->|"restart action"| QueryController
    QueryController -->|"drop + populate"| Tables
```

---

## 👥 Team

- Krisha Bhalala
- Varun Mulchandani
- Krish Bhalala

---

## 📜 License

MIT License — but please don't copy our code without understanding it first and learning from it + give some credits to us if you use our code.

---

*"You miss 100% of the queries you don't run."*
