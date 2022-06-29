## 1. Download
Install MySQL: https://www.mysql.com/downloads/
<br></br>
Install Node.js: https://nodejs.org/en/
<br></br>
Install Python: https://www.python.org/getit/
<br></br>
## 2. Database
Open terminal, create database:
```
mysql -u root -p
CREATE DATABSE safetweets;
```
Use VSCode open "SafeTweet"
<br></br>
Open file: `SafeTweet/backend/knexfile.js`, modify the configure to fit your MySQL.
<br></br>
Open VSCode terminal, create tables:
```
cd backend
npm knex migrate:latest
```
<br></br>
## 3. Install packages
VSCode terminal:
<br></br>
Front-end:
```
cd frontend
npm install
```
Back-end:
```
cd backend
npm install
pip install -U scikit-learn scipy matplotlib (About 260M)
pip install stanza
pip install joblib
```
<br></br>
Open and run file: `SafeTweet/backend/python/ner.py`, to install the stanza English dictionary (About 480M)
<br></br>
After downloading dictionary, comment
```
# stanza.download('en ')
```
The dictionary only needs to be downloaded once.
<br></br><br></br>
Open file: `SafeTweet/backend/routes/post.js`, change your Python path in line 68:
```
pythonPath: '/PATH/TO/PYTHON'
```
<br></br>
## 4. Start server
VSCode terminal:
<br></br>
Front-end:
```
cd frontend
npm run server
```
Back-end:
```
cd backend
npm start
```
<br></br>
## 5. Use SafeTweet
Open browser
<br></br>
URL: https://localhost:8080
<br></br>
Please enjoy it.


