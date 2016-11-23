# python-webpage-downloader
Simple python(3.x) program to download html source along with external assets (js,css,images) from a webpage.

This program is designed to download the source html of a webpage along with external assets(js,css,images).
It checks for external assets, downloads them and replaces their respective paths in downloaded source html.

Requirements :

BeautifulSoup - To parse the html

## Example

Let's say you have to download the webpage @ http://imdb.com

First import WebPageDownloader module into your script and create an instance.
```
from webpagedownloader import WebPageDownloader
wpd = WebPageDownloader(url, data_dir)
```
Now, call the save_all_assets method from WebPageDownloader
```
url = "http://imdb.com"
data_dir = "/path/to/the/download/dir/"
wpd.save_all_assets()
```
