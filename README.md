# cms-dox

Single-page app for browsing various CMS library documentation, much like the incredible [DevDocs](http://devdocs.io/).

Demo: http://cms-dox.herokuapp.com/

## Building a database

Instructions for building databases can be reviewed in the sections below.

#### WordPress

Use the following steps to build the database for WordPress:

1. Go to [this page](https://codex.wordpress.org/index.php?title=Special:Export&action=submit) to start the Export process
2. Enter `Functions` into the search box, and click `Add`
3. Go through the list and remove any lines you do not want (recommendation: remove all entries starting with `User:`)
4. Click `Export` to save the pages in `.xml` format
5. From the project directory, run `python db-loader.py [path to the file you downloaded]`

This will create the following SQLite database file: `data/wordpress.sqlite`.
