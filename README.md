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
├── server/
│   ├── router.py              # Route decorators and handlers
│   ├── database_interface.py  # Database query layer
├── handlers.py                # API endpoint implementations
├── constants.py               # Type definitions and constants
└── README.md
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
