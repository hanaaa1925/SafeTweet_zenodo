
exports.up = function(knex) {
    return knex.schema.createTable('comments', table => {
        table.increments('id').primary();
        table.text('content').notNullable();
        table.boolean('is_anonymous');
        table.integer('user_id').unsigned().nullable()
        table.integer('tweet_id').unsigned().nullable()
        table.timestamp('created_at').defaultTo(knex.fn.now())
        table.timestamp('updated_at').defaultTo(knex.fn.now())

        table.foreign('user_id').references('users.id');
        table.foreign('tweet_id').references('tweets.id')
    })
};

exports.down = function(knex) {
    return knex.schema.dropTable('comments');
};
