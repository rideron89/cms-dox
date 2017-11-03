const express  = require('express')
const history  = require('connect-history-api-fallback');
const markdown = require('markdown').markdown
const sqlite   = require('sqlite3').verbose()

var app = express()
var db  = new sqlite.Database('data/wordpress.sqlite')

app.use(history())
app.use(express.static('public'))

app.get('/api/titles', function(req, res) {
    db.all(`SELECT title FROM actions`, function(err, action_rows) {
        if (err) {
            console.log(err)
            return res.send({ error: true, data: err })
        }

        db.all(`SELECT title FROM functions`, function(err, function_rows) {
            if (err) {
                console.log(err)
                return res.send({ error: true, data: err })
            }

            res.send({ error: false, data: {
                actions: action_rows.map(r => r.title),
                functions: function_rows.map(r => r.title)
            } })
        })
    })
})

/**
* Retrieve the content for a single title.
*
* Ex: GET /api/functions/$post
*/
app.get('/api/:table/:title', function(req, res) {
    let title = decodeURIComponent(req.params.title)

    db.get(`SELECT content FROM ${req.params.table} WHERE title = "${title}"`, function(err, row) {
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
