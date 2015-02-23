#CodeWiki
##Cezary Kaszuba & Sebastian Talarowski
###Wyższa Szkoła Informatyki i Umiejętności 2014/2015

###Projekt semestralny



####Przed instalacją CodeWiki zapoznaj się z dokumentacją!

#####Instalacja CodeWiki (Linux)

- Zainstaluj wymagane narzędzia:
```
sudo apt-get update
sudo apt-get install python3-dev python3-setuptools
sudo easy_install virtualenv
```

- Skonfiguruj środowisko:
```
cd ~
mkdir pyramid_sites
cd pyramid_sites
sudo apt-get install git
git clone https://github.com/Krylion/codewiki
cd codewiki
```

dodatkowo...

```
virtualenv --no-site-packages env
source env/bin/activate
easy_install pyramid
easy_install pyramid_jinja2
```

- Uruchom aplikację:
```
psevre production.ini
```

Aby poprawnie przejść przez proces instalacyjny, wymagane jest konto root.