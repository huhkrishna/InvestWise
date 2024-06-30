const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database(':memory:');

db.serialize(() => {
  db.run("CREATE TABLE accounts (accountNumber TEXT, password TEXT)");
  
  const stmt = db.prepare("INSERT INTO accounts VALUES (?, ?)");
  stmt.run("123", "john");
  stmt.run("456", "jane");
  stmt.finalize();
});

module.exports = db;
