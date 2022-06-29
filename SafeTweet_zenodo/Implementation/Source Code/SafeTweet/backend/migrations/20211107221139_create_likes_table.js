
exports.up = function(knex) {
    return knex.schema.createTable('likes', table => {
        table.increments('id').primary();
        table.integer('user_id').unsigned().nullable()
        table.integer('tweet_id').unsigned().nullable()
        table.foreign('user_id').references('users.id');
        table.foreign('tweet_id').references('tweets.id')
    })
};

exports.down = function(knex) {
    return knex.schema.dropTable('likes');
};
