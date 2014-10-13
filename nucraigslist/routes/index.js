var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res) {
  res.render('index', { title: 'Express' });
});


/* GET Userlist page. */
router.get('/posts', function(req, res) {
    var db = req.db;
    var collection = db.get('posts');
    collection.find({},{},function(e,docs){
        res.render('posts', {
            "posts" : docs
        });
    });
});

module.exports = router;
