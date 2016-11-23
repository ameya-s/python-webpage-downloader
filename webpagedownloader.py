import sys, os, shutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote
from urllib.request import urlopen, urlretrieve, Request
from urllib.error import URLError, HTTPError

class WebPageDownloader():

    def __init__(self, url, data_dir):
        self.url = url
        self.html_source = self.get_content(self.url)
        self.soup = BeautifulSoup(self.html_source, 'html.parser')
        if data_dir[-1] == '/':
            self.data_dir = data_dir
        else:
            self.data_dir = data_dir + '/'

    def get_content(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            req = Request(url, headers=headers)
            res = urlopen(req)
            content = res.read()
            return content
        except HTTPError as err:
            print("HTTP error occured!\n\tError code : %s\n\tReason : %s" % (err.code , err.reason))
        except URLError as err:
            print("ERROR : %s" % (err.reason))

    def make_dir(self, path):
        try:
            if not os.path.exists(path):
                os.umask(0000)
                os.makedirs(path)
            return True
        except Exception as e:
            print("ERROR : %s" % e.message)

    def save_all_assets(self):
        assets = {'js':{'tag':'script','attr':'src', 'ext':['.js']},'css':{'tag':'link','attr':'href', 'ext':['.css']},'img':{'tag':'img','attr':'src', 'ext':['.png','.jpg','.gif']}}
        parsed_url = urlparse(self.url)
        for asset_type in assets:
            for asset in self.soup.findAll(assets[asset_type]['tag']):
                for extension in assets[asset_type]['ext']:
                    try:
                        if extension in asset[assets[asset_type]['attr']]:
                            if 'http' not in asset[assets[asset_type]['attr']]:
                                if asset[assets[asset_type]['attr']][0] is not '/':
                                    if asset[assets[asset_type]['attr']][0] == '.':
                                        while asset[assets[asset_type]['attr']][0] is not '/':
                                             asset[assets[asset_type]['attr']] = asset[assets[asset_type]['attr']][1:]
                                        _href = parsed_url[0] + '://' + parsed_url[1] + asset[assets[asset_type]['attr']]
                                    else:
                                        _href = self.url + "/" + asset[assets[asset_type]['attr']]
                                else:
                                    if asset[assets[asset_type]['attr']][0:2] == '//':
                                        _href = 'http://' + asset[assets[asset_type]['attr']].replace('//','')
                                    else:
                                        _href = parsed_url[0] + '://' + parsed_url[1] + asset[assets[asset_type]['attr']]
                            else:
                                _href = asset[assets[asset_type]['attr']]

                            self.make_dir(self.data_dir + asset_type + '/')

                            if len(_href.split("/")[-1].split('.')[0]) < 15:
                                _asset_path = self.data_dir + asset_type + '/' + _href.split("/")[-1].split('.')[0] + extension
                            else:
                                _asset_path = self.data_dir + asset_type + '/' + _href.split("/")[-1].split('.')[0][0:15] + extension

                            if not os.path.isfile(_asset_path):
                                _asset_string = self.get_content(_href)
                                if asset_type == 'img':
                                    with open(_asset_path, 'wb') as f:
                                        f.write(_asset_string)
                                        f.close()
                                else:
                                    with open(_asset_path, 'w+') as f:
                                        f.write(str(_asset_string, 'utf-8'))
                                        f.close()

                            # Modify the asset path in the source html
                            asset[assets[asset_type]['attr']] = './'+ asset_type + '/' + _asset_path.split("/")[-1]
                    except:
                        print("Can't download the asset : %s" % asset)

        self.html_source = str(self.soup)
        with open(self.data_dir + 'index.html', 'w+') as html_source_file:
            html_source_file.write(self.html_source)
            html_source_file.close()
