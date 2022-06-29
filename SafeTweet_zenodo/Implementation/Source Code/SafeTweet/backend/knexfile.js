const { attachPaginate } = require('knex-paginate');
attachPaginate();

module.exports = {
    client: 'mysql',
    connection: {
        host: 'localhost',
        port: 3306,
        user: 'root',
        password: '123456',
        database: 'safetweets',
        charset : 'utf8mb4'
    },
    useNullAsDefault: true,
    migrations: {
        diractory: './data/migrations',
    },
    seeds: {
        directory: './data/seeds'
    }
}