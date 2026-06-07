# potyk-self-2

> Personal diary

## Links

- [Github](https://github.com/potykion/potyk-self-2.git)

## Ops

### Prod Setup

#### First time

```shell
ssh-keygen
# example pub
# paste it to https://github.com/settings/keys
cat .ssh/id_ed25519.pub

ssh -l leybovich-nikita 84.201.131.244
# e.g. git@github.com:potykion/wine-wish.git
git clone git@github.com:potykion/potyk-self-2.git

cd potyk-self-2
python3 -m venv ".venv"
source ./.venv/bin/activate
pip install -r requirements.txt
# fill env w FLASK_APP=main & FLASK_SECRET=...
nano .env
python setup_db.py

sudo cp ./potyk-self-2.service /etc/systemd/system/potyk-self-2.service
sudo chmod 644 /etc/systemd/system/potyk-self-2.service
sudo systemctl enable --now potyk-self-2.service

```

#### Update

```shell
ssh -l leybovich-nikita 84.201.131.244
cd potyk-self-2
git pull

source ./.venv/bin/activate
pip install -r requirements.txt 
alembic upgrade head

sudo systemctl restart potyk-self-2.service
```

### Copy prod bd backup to local

```sh
/home/leybovich-nikita/potyk-self-2/instance

```