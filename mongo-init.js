db = db.getSiblingDB('ComponentStock');
db.createUser(
  {
    user: 'root',
    pwd: 'root',
    roles: [{ role: 'readWrite', db: 'ComponentStock' }],
  },
);
