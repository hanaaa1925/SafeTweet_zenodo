const express = require('express');
const router = express.Router();
const middleware = require('../middlewares');

router.post('/', middleware.authorize, async function(req, res) {
    const { is_anonymous, content, tweet_id, id } = req.body;
    const user_id = req.decoded.user.id;

    return req.db.insert({ is_anonymous, content, tweet_id, user_id }, 'id')
        .into('comments').then(() => {
            return res.status(200).json({
                "message": "comment created"
            })
           
        }).catch(err => {
            console.log(err)
            res.status(500).json({ "Error": true, "Message": "Error in MySQL query" })
        })
});

router.get('/:id', function(req, res) {
    const { id } = req.params;
    const builder = req.db.from('comments').innerJoin('users', 'users.id', '=', 'comments.user_id')
    builder.select('*','comments.id as id', 'comments.created_at as created_at').where('comments.tweet_id', id)
        .orderBy('comments.created_at', 'desc')
        .then(async (data) => {
            res.json(data)
        }).catch(err => {
            console.log(err);
            res.status(500).json({ "Error": true, "Message": "Error" })
        })
});



module.exports = router;