const express = require('express')
const path = require('path');
var bodyParser = require('body-parser');
const exec = require("child_process").exec;
const fs = require("fs");
const mustacheExpress = require("mustache-express");

const app = express()
const port = 3000
const TOKEN_MAX = 1000000000
const __views = path.join(__dirname, "public", "views")

const pre_path = "./pre";
const python_path = "/usr/bin/python";

function getToken() {
    return Math.floor(Math.random() * Math.floor(TOKEN_MAX));
}

app.engine('html', mustacheExpress());
app.set('view engine', 'html');
app.set('views', __views)

app.use(express.static("public"));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.render("index.html");
})


app.post('/final', (req, res) => {
    var input = req.body.input20;
    var i = 0;
    content = "";
    while (req.body["input" + i] != undefined)
    {
        txt = req.body["input" + i];
        if (txt.substr(txt.length-7) == "<<out>>")
        {
            
            txt = txt.substr(0, txt.length-7);
    
            var token = getToken();
            var name = token + ".txt";
    
            var url = path.join(pre_path, name);
    
            fs.writeFileSync(url, txt);
            exec(python_path + ` -m src backit ${url}`, function(error, stdout, stderr) {
                if (error != null)
                    console.log(error);
                console.log(stdout);
                // console.log(stderr);
            });
        }
        else
        {
            content += txt + " ";
        }
        i++;
    }
    res.render("result.html", {"content": content});
});


app.post('/submit', (req, res) => {
    var quick = req.body.submit == "Quick Submit";
    var text = req.body.text;
    var ratio = req.body.ratio;

    if (quick)
    {
        console.log("Quick submit was requested!");

        var token = getToken();
        var name = token + ".txt";
        var meta = token + ".meta";

        var url = path.join(pre_path, name);
        var metaurl = path.join(pre_path, meta);

        fs.writeFileSync(url, text);
        fs.writeFileSync(metaurl, ratio);

        exec(python_path + ` -m src "${url}" "${metaurl}"`, function(error, stdout, stderr) {
            if (error != null)
                console.log(error);

            fs.unlinkSync(url);
            fs.unlinkSync(metaurl);

            res.render("result.html", {"content": stdout});
        });
    }
    else
    {
        console.log("Normal submit was requested!");
        
        var token = getToken();
        var name = token + ".txt";
        var meta = token + ".meta";

        var url = path.join(pre_path, name);
        var metaurl = path.join(pre_path, meta);

        fs.writeFileSync(url, text);
        fs.writeFileSync(metaurl, ratio);

        exec(python_path + ` -m src "${url}" "${metaurl}"`, function(error, stdout, stderr) {
            if (error != null)
                console.log(error);

                

            chunks = stdout.split("\n");
            

            var content = {"sentences": []};
            for(var i=0; i<chunks.length; i++)
            {
                if (chunks[i].length <= 2) continue;
                content["sentences"].push({"content": chunks[i], "ord": "input" + i.toString()})
            }
            res.render("editor.html", content);
        });

    }
});


app.listen(port, () => {
    console.log(`Example app listening on port ${port}!`)
})