# CompuKids Website

A multi-page website for **CompuKids**, a fictional app development company based in Durban, South Africa. I built it during the **FNB App Academy** training to practise HTML, CSS and JavaScript.

**Live demo:** https://ukhezo.github.io/COMPUKIDS-WEBSITE-1/

![Home page](screenshots/home.png)

## Features

- **Live clock:** JavaScript shows the current date and time, updating every second
- **Responsive image gallery:** a CSS Grid gallery that adjusts to any screen size
- **Hero profile pages:** each Avenger has a page with a bio and power stats
- **Scrolling text:** a CSS keyframe animation (a modern replacement for `<marquee>`)
- **Navigation menu:** the same menu on every page, with hover effects
- **Mobile friendly:** a viewport meta tag and a flexible layout

## Screenshots

| Hero page | About page |
| --- | --- |
| ![Hero page](screenshots/avenger-page.png) | ![About page](screenshots/about.png) |

| Contact page | Mobile view |
| --- | --- |
| ![Contact page](screenshots/contact.png) | <img src="screenshots/mobile.png" alt="Mobile view" width="250"> |

## Pages

| Page | File | Description |
| --- | --- | --- |
| Home | `index.html` | Live date and time, plus a gallery of six Avengers |
| Avengers | `avenger-1.html` to `avenger-6.html` | Bio and power stats for Thor, Iron Man, Hulk, Hawkeye, Captain America and Black Widow |
| About Us | `about.html` | The company introduction, with scrolling text |
| Contact | `contact.html` | Contact details and a live clock |
| Links | `links.html` | Useful links |

## Built with

- **HTML5:** semantic page structure and meta tags
- **CSS3:** Grid layout, keyframe animations and hover effects
- **JavaScript:** a live date and time with `setInterval`

## Project structure

```
COMPUKIDS-WEBSITE-1/
├── index.html
├── about.html
├── contact.html
├── links.html
├── avenger-1.html … avenger-6.html
├── style.css
├── script.js
├── images/         ← Avenger images
└── screenshots/    ← README screenshots
```

## Run it locally

1. Clone the repo:
   ```bash
   git clone https://github.com/Ukhezo/COMPUKIDS-WEBSITE-1.git
   ```
2. Open `index.html` in any browser. Nothing needs to be installed.

## What I learned

- Structuring a multi-page website and linking pages together
- Styling with external CSS, including Grid and animations
- Adding interactivity with JavaScript
- Using Git and GitHub, and hosting a site on GitHub Pages

## Disclaimer

This is a training project. CompuKids and its contact details are fictional. Avengers characters and images belong to Marvel and are used for educational purposes only.

## Author

**Ukhezo** – [GitHub](https://github.com/Ukhezo)
