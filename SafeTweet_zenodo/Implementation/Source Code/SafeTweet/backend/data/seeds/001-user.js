const bcrypt = require('bcrypt');

exports.seed = function(knex) {
  // Deletes ALL existing entries
  return knex('users').del()
    .then(function() {
      // Inserts seed entries
      const saltRounds = 10;
      const hash = bcrypt.hashSync('admin', saltRounds)
      return knex('users').insert([
        { id: 1, username: 'admin', avatar: '', stu_id: 'a1000101', email: 'admin@gmail.com', password: hash, role: 1, u_status: 1 },
        { id: 2, username: 'Kell', avatar: '', stu_id: 'a1000102', email: 'user@gmail.com', password: hash, role: 0, u_status: 1 },
        { id: 3, username: 'Molly', avatar: '', stu_id: 'a1000103', email: 'test@gmail.com', password: hash, role: 0, u_status: 1 },

      ]);
    });
};
