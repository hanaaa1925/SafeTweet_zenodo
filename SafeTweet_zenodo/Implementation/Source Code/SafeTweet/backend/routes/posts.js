const express = require('express');
const router = express.Router();
const middleware = require('../middlewares');
const {PythonShell} = require('python-shell');

router.get('/test', function(req, res) {
    
    return req.db.from('tweets')
    .join('users', 'users.id', '=', 'tweets.user_id')
    .select('tweets.*', 'users.avatar', 'users.username')
    .whereRaw(`users.company <> "q"`)
    .orderBy('created_at', 'desc').then((tweets) => {
        return res.status(200).json(tweets)
    }).catch(err => {
        console.log(err)
        res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
    })
    
});


router.get('/', function(req, res) {
    return req.db.from('tweets')
    .join('users', 'users.id', '=', 'tweets.user_id')
    .select('tweets.*', 'users.avatar', 'users.username')
    .orderBy('created_at', 'desc').then((tweets) => {
        return res.status(200).json(tweets)
    }).catch(err => {
        console.log(err)
        res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
    })
});


router.put('/company/:company', middleware.authorize, async function(req, res) {
    const { company } = req.params;
    const user_company = req.decoded.user.company;

    return req.db.from('tweets')
    .join('users', 'users.id', '=', 'tweets.user_id')
    .select('tweets.*', 'users.avatar', 'users.username')
    .whereRaw(`users.company <> ${company}`)
    .orderBy('created_at', 'desc').then((tweets) => {
        return res.status(200).json(tweets)
    }).catch(err => {
        console.log(err)
        res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
    })
});

router.get('/open', function(req, res) {
    return req.db.from('tweets')
        .where({'is_anonymous': 0})
        .join('users', 'users.id', '=', 'tweets.user_id')
        .select('tweets.*', 'users.avatar', 'users.username')
        .orderBy('created_at', 'desc').then((tweets) => {
            return res.status(200).json(tweets)
        }).catch(err => {
            console.log(err)
            res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
        })
});

router.post('/check', function(req, res) {
    const { content } = req.body;
    let options = {
        mode: 'text',
        pythonPath: '/usr/local/bin/python3.7',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: 'python',
        args: content
    };
    PythonShell.run('ner.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        if (!results) {
            message = "Safe!"
        } else {
            message = results
        }
        console.error('results: \n', results);
        return res.send({ message })
    })
})

router.post('/', middleware.authorize, function(req, res) {
    const { content, is_anonymous, is_encryption } = req.body

    return req.db.insert({ content, is_anonymous, is_encryption, user_id: req.decoded.user.id }, 'id')
        .into('tweets').then(() => {
            return res.status(200).json({
                "message": "Tweet created"
            })
        }).catch(err => {
            console.log(err)
            res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
        })
});

router.put('/like/:id', middleware.authorize, async function(req, res) {
    const { id } = req.params;
    const user_id = req.decoded.user.id;
    let liked = await req.db.from('likes').whereRaw(`user_id = ${user_id} AND tweet_id = ${id}`)

    if (liked[0]) {
        return res.status(409).json({ "error": true, "message": "You have liked" })
    } else {
        await req.db.from('tweets').whereRaw(`id = ${id}`)
            .update({
                'likes': req.db.raw('likes + 1')
            });
        await req.db.insert({ user_id, tweet_id: Number(id) }, 'id').into('likes')
        return res.status(200).json({ "message": "liked" })
    }
});

router.put('/fav/:id', middleware.authorize, async function(req, res) {
    const { id } = req.params;
    const user_id = req.decoded.user.id;
    let fav = await req.db.from('favourites').whereRaw(`user_id = ${user_id} AND tweet_id = ${id}`)

    if (fav[0]) {
        await req.db.from('tweets').whereRaw(`id = ${id}`)
            .update({
                'favourites': req.db.raw('favourites - 1')
            });
        await req.db.delete({ user_id, tweet_id: Number(id) }, 'id').from('favourites')
        return res.status(200).json({ "message": "Cancel favourite" })
    } else {
        await req.db.from('tweets').whereRaw(`id = ${id}`)
            .update({
                'favourites': req.db.raw('favourites + 1')
            });
        await req.db.insert({ user_id, tweet_id: Number(id) }, 'id').into('favourites')
        return res.status(200).json({ "message": "favourite" })
    }
});

router.get('/:id', middleware.authorize, function(req, res) {
    const builder = req.db.from('tweets').join('users', 'users.id', '=', 'tweets.user_id').where('tweets.user_id', req.decoded.user.id)
    builder.select('*', 'tweets.id as id')
        .then(async (rows) => {
            res.json(rows)
        }).catch(err => {
            console.log(err);
            res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
        })
});

router.get('/search/:key', function(req, res) {
    const builder = req.db.from('tweets').join('users', 'users.id', '=', 'tweets.user_id')
    .where('tweets.content', 'like',`%${req.params.key}%`)
    builder.select('*', 'tweets.id as id')
        .then(async (rows) => {
            res.json(rows)
        }).catch(err => {
            console.log(err);
            res.status(500).json({ "Error": true, "message": "Error in MySQL query" })
        })
});




module.exports = router;
