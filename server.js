const markdown = require('markdown').markdown
const sqlite   = require('sqlite3').verbose()
const express  = require('express')

var app = express()
var db  = new sqlite.Database('data/wordpress.sqlite')

app.use(express.static('public'))

/**
* Retrieve all the titles.
*
* Ex: /api/titles
*/
app.get('/api/titles', function(req, res) {
    db.all('SELECT title FROM functions', function(err, rows) {
        if (err) {
            return res.send({ error: true, data: err })
        }

        res.send({ error: false, data: rows.map(r => r.title) })
    })
})

/**
* Retrieve the content for a single title.
*
* Ex: GET /api/title/$post
*/
app.get('/api/title/:title', function(req, res) {
    let title = decodeURIComponent(req.params.title)

    db.get('SELECT content FROM functions WHERE title = "' + title + '"', function(err, row) {
        if (err) {
            return res.send({ error: true, data: err })
        }

        res.send({ error: false, data: row })
    })
})

/**
* Start the server.
*/
db.serialize(function() {
    const port = process.env.PORT || 3000

    app.listen(port, () => console.log('Server listening on port', port))
})
