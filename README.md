## MindfulTube

A video viewer for people who want to be free from the algorithms .

---

## About
- Select channels to allow from a **YT URL.**
- Watch the videos algorithm free, ad free directly on your device.
- Select videos or shorts from the selected channel in the app.

---

## Installation (Linux / Ubuntu / Debian)
- Debian:  sudo apt install ./mindful_tube_pkg.deb
- Others:  curl -sSL https://raw.githubusercontent.com/timmylockley/Mindful-Tube/main/mindful_tube_install.sh | bash
- Manual Build:
      If you want to build the package yourself from source:
      
      1. Clone the repository:
         git clone https://github.com/your-username/mindful-tube.git
         cd mindful-tube
      2. Set up your virtual environment and install dependencies:
         python3 -m venv myenv
         source myenv/bin/activate
         pip install -r requirements.txt
      3. Rebuild the package and install:
         dpkg-deb --build mindful_tube_pkg
         sudo apt install ./mindful_tube_pkg.deb

---

## License
- Licensed under the **MIT Licensed.**
- Authored by **Timothy Lockley.**
- **Note:** This project is Vibe coded, but has been extensively reviewed and compiled by Me.
