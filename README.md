# MindfulTube

An intentional, distraction-free YouTube curation and playback tool.

---

## About

MindfulTube is a desktop application designed to help you regain control over your attention. By filtering out algorithmic noise, recommendations, and sidebars, MindfulTube lets you watch the content you actually intend to watch without falling into the endless rabbit hole of the YouTube homepage.

---

## Features

* Distraction-Free Interface: Clean, focused video player without recommendations, comments, or distracting sidebars.
* Curated Intent: Search or load specific media intentionally.
* Powered by yt-dlp: Fast, reliable, and lightweight video stream fetching.
* Cross-Platform Potential: Built with Python, available for Linux desktop via .deb packages and expandable to mobile targets via BeeWare.

---

## Tech Stack

* Language: Python 3
* GUI Framework: Toga / PyQt (depending on your build target)
* Downloader Backend: yt-dlp

---

## Installation (Linux / Ubuntu / Debian)

You can install MindfulTube directly using the pre-compiled Debian package (.deb) included in the repository:

sudo apt install ./mindful_tube_pkg.deb

### Manual Build
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

## Usage

Once installed, launch MindfulTube directly from your system's application menu or run it from the terminal:

mindful-tube

---

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See LICENSE for more information.
