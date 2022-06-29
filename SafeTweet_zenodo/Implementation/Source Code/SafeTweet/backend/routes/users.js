const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const middleware = require('../middlewares');
const expireTime = 18000;
const multer = require('multer')

const avatarDIR = './public/avatars';

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, avatarDIR);
  },
  filename: (req, file, cb) => {
    const fileName = req.decoded.user.id + '.png';
    cb(null, fileName)
  }
});

const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {

    if (file.mimetype == "image/png" || file.mimetype == "image/jpg" || file.mimetype == "image/jpeg") {
      cb(null, true);
    } else {
      cb(null, false);
      return cb(new Error('Only .png, .jpg and .jpeg format allowed!'));
    }
  }
});


router.get('/', middleware.authorize, function(req, res) {

  req.db.from('users').select('*').where('email', '=', req.decoded.user.email).then((rows) => {
    return res.json(rows[0]);
  }).catch(err => {
    console.log(err);
    res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
  })
});


router.post('/logout', (req, res) => {
  res.clearCookie('token').end();
});


router.post('/register', function(req, res) {

  const { email, password, username, company } = req.body;

  if (!email || !password || !username || !company) {
    return res.status(400).json({
      "error": true,
      "message": "Request body incomplete, both email and password are required"
    })
  }

  req.db.from('users').select('*').where('username', '=', username).then((rows) => {
    if (rows.length > 0) {
      return res.status(409).json({
        "error": true,
        "message": "User already exists"
      })
    }
    const saltRounds = 10;
    const hash = bcrypt.hashSync(password, saltRounds)
    return req.db.insert({ email, password: hash, username, company, avatar: '/avatars/default-avatar.png' }, 'id').into('users').then(() => {
      return res.status(200).json({
        "message": "User created"
      })
    })
  }).catch(err => {
    console.log(err);
    res.status(500).json({
      "error": true,
      "message": "email already exists"
    })
  })

});

router.post('/login', function(req, res) {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({
      "error": true,
      "message": "Request body incomplete, both email and password are required"
    })
  }
  let user = {};
  req.db.from('users').select('*').where('email', '=', email).then((rows) => {
    if (rows.length == 0) {
      return res.status(401).json({
        "error": true,
        "message": "Incorrect email or password"
      })
    }
    user = rows[0];
    return bcrypt.compare(password, user.password)
  }).then((match) => {
    if (!match) {
      return res.status(401).json({
        "error": true,
        "message": "Incorrect email or password"
      })
    }
    delete user.password
    const secretKey = require('../constants').secretKey;
    const expires_in = 60 * 60 * 24;
    const exp = Date.now() + expires_in * 1000;
    const token = jwt.sign({ user, exp }, secretKey)

    res.cookie('token', token, { httpOnly: true, sameSite: true, maxAge: 1000 * expireTime });
    return res.json({ access_token: token, expires_in: 1000 * expireTime, user })
  })
    .catch(err => {
      console.log(err);
      return res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
    })
});




router.get('/profile', middleware.authorize, function(req, res) {


  const builder = req.db.from('users');

  builder.select('*');

  builder.where('id', '=', req.decoded.user.id)
    .then((rows) => {
      if (rows.length == 0) {
        return res.status(401).json({
          "error": true,
          "message": "User not found"
        })
      }

      res.json(rows[0]);

    }).catch(err => {
      console.log(err);
      res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
    })

})

router.get('/company', middleware.authorize, function(req, res) {
  const builder = req.db.from('users');
  builder.select('company');

  builder.where('id', '=', req.decoded.user.id)
    .then((rows) => {
      if (rows.length == 0) {
        return res.status(401).json({
          "error": true,
          "message": "User not found"
        })
      }
      res.json(rows[0]);
    }).catch(err => {
      console.log(err);
      res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
    })
  
})


router.get('/profile/:id', function(req, res) {

  const id = req.params.id;

  const builder = req.db.from('users');

  builder.select('*');

  builder.where('id', '=', id)
    .then((rows) => {
      if (rows.length == 0) {
        return res.status(401).json({
          "error": true,
          "message": "User not found"
        })
      }

      res.json(rows[0]);

    }).catch(err => {
      console.log(err);
      res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
    })

})

router.post('/upload', middleware.authorize, upload.single('file'), function(req, res) {
  const builder = req.db.from('users').where('id', req.decoded.user.id);
  if (req.file)
    builder.update('avatar', '/avatars/' + req.file.filename)
  builder.then(() => {
    let _b = req.db.from('users');

    _b.select('*');

    _b.where('id', '=', req.decoded.user.id)
      .then((rows) => {
        let user = rows[0]
        delete user.password
        res.json(user);
      }).catch(err => {
        res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
      })

  }).catch(err => {
    console.log(err);
    res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
  })
})

router.put('/profile', middleware.authorize, function(req, res) {

  const { email, full_name, company, phone, password } = req.body;

  const builder = req.db.from('users').where('id', req.decoded.user.id);

  if (email)
  builder.update('email', email)
  if (full_name)
    builder.update('full_name', full_name)
  if (company)
    builder.update('company', company)
  if (phone)
    builder.update('phone', phone)
  if (password) {
    const saltRounds = 10;
    const hash = bcrypt.hashSync(password, saltRounds)
    builder.update('password', hash)
  } 

  builder.then(() => {
    let _b = req.db.from('users');

    _b.select('*');

    _b.where('id', '=', req.decoded.user.id)
      .then((rows) => {
        if (rows.length == 0) {
          return res.status(401).json({
            "error": true,
            "message": "User not found"
          })
        }
        let user = rows[0]
        delete user.password
        res.json(user);

      }).catch(err => {
        res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
      })

  }).catch(err => {
    console.log(err);
    res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
  })

})

module.exports = router;
