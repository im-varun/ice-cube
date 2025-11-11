# ❄️ IceCube

**A crystalline database management system for NHL analytics**

IceCube is a powerful DBMS interface designed to unlock deep insights from NHL game data. Built for the 2019-2020 season, IceCube transforms raw hockey statistics into actionable intelligence through intuitive queries and blazing-fast performance.

---

## 🏒 What is IceCube?

IceCube cuts through the noise of hockey statistics like skate blades on fresh ice. Whether you're analyzing player performance, team dynamics, or game-changing moments, IceCube delivers the data you need with precision and speed.

**Think of it as your personal Zamboni for NHL data** smoothing out the rough patches and revealing the perfect surface beneath.

---

## ✨ Key Features

### 🎯 Signature Queries

IceCube comes packed with powerful analytical queries designed to answer some of the most unique questions that hockey fans may have:

* **Messi or Ronaldo? Head-to-Head Duel Tracker** Compare player matchups and rivalry statistics
* **Revenge Game Effect** Analyze performance patterns when teams face recent opponents
* **Home Rink Side Advantage** Quantify the true impact of playing at home
* **Birthday Curse Analysis** Does playing on your birthday affect performance?
* **Game Scoring Trends** Track scoring patterns across periods, seasons, and situations
* **Most Common Play Types** Understand the flow and style of modern hockey
* **Highest Scoring Teams per Season** Identify offensive powerhouses
* **Players with Most Assists** Celebrate the playmakers
* **Longest Games** Find those epic overtime battles
* **Players with Longest Average Shift Durations** Discover the endurance athletes
* **Top Scoring Players Excluding Penalty-Prone Players** Clean skill analysis
* **Players Who Score But Never Assist** Pure goal-scorers revealed

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* NHL 2019-2020 season database

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/icecube.git
cd icecube

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

### Quick Example

## 📁 Project Structure

```
icecube/
├── .github/                              # github ci/cd workflows with ruff
│   └── workflows/
│   	└── ci.yml
│
├── lib/                              # Packaged dependencies (no venv)
│   ├── textual/
│   ├── rich/
│   └── ...
│
├── src/                              # Main application code
│   │
│   ├── ui/                           # UI Layer (Member 1)
│   │   ├── __init__.py
│   │   ├── screens/                 # Textual screens
│   │   │   ├── __init__.py
│   │   │   ├── home_screen.py
│   │   │   ├── login_screen.py
│   │   │   ├── query_screen.py
│   │   │   ├── results_screen.py
│   │   │   └── analytics_screen.py
│   │   │
│   │   ├── widgets/                 # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── query_card.py
│   │   │   ├── data_table.py
│   │   │   ├── stat_panel.py
│   │   │   └── loading_spinner.py
│   │   │
│   │   ├── styles/                  # CSS styling for Textual
│   │   │   ├── __init__.py
│   │   │   ├── theme.tcss
│   │   │   └── components.tcss
│   │   │
│   │   └── app.py                   # Main Textual App class
│   │
│   ├── controllers/                 # Business Logic Layer (Member 2)
│   │   ├── __init__.py
│   │   ├── base_controller.py      # Abstract base controller
│   │   ├── auth_controller.py      # Login/logout logic
│   │   ├── query_controller.py     # Query orchestration
│   │   ├── analytics_controller.py # Analytics queries logic
│   │   └── data_formatter.py       # Format data for UI consumption
│   │
│   ├── database/                    # Database Layer (Member 3)
│   │   ├── __init__.py
│   │   ├── connection.py           # DB connection management
│   │   ├── query_engine.py         # Main query execution engine
│   │   ├── query_validator.py      # SQL injection prevention
│   │   ├── query_builder.py        # Safe query construction
│   │   │
│   │   ├── queries/                # Predefined queries
│   │   │   ├── __init__.py
│   │   │   ├── player_queries.py
│   │   │   ├── team_queries.py
│   │   │   ├── game_queries.py
│   │   │   └── analytics_queries.py
│   │   │
│   │   └── models/                 # Data models/schemas
│   │       ├── __init__.py
│   │       ├── player.py
│   │       ├── team.py
│   │       └── game.py
│   │
│   ├── shared/                      # Shared utilities
│   │   ├── __init__.py
│   │   ├── config.py               # Configuration management
│   │   ├── constants.py            # Shared constants
│   │   ├── exceptions.py           # Custom exceptions
│   │   ├── logger.py               # Logging setup
│   │   └── types.py                # Type definitions
│   │
│   └── main.py                      # Application entry point
│
├── scripts/                         # Utility scripts
│   ├── populate_database.py
│   ├── empty_database.py
│   ├── data_cleaning.py
│   └── view_metadata.py
│
├── data/                            # Data files
│   ├── raw/                        # Raw NHL data
│   ├── cleaned/                    # Cleaned data
│   ├── metadata.txt                # Data documentation
│   └── schema.sql                  # Database schema
│
├── reports/                         # Project documentation
│   ├── er_diagram.png
│   ├── erd_relations.pdf
│   ├── normalization_steps.pdf
│   └── queries_description.pdf
│
├── tests/                           # Unit tests (mirror src structure)
│   ├── __init__.py
│   ├── test_ui/
│   ├── test_controllers/
│   ├── test_database/
│   └── test_shared/
|
├── logistics_scripts/               # basic scripts for creating empty project
│   ├── __init__.py
│   ├── test_ui/
│   ├── test_controllers/
│
├── .git/                            # Git repository
├── .gitignore
├── .pre-commit-config.yaml         # Pre-commit hooks
├── pyproject.toml                  # Project metadata
├── requirements.txt                # Dependencies list
├── README.md
├── template.py			    # Simple textual app to test dependencies
└── CONTRIBUTING.md                 # Collaboration guidelines
```

---

## 🎮 API Reference

---


## 🧊 Database Schema

---

## 🏆 Why "IceCube"?

Like ice cubes in a cold drink, IceCube keeps your data  **crystal clear** ,  **perfectly structured** , and  **refreshingly accessible** . Each query is a facet that reveals new insights, just as light refracts through ice to create brilliant patterns.

Plus, it sounds cool. 😎

---

## 🤝 Contributing

We welcome contributions! Whether it's new queries, performance improvements, or bug fixes, feel free to submit a pull request.

1. Fork the repository
2. If importing textual library related features, make sure to change path to `lib/`
   ```
   # eg- template.py is within same directory as lib/

   import sys
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
   ```
3. Create your feature branch (`git checkout -b feature/bar-down-analytics`)
4. Commit your changes (`git commit -m 'Add bar-down goal analysis'`)
5. Push to the branch (`git push origin feature/bar-down-analytics`)
6. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License see the LICENSE file for details.

---

## 🙏 Acknowledgments

* NHL for the 2019-2020 season data
* All the players who made this season unforgettable
* Collaborators: Krisha Bhalala, Varun Mulchandani, Krish Bhalala

---

**Built with hockey fans, by hockey fans, for hockey fans**

*"You miss 100% of the queries you don't run." — Wayne Gretzky, probably*
