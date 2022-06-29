const jsonwebtoken = require('jsonwebtoken');

module.exports = {
    authorize: (req, res, next) => {

        let token;
        if (req.headers.authorization && req.headers.authorization.split(' ')[0] === 'Bearer') {
            token = req.headers.authorization.split(' ')[1];
        } 
        if (!token) {
            return res.status(401).json({
                error: true,
                message: "Miss token"
            })
        }
        
        try {
            const secretKey = require('./constants').secretKey;
            const decoded = jsonwebtoken.verify(token, secretKey)
            req.decoded = decoded;
            if (decoded.exp < Date.now()) {
                return res.status(401).json(errors.TokenExpired)
            }
            next();
        } catch (e) {
            return res.status(401).json(errors.InvalidJWT)
        }
    }
}