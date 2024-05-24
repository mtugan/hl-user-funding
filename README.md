# hl-user-funding

For now charts dollars paid per funding cycle (sign is flipped, paying is positive, receiving is negative, in line with funding rate).

## Use

```bash
# Clone repo
git clone https://github.com/mtugan/hl-user-funding
# Make virtualenv in dir
virtualenv hl-user-funding
# activate env
cd hl-user-funding
source bin/activate
# Install deps
pip install python-dotenv matplotlib pandas
# Fill out .env 
echo "ADDRESS=""" > .env
# Run
python main.py
```