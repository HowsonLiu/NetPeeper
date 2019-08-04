# NetPeeper
My email reminder and spider framework 😎
# Install
- install python3, pip3 and git
- git clone project
```
git clone git@github.com:HowsonLiu/NetPeeper.git
```
- install virtualenv
```
pip install virtualenv
```
- create venv for project
```
cd NetPeeper
virtualenv venv
```
- active venv
```
source venv/bin/activate
```
- install all requirement
```
pip install -r requirement.txt
```
- init the environment
```
python init.py
```
- then setup.cfg file will be created, fill your information
- run the spider
```
python run.py
```
# Forex
Forex module is my spider of forign currency. Data comes from bank of china.
## How to add my insterested forign currency?
In boc_spider.py, add your interested forign currency in `monitor_fc_type_list` with chinese, no need to restart then fine.