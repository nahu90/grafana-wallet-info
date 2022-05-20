<div id="top"></div>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Grafana Wallet Info</h3>

  <p align="center">
    <br />
    <a href="http://naha.ar/dashboards">View Demo</a>
    ·
    <a href="https://github.com/nahu90/grafana-wallet-info/issues">Report Bug</a>
    ·
    <a href="https://github.com/nahu90/grafana-wallet-info/issues">Request Feature</a>
  </p>
</div>

[![grafana Screen Shot][product-screenshot-1]](http://django.naha.ar/media/images/Screenshot_from_2022-05-19_18-43-40.png)
[![grafana Screen Shot][product-screenshot-2]](http://django.naha.ar/media/images/Screenshot_from_2022-05-15_00-41-53.png)

<!-- ABOUT THE PROJECT -->
## About The Project

This project was created due to the necessity to track the assets worth and performance from my own 
wallet on the ethereum and polygon network. Most of the existing "wallet trackers" analyze your 
current assets and generate a timeline based on their historical value. Nevertheless, this type of 
trackers doesn't contain the information of your past token holdings which prevents you from comparing 
while selling and buying. That's why I've created this system that regularly saves screenshots from 
assets worth and performance, generating a historical timeline of your token holdings which are 
showed in a graphic.

To achieve this, I've developed a docker compose that contains the following pictures:
* A postgres data base
* A django backend
* A task queue made using celery/redis
* A grafana fronted

I've decided to make this project public since I've found out that it is really hard to get 
information about including a grafana in a docker compose, as well as how to use it with grafanalib 
in order to create graphics that are related to economic issues. 


[![grafana Screen Shot][product-screenshot-3]](http://django.naha.ar/media/images/Screenshot_from_2022-05-15_00-44-06.png)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- FEATURES -->
## Features

- [x] Get historical prices from Coingecko
- [ ] Realtime last prices
- [ ] Connect to Ethereum blockchain
- [ ] Connect to L2 blockchains
    - [x] Polygon
    - [ ] Avalanche
- [x] Get balance of MATIC
- [x] Get balance of ERC-20 tokens
- [x] Get balance from AAVE v3 supplies
- [ ] Get pools from Uniswap
- [ ] Get pools from Quickswap

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [PostgreSQL](https://www.postgresql.org/)
* [Django](https://www.djangoproject.com/)
* [Grafana](https://grafana.com/)
* [Redis](https://redis.io/)
* [Celery](https://docs.celeryq.dev/en/stable/)
* [NGINX](https://www.nginx.com/)

### Python lib to connect web3

* [Web3.py](https://github.com/ethereum/web3.py)

### Python lib to connect grafana

* [grafanalib](https://github.com/weaveworks/grafanalib)

### Python lib to connect coingecko

* [pycoingecko](https://github.com/man-c/pycoingecko)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

You will need to configure several issues in order to run it locally. The following tutorial is for 
ubuntu or linux-based OS only:

### Prerequisites

As a prerequisite you will need to install docker, docker-compose and make.
* install docker
  ```sh
  sudo apt update
  sudo apt install apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
  sudo apt install docker-ce
  sudo usermod -aG docker ${USER}
  su - ${USER}
  ```
* install docker compose
  ```sh
  sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  ```
* install make
  ```sh
  apt install make
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/nahu90/grafana-wallet-info.git
   ```
2. create file `.env`, clone from `.env.template `
3. create file `.gfenv`, clone from `.gfenv.template`
4. run deploy command
   ```sh
   make deploy
   ```
<p align="right">(<a href="#top">back to top</a>)</p>

### Troubleshooting

* It will be necesary for you to enter postgres and create a database for grafana, put the credentials in `.gfenv` and redeploy the app
* You will have to enter grafana interface and add Django Postgres DB as a datasource.
* It is important that you to enter grafana interface and create an api key, then put in `.env` in `GRAFANA_API_KEY` and redeploy the app

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Nahuel Fernandez - naha90@gmail.com

Project Link: [https://github.com/nahu90/grafana-wallet-info](https://github.com/nahu90/grafana-wallet-info)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot-1]: http://django.naha.ar/media/images/Screenshot_from_2022-05-19_18-43-40.png
[product-screenshot-2]: http://django.naha.ar/media/images/Screenshot_from_2022-05-15_00-41-53.png
[product-screenshot-3]: http://django.naha.ar/media/images/Screenshot_from_2022-05-15_00-44-06.png
