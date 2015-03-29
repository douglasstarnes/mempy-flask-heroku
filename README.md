#Deploying a Flask app to Heroku
At the MEMpy meeting in March, we saw how to create and deploy a simple Flask application to Heroku using the Cloud9 IDE.  What follows is a detailed description of how to recreate a similiar application.

####What you'll need
Before you begin you'll need to sign up for a few online services:

 * Github - If you haven't created a Cloud9 account yet, you can easily do so with Github
 * Cloud9 - Use your Github account to log in
 * Heroku - This is the cloud hosting service
 * MongoLab - This is the database

######Github
The home page for Github is [github.com](http://github.com).  We won't be using Github for in this tutorial for anything other than creating a Cloud9 account.  If you already have a Github account, you can skip to the next section.  Otherwise, go to the Github home page and create a new account.  You'll have to verify your email address by clicking on a link in an email they will send to you.  After that, you're ready to move on to Cloud9.

######Cloud9 IDE
This is the browser-based development environment we will be using.  It's completely free to use except there is one note of caution I like to reiterate.  **In the free Cloud9 workspaces, all code is public read-only.**  This means that you should not hardcode sensitive data like OAuth tokens or API keys (and you shouldn't do this anyway).  We'll see a better way of doing this when we get to MongoLab.

The Cloud9 home page is [c9.io](http://c9.io).  You can use your Github account (see the previous section) to create a Cloud9 account.  Just click on the icon that looks like the silhouette of a cat next to the _SIGN IN_ button:

![Sign in to Cloud9 with Github](readme_images/c9signin.png)

If you already have a Cloud9 account associated with Github you'll be taken to the dashboard.  Otherwise, a page will appear asking you to authorize Cloud9 to use your Github account.  Once you agree, you'll be taken to the dashboard.

######Heroku
Heroku is a cloud web application hosting provider.  We will use Heroku to serve our application.  Heroku is free just like Github and Cloud9 (or at least it has a free plan which will be more than enough for our simple application.) but you can't use Github to log in.  So you'll need to go to the Heroku homepage at [heroku.com](http://heroku.com) and create an account.  The process is similar to Github and you'll need to verify your email by clicking on a link they will send you in an email.  

One note about Heroku, it also has paid plans.  By default, you get 5 applications and a limited number of add on services (such as databases) for free.  However, if you verify your account with a credit card, they will give you 100 application and more add ons.  This will make adding MongoDB support much easier.  However, I understand that not everyone will want to do this so I have included the instructions for using MongoLab with Heroku without a verified account.

######MongoLab
MongoLab is the host for the database that we will use.  This database is called MongoDB.  If you haven't worked with MongoDB or it's relatives (collectively referred to as NoSQL) it's quite different from other databases you might have used in the past.  However, it's super simple to use, is pre-installed on Cloud9 for testing purposes, has an excellent Python library and is free!  So just like Heroku, you can't use Github to login.  You'll need to go to the MongoLab home page at [mongolab.com](http://mongolab.com) and create an account.  After that, head back to Cloud9 and we'll start coding!

####Setting up Cloud9
There is not a lot to do here because most everything is preinstalled but there are a few things we need to do.  First we have to create a new workspace.  When you log in to Cloud9, you'll be taken to the dashboard which has a list of your workspaces on the left.  By default, Cloud9 creates a demo project workspace for you, but we are going to create one from scratch.  So click the green _CREATE NEW WORKSPACE_ button in the upper left and then on the _Create a New Workspace_ link in the pop up menu:

![Create a new Cloud9 workspace](readme_images/createc9wkspc.png)

You'll be presented with the _Create a New Workspace_ dialog:

![Create a New Workspace](readme_images/createwkspcdialog.png)

1. Give your workspace a name.  This name does not have to be unique across Cloud9, only to your account so you can use _mempydemo_ like shown above.
2. Select _Open and Discoverable_ for _Workspace Privacy_.  This is the option for free workspaces.
3. For _Hosting_ select _Hosted_.  Again, this is for the free workspaces.
4. Select _Custom_ for the workspace type.  This will give us a blank workspace without any opinions as to the framework or language we will be using.
5. Click the green _CREATE_ button.

A new entry in the left pane will come up with your workspace name and a spinning gear.  This means Cloud9 is creating the workspace.  It should only take a few seconds.  Cloud9 is very fast!

![Workspace pending](readme_images/c9working.png)

When Cloud9 is finished you can click the green _START EDITING_ button in the right side of the window.

![Begin editing](readme_images/c9beginediting.png)

Below is a picture of the default layout for the Cloud9 IDE:

![C9 workspace](readme_images/c9workspace.png)

1. The project manager that shows a tree view of the files in this workspace.
2. An editor similar to Sublime Text with optional vim bindings.
3. A Linux terminal with sudo access.

There are only a few more things we need to do to get set up and all of them can be done from the terminal.

First, since the maintainers of Python are investing all new development in Python 3, we should use that.  However, the default version of Python installed on Cloud9 workspaces (which are running on top of Ubuntu 14.04) is 2.7.6 (feel free to verify this by running `python --version` in the terminal).  So we are going to create a _virtual environment_ which is a special instance of Python that thinks it is the default version.  Virtual environments can have their own Python version and implementation as well as their own set of packages (libraries) installed.  Fortunately, Cloud9 includes the virtual environment scripts for us.  So to create a virtual environment with Python 3, run the following command in the terminal:
```
mkvirtualenv --python=`which python3` mempydemo
```
> Don't like to type?  Just type the first few letters of a long command (ie. 'mkv') and press TAB.  The terminal will complete it for you!

You'll see some output similar to this:
```
Running virtualenv with interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in mempydemo/bin/python3
Also creating executable in mempydemo/bin/python
Installing setuptools, pip...done.
```
The last parameter is the name of the virtual environment.  You can use any name you want but since this is specific only to the workspace, you can use _mempydemo_ to make it easier to follow along.  Notice that the prompt in the terminal is now prefixed with the name of the virtual environment in parentheses.  This means you are inside a virtual environment.  To verify this run the command `python --version` again and you should see a variant of Python 3, 3.4.0 as of this writing.

To leave a virtual environment, run the command `deactivate`.  The prefix willbe removed from the prompt and Python 2.7.6 will be the default version again.  Again, check this with `python --version`.  To enter the virtual environment, run `workon mempydemo` (or whatever you named your virtual environment) and you'll see the environment is now active again.

If you look at the output from `mkvirtualenv` the last line says it installed an application called `pip`.  This is a package manager that will retrieve and install Python packages and their dependencies from the internet.  We are going to use it to install Flask, the web framework we will use to write our application.  Run this command in the terminal:

```
pip install Flask
```

This will create a lot of output and you don't need to worry about it as long as there are no errors.  However, notice that at the end of the output it installed Flask as well as four other packages.  These are packages that Flask depends on.  Also, just before that, pip compiled a native C extension that one of the packages uses.  Cloud9 is set up for you to do this.  Otherwise, you would have had to install some prerequisite development libraries.  Cloud9 helps you out more than you think!

We'll install some more packages later but this will get us started.  Let's go ahead an write a simple application.

####Our first application
We need to create a new Python file to hold our code.  This can be done in many ways.  You can create a new file through the IDE by selecting _File -> New File_ from the menu, by right clicking on a folder in the project manager and by click the plus (+) tab in the editor:

![The plus tab](readme_images/plustab.png)

My preferred way is to create new files in the terminal.  To do this make sure you are in the _workspace_ directory in your home directory (`cd ~/workspace` to move there) and then run `touch main.py` where _main.py_ is the name of the file to create.  Then double click on that file in the project manager.  If you don't see it you may have to refresh the file tree which you can do by clicking on the gear in the project manager and selecting _Refresh File Tree_.

![Refresh File Tree](readme_images/refreshfiletree.png)

The following code will comprise our application:

```python
from flask import Flask
import os

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return 'Hello MEMpy'

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)
```

We'll go more in depth with Flask later but for a quick look at the code.  The first two lines import packages, namely Flask and os which we use in the entry point to get values for environment variables.  The next two lines create an instance of Flask and turn on debugging so that if (when) errors happen we will see a nice stack trace in the browser.  (Of course this should __NEVER__ be enabled in a production application.)  The `route()` decorator tells Flask that when it receives a request for the root of the site to invoke the `index()` function.  That function merely returns a string which Flask will wrap in an HTTP response and send back to the browser.  The entry point extracts values for environment variables named _PORT_ and _IP_.  This is because if the application is started on a certain port and ip address that Cloud9 has reserved, the application will be accessible to the public web via a special URL.  These are stored in the environment variables.  The last line starts Flask on the port and ip we retrieved before.

To start this app, just run `python main.py` in the terminal.  You should see the following output:
```
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
```
The first line tells us the server did indeed start.  And the second line shows is running in debug mode.

Now let's access our application from a browser.  The URL we can use for our applcation is of the form:

`[workspace]-c9-[username].c9.io`

For example, my workspace name is _mempydemo_ and my username is _douglasstarnes_ so the URL for my application would be

`http://mempydemo-c9-douglasstarnes.c9.io`

Navigating to the URL for the application should yield the message 'Hello MEMpy'.

![Hello MEMpy](readme_images/hellomempy.png)

To stop the server press _Ctrl-c_ in the terminal.

Also, after you close the browser, the workspace will become idle and the process running the server will be terminated.  Obviously, this is not intended for long term hosting.  For a robust hosting solution, we'll turn to Heroku.


####Deploying to Heroku
Before we can deploy our application to Heroku there is some set up involved.  Fortunately, this only has to be done once for the application.  The first step is to log in to Heroku via the scripts in the Heroku Toolbelt.  Normally, we would need to install this manually but Cloud9 has pre-installed it in the workspace for us.  So run the following command in the terminal:
```
heroku login
```
You'll be asked to provide the email address and password that you used to sign up with.  After that, you'll be able to use the `heroku` command to create and manage deployments.

Before that, we need to prepare our application for deployment.  We'll create some files to give Heroku information as to how to install and configure our application.  The first file is called `runtime.txt` and merely contains the version of Python that the application requires.  To reiterate, run `python --version` in the terminal to see the current version of Python.  The output I got when writing this is:
```
Python 3.4.0
```
So create a new file in the same directory as `main.py` and call it `runtime.txt`.  The contents is a single line.  In my case for Python 3.4.0 it is:
```
python-3.4.0
```
The next file is called `Procfile` and it tells Heroku the command to run to start the server.  In our case it is simply: `python main.py`.  The contents of `Procfile` should be:
```
web: python main.py
```
The last file tells Heroku what dependencies the application requires.  These were installed for us automatically when we installed Flask with pip.  And we can retrieve what pip installed with the command `pip freeze`.  The output you get should be similar to this: (your version numbers may differ)
```
Flask==0.10.1
Jinja2==2.7.3
MarkupSafe==0.23
Werkzeug==0.10.4
itsdangerous==0.24
```
The file Heroku looks for to determine what dependencies to install is called `requirements.txt`.  We could just copy the output of `pip freeze` into a new file but there is an easier way.  Linux will let you _redirect_ the output of a command to a file.  So for our needs the command
```
pip freeze > requirements.txt
```
will suffice.

######Git
Git is a version control system.  As you work on your project you will _commit_ changes at various stages to a Git _repository_ on your local machine and Git will keep track of those changes and also allow mulitple people to work on the same project without silently overwriting each other's work.  However, we are going to use Git for deploying our application to Heroku's servers.  When you are ready to send committed changes to a remote master repository, you do a _push_ to the server.  When you push changes to Heroku's server, it will also trigger the deployment process of copying files, installing dependencies and starting the application.  So let's set up Git.

Again, Cloud9 has made this easy by installing Git in the workspace for you.  So the first thing we need to do is make sure the current directory is the root of the workspace (`~/workspace`) and initialize it as a Git repository with the command:
```
git init .
```
The last parameter is the directory to use or '.' (dot) for the current directory.

Then we need to tell Git which files to add to this repository.  We can just add all of them with the command:
```
git add .
```
Finally, we need to commit the changes to the local Git repo with the command:
```
git commit -m 'initial commit'
```
The parameter to the -m (for _message_) flag allows you to provide some text to describe the changes in this commit.  You should get in the habit of doing this.  Commits are not always large changes so you shouldn't need much text.  However, we can use some dummy text like above for now.

######Push to Heroku
The commands `git add` and `git commit` have come to be known as part of the 'check in dance'.  The last step is to push the committed changes to the remote server, Heroku in this case.  First, we have to tell Git where that server is.  Heroku makes this very easy for you.  When you create a new app on Heroku, it will create a Git _remote_ that will specify the address of a remote repository that Heroku has set up for your application.  To create a new app use the `apps:create` command:
```
heroku apps:create [app-name]
```
You can omit the app-name and heroku will generate one for you or you can provide one.  However, if you provide one it must be unique across Heroku so you might have to try a few times to find one that is not in use.

The `apps:create` command will set up the remote which you can view with the command `git remote -v` (v for verbose).  You will see that it created a remote called _heroku_.  That will obviously be the source.  We also need to provide a destination for Git on Heroku which will be called _master_.  Heroku also set that up for us.  So the command to push the application to Heroku ends up being:
```
git push heroku master
```
This will take a little while and product a lot of output.  You'll see that it will detect the Python version in `runtime.txt` and then install the dependencies from `requirements.txt`.  Then it will launch the application and verify the deployment.  After that, assuming everything worked, it will return to the command line without error.  

To see our application on the web, we have a URL reserved for us in the form:
`[app-name].herokuapp.com`
I called my app _mymempydemo_ so the URL to my app is `http://mymempydemo.herokuapp.com/`.

![Hello Heroku](readme_images/helloheroku.png)

If that seemed like a lot of steps, it was but most them only have to be done once for the application.  In the future, when we make changes we'll only need to add any new files and then commit the changes and push them.  So the check-in dance ends up being:
```
git add .
git commit -m 'message'
git push heroku master
```
And you don't have to push after every commit.  Git will aggregrate the commits and push all made since the last push.

####Connecting to MongoDB

######MongoLab
In the beginning of this tutorial, you created an account with a service called MongoLab.  Now we will set up a MongoDB database in MongoLab.  Log into your MongoLab account at [mongolab.com](http://mongolab.com).  The section _MongoDB Deployments_ will be empty.  Click on the _Create new_ button.
![Create MongoDB](readme_images/createmongodb.png)
On the next page, under _Create new subscription_ select the following options:
![Create new subscription](readme_images/newsubscription.png)

1. For the _Cloud provider_ select any of the providers available.  I selected Amazon Web Services.
2. Under _Plan_ be sure to select _Single-node_.  This is the only option with a free quota.
3. Select the _Sandbox_ plan, which is free.

Give your database a name and click the _Create_ button.

You'll see the deployments page again with the newly created database.

![New DB](readme_images/mempydemomongo.png)

Now we need to create a new user for the database to access it remotely.  Click on the new database.  You'll see the following page.  There will be a message telling you to create a new user.  Click the link that is highlighted to create a new user.

![Create new user](readme_images/createnewuser.png)

A short dialog will appear asking for a username and password for the new user.

Back in the database page, you'll see a URI of the form:
```
mongodb://<dbuser>:<dbpassword>@<host>:<port>/<db>
```
We will use this URI to connect to MongoDB from Python via a package called MongoEngine.  But first, we need to have a way for Python to know about the URI.  We could store it in a Python constants file but then that would make it visible to the world as we are using the free workspaces on Cloud9.  However, we can use an environment variable to store the URI.  Set up a new environment variable on Heroku using the web interface at [heroku.com](http://heroku.com).

Log in to Heroku and you'll be taken to the dashboard where you'll see the app you created from before.  

![Heroku dashboard](readme_images/herokudb.png)

Click on it and then on _Settings_ tab.

In Settings you'll see a section named _Config Variables_.  Click on that link to show the config variables and then on the _Edit_ button on the right.  Create a new variable with the _KEY_ set to `MONGOLAB_URI` and the _VALUE_ set to the URI from MongoLab.  You'll need to substitute the username and password with those you created for the new database.  Then click the _Save_ button.

That's got MongoDB set up on MongoLab and Heroku.  But MongoLab is our production database that is live on the web.  We want to be able to have a test database that we can experiement with during development.  Fortunately, Cloud9 has thought ahead for us and has preinstalled MongoDB on our instance.  Let's get that set up next.

######MongoDB on Cloud9
The best way to set up MongoDB on Cloud9 is the steps on this page in the Cloud9 documentation which I've reproduced below: [https://docs.c9.io/v1.0/docs/setting-up-mongodb](https://docs.c9.io/v1.0/docs/setting-up-mongodb)

In the root of your workspace (`~/workspace`), create a new directory called 'data' with the following command in the terminal:
```
mkdir data
```

Then run the following command to make a script that will start MongoDB:
```
echo 'mongod --bind_ip=$IP --dbpath=data --nojournal --rest "$@"' > mongod
```

Finally make the script executable:
```
chmod a+x mongod
```

Now run the script to start MongoDB:
```
./mongod
```

You'll have to open a new terminal tab to continue because the you can't use the current one without stopping MongoDB.  To do this, click on the (+) tab at then end of the tab bar for the terminal and select _New Terminal_:

![New terminal](readme_images/newterminal.png)

Also, the new terminal will not have the virtual environment activated so you'll need to use the `workon` command to activate the virtual environment you created before.

######MongoEngine
Now we need to install mongoengine, the Python package that will connect to MongoDB.  We will use pip to do this:
```
pip install mongoengine
```

We also need to update the `requirements.txt` file so that the next time we push to Heroku, mongoengine will be installed on the server:
```
pip freeze > requirements.txt
```

Now we can test MongoEngine.  I'll do this in a new file that I'll call `test_mongo.py`.  This isn't standard practice but it will be OK for experimentation.

In my test file I will first connect to the database.  Mongoengine provides a function `connect()` that we can import from the `mongoengine` package.  So at the top of the file:
```
from mongoengine import connect
```

Then in the entry point call the `connect()` function and pass it the name of the database to use.  This will connect to the test instance of MongoDB we just set up.  (Before we push to Heroku, we will set the application up to connect to MongoLab.)  We can use any database name for testing and MongoDB will create it for us:

```python
if __name__ == '__main__':
    connect('mempydemo')
```

Now we need to tell MongoDB what data we want to store. We will keep it very simple and store shapes with two properties: a name (which will be a string), and a number of sides (an integer).  We will do this in a Python class.  However, MongoEngine gives us a class that tells MongoDB how to load, save and do other things with data.  This class is called `Document`.  We'd like to use that so our class will inherit from `Document`:

```python
class Shape(Document):
    name = StringField()
    sides = IntField()
```

`Document`, `StringField`, and `IntField` are also in the `mongoengine` package so we need to import them as well:

```
from mongoengine import connect, Document, StringField, IntField
```

Back in the entry point, we'll create a couple of `Shape` objects.  Then we'll call the `save()` method inherited from `Document` to persist the changes to MongoDB:
```python
square = Shape('square', 4)
octagon = Shape('octagon', 8)
circle = Shape('circle', 1)
point = Shape('point', 0)

square.save()
octagon.save()
circle.save()
point.save()
```

Here is the entire code for the test file:
```python
from mongoengine import connect, Document, StringField, IntField

class Shape(Document):
    name = StringField()
    sides = IntField()
    
if __name__ == '__main__':
    connect('mempydemo')
    
    square = Shape('square', 4)
    octagon = Shape('octagon', 8)
    circle = Shape('circle', 1)
    point = Shape('point', 0)

    square.save()
    octagon.save()
    circle.save()
    point.save()
```

> You might notice the red x's in the gutter in the Cloud9 editor.  This is Cloud9 complaining that it can't find the method `save()` on the `Shape` objects.
>
> ![Editor 'error'](readme_images/xsc9editor.png)
> 
> However, this is not an error in this case.  The x's can be ignored.  The dynamic nature of Python makes static analysis difficult at times.  

To run this test file, execute the command:
```
python test_mongo.py
```

If if looked like nothing happened, and there were no errors, then it likely worked.  To see the data in the database we need to connect to it with the `mongo` command line app.  So in the terminal run the command:
```
mongo
```


You'll see some output similar to this: (ignore any warnings about the rest interface)
```
MongoDB shell version: 2.6.7
connecting to: test
Server has startup warnings: 
2015-03-28T23:25:19.828+0000 ** WARNING: --rest is specified without --httpinterface,
2015-03-28T23:25:19.828+0000 **          enabling http interface
```

To see if the database was created run the `show dbs` command in the `mongo` shell.  The output will look something like this:
```
admin      (empty)
local      0.078GB
mempydemo  0.078GB
```

We can see that the database was created.  Make it the current database with the `use mempydemo` command.  MongoDB stores data as _documents_ inside of _collections_.  The `Shape` class we created represents a document.  So if we run the `show collections` command in the `mongo` shell we should see a collection for the `Shape` class:
```
shape
system.indexes
```

To see the documents (data) that are inside of a collection, we can call the `find()` method on the collection.  In the `mongo` shell, the variable `db` refers to current database ('mempydemo' in my project).  The collections are just properties on the `db`.  So to get all of the documents in the `shape` collection we would run:
```
db.shape.find()
```

And see something like this:
```
{ "_id" : ObjectId("55173eecbe0cfc0a02a6b18e"), "name" : "square", "sides" : 4 }
{ "_id" : ObjectId("55173eedbe0cfc0a02a6b18f"), "name" : "octagon", "sides" : 8 }
{ "_id" : ObjectId("55173eedbe0cfc0a02a6b190"), "name" : "circle", "sides" : 1 }
{ "_id" : ObjectId("55173eedbe0cfc0a02a6b191"), "name" : "point", "sides" : 0 }
```

Your values for '_id' will definitely vary, but other than that it should be the same.

Now that we have a database server working, we can build out the rest of the app.  If you want to clean up the database and start fresh run:
```
db.dropDatabase()
```
This will delete the database but it will be recreated the next time we connect to it and save a document.  Exit the `mongo` shell with _Ctrl-d_.  Then delete the test file.

####Flask and forms
We're going to create the present day 'Hello world' app which is a todo list.  So first we'll create a form that will let a user create a new todo item.  We'll use an HTML template for this and have Flask display that template on the index page.  Templates in Flask are by default stored in a directory in the root of the application called `templates` so let's go ahead and create it:
```
mkdir templates
```

Next, inside of the `templates` folder, create a new template file called `index.html` and add the following markup to it:
```html
<html>
    <body>
        <h1>Index page</h1>
    </body>
</html>
```

Back in `main.py` import the `render_template` function from the `flask` package.
```
from flask import Flask, render_template
```
This function will take the path of a template relative to the `templates` directory.  It will also optionally take a collection of keyword arguments to populate the template.  Then it will return a string representing the final HTML document.  For starters let's just render the document.  Change the body of the `index()` function:
```python
def index()
    return render_template('index.html')
```

Now we can run the application and look at it in the browser.  You should see something like this:
![Template index](readme_images/templateindex.png)

Let's add the form to the `index.html` template:
```html
<h3>Create a new task</h3>
<form action="" method="post">
    Task: <input type="text" name="task"><br/>
    Days until due: <input type="text" name="duedays"><br/>
    Priority: <input type="text" name="priority"><br/>
    <input type="submit" value="Create Task">
</form>
```
The result should be something like the following:
![Task form](readme_images/taskform.png)

We'll make it look better after we get the application working.

If you try to create a new task now, you'll get an error:
![Task error](readme_images/taskerror.png)

This is because we specified the POST method in the form.  By default, handler functions (such as `index()`) can only handle GET requests.  The `route` decorator accepts a list of methods that the handler function can handle:
```python
@app.route('/', methods['GET', 'POST'])
def index():
    return render_template('index.html')
```

Make this change, save `main.py` and the server will restart.  Now you can click the button and get no errors.  But nothing appears to have happened.  That's because we are not watching for a POST request in the handler function.

To detect POST requests, we'll need to import a object from `flask` called `request`:
```
from flask import Flask, render_template, request
```

This object will always represent the current HTTP request.  It has a `method` property that will hold the method of the current request such as 'GET' or 'POST'.  If the method is a GET request, we'll return the template.  If it is a POST request, we'll use the `form` property of `request` to access the form values.  This `form` property is a dictionary like object that we can use to access the form values by name.  So the `index()` function now looks like this:
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        return 'task: {0}, days til due: {1}, priority: {2}'.format(
            request.form['task'],
            request.form['duedays'],
            request.form['priority'])
```
Save `main.py` and the server will restart.  Then the form should work as in the following screengrabs:

![Task before](readme_images/taskbefore.png)
---
![Task after](readme_images/taskafter.png)

######Storing the Todo items
Now we have all the pieces that we need to store todo items in MongoDB. So let's implement that next.  

First we need a class deriving from `Document` that will represent a todo item.  The class will have:
 
 * task - string (`StringField`)
 * duedays - integer (`IntField`)
 * priority - integer (`IntField`)
 * complete - boolean (`BooleanField`)

Here is the code for our TodoItem class:
```python
class TodoItem(Document):
    task = StringField()
    duedays = IntField()
    priority = IntField()
    complete = BooleanField()
```

> Don't forget to import `Document`, `StringField`, `IntField` and `BooleanField` from the `mongoengine` package.

At the top of the file, right after creating the Flask app, add a call to `connect()`:
```python
connect('mempydemo')
```

> Don't forget to import `connect` from the `mongoengine` package.

Next, inside of the `index()` function where we handle the POST request, replace the body with the following code:
```python
task = request.form['task']
duedays = int(request.form['duedays'])
priority = int(request.form['priority'])
complete = False

todo = TodoItem(task=task, duedays=duedays, priority=priority, complete=complete)
todo.save()

return redirect('/')
```

First, the `redirect()` function will tell the browser to go to the URL passed to it.  You'll need to import `redirect` from the `flask` package.  Also, we always set `complete` to `False`.  It doesn't make much sense to create todo item that is already complete.

For reference, here is the entire `main.py` file since we have made so many changes:
```python
# main.py (this is a comment)
from flask import Flask, render_template, request, redirect
import os
from mongoengine import connect, Document, StringField, IntField, BooleanField

app = Flask(__name__)
app.debug = True

connect('mempydemo')

class TodoItem(Document):
    task = StringField()
    duedays = IntField()
    priority = IntField()
    complete = BooleanField()
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        task = request.form['task']
        duedays = int(request.form['duedays'])
        priority = int(request.form['priority'])
        complete = False
        
        todo = TodoItem(task=task, duedays=duedays, priority=priority, complete=complete)
        todo.save()
        
        return redirect('/')
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)
```
Save the file to restart the server and try to enter a new task.  It will appear that nothing happened.  So let's run the `mongo` shell and see if we have a TodoItem document in the database:
```
MongoDB shell version: 2.6.7
connecting to: test
Server has startup warnings: 
2015-03-28T23:25:19.828+0000 ** WARNING: --rest is specified without --httpinterface,
2015-03-28T23:25:19.828+0000 **          enabling http interface
> show dbs
admin      (empty)
local      0.078GB
mempydemo  0.078GB
> use mempydemo
switched to db mempydemo
> show collections
system.indexes
todo_item
> db.todo_item.find()
{ "_id" : ObjectId("55175599be0cfc0f89dd46dc"), "task" : "My new task", "duedays" : 7, "priority" : 10, "complete" : false }
```


Sure enough it worked!  Now we need to display a list of the todo items.  The index page is a good place to do that, just before the form to create a new todo item.


#### Displaying a list of TodoItems
Getting the `TodoItem` documents out of the database could not be easier.  The `Document` class has an `objects` property which will get all documents of that type from MongoDB.  So the line:
```python
TodoItem.objects
```

Will get all of the `TodoItem` documents as `TodoItem` inherits from `Document`.  Now we need to send those documents to the template.  So modify the call to `render_template`:
```python 
return render_template('index.html', todos=TodoItem.objects)
```

Now we will use a templating language that is part of the Jinja2 package inside of `index.html` to iterate through `todos` and render the task for each one.  Jinja2 is installed as part of Flask. (`pip freeze` to verify it is installed).  Before the form in `index.html` add this code:
```html
<h3>All Todos</h3>
<ul>
{% for item in todos %}
    <li>{{ item.task }}</li>
{% endfor %}
</ul>
```
As you can see, this reads very much like Python.  The `{% %}` syntax escapes the templating language.  The value inside the double curly braces is rendered as text.  Save all files, the server will restart and if you go to the root of the site ('/') you should see the task you just created:

![Task list](readme_images/tasklist.png)

This is looking good, but there is still more to be done.  It would be nice to be able to mark items as complete, highlight overdue items, sort items by priority and more.  This would be best served with buttons and styling.  Bootstrap makes short of that so we'll tackle it next.  But first, let's push what we have to Heroku.

####Push to Heroku again
We have some prep work to do before we can push to Heroku.  First, there are some files that we don't want to push.  That would be the `data` directory and the `mongod` script.  We can tell Git to ignore these files by placing their paths in a `.gitignore` file.  So create a `.gitignore` file with the following:
```
mongod
data/
.c9/
```
The `.c9` directory is created by Cloud9 so we don't need to send it to Heroku.

Next we need to tell Flask which database to connect to if it is running on Heroku.  Remember that we created an environment variable on Heroku through the web interface called `MONGOLAB_URI` that points to a database on MongoLab's servers.  To check if it exists run this command in the terminal:
```
heroku config
```

And the output will be something like this: (obviously your urls will vary)
```
=== mymempydemo Config Vars
MONGOLAB_URI: mongodb://heroku_app35297401:<your_password_here>@ds059888.mongolab.com:59888/heroku_app35297401
```

This environment variable does not exist on Cloud9 so if we can access it, we can assume we are running on Heroku.  Therefore a simple `if` clause can be added to the top of `main.py` in place of the `connect()` call:
```python
if os.getenv('MONGOLAB_URI') is not None: # on Heroku
    mongolab_uri = os.getenv('MONGOLAB_URI')
    db = mongolab_uri[mongolab_uri.rfind('/')+1:] #extract the database name
    connect(db, host=mongolab_uri)
else: # on Cloud9
    connect('mempydemo')
```

Now we can proceed with the check in dance and push to Heroku:
```
git add .
git commit -m 'push to heroku with mongodb'
git push heroku master
```

You can now go to `[app-name].herokapp.com` and see the application working on Heroku. 
![Tasks on Heroku](readme_images/taskheroku.png)

Also, you can go to [mongolab.com](http://mongolab.com) and browse the database:
![Tasks on MongoLab](readme_images/tasksonline.png)

> If you are having trouble with your MongoLab URI, you can try to connect via the `mongo` shell in the Cloud9 terminal with the command:
>
> `mongo <host>:<port>/<db> -u <dbuser> -p <dbpassword>`
>
> You get all of the variables from the URI which is:
>
> `mongodb://<dbuser>:<dbpassword>@<host>:<port>/<db>`

####Bootstrap
I openly admit that I am not a designer.  However, end users are not always understanding of my lack of design skills.  So when I need to create a user interface, I turn to Twitter Bootstrap.  Bootstrap is a library of CSS components that makes it easy (or at least easier) for non-designers like myself to quickly create a pleasing (or plausible) user interface.  The first step is to add the CSS file for Bootstrap to our template.  I like to get commonly used resources such as Bootstrap, jQuery, underscore and AngularJS from [cdnjs.com](http://cdnjs.com).  So if we go to their site, and search for __bootstrap__, we'll see the first result is for _twitter-bootstrap_.

![Twitter Bootstrap on cdnjs](readme_images/cdnjstbs.png)

Click on that link and then find the link for _bootstrap.min.css_.  This is the minfied CSS that will take less time to load.  Click the _Copy_ button to copy the link to the clipboard.

![Select bootstrap.min.css](readme_images/bsmincss.png)

Now switch over to `index.html`.  Add a `<head>` tag and a `<link>` tag inside of that.

> Inside an HTML file with the Cloud9 editor, you can type 'head' and then press the TAB key to have it generate the opening and closing tag.  You can do the same with 'link' and it will also fill in some of the most used attributes as well.

In the 'href' attribute paste the link from cdnjs.com for Bootstrap.  We will also need some custom styles to highlight high priority and overdue tasks.  So add another `<link>` tag.  This time the 'href' attribute will be the path to a custom CSS file.  In Flask, static assets like styles and scripts are stored in a directory in the root of the application called `static` so go ahead and create that now and then a file inside called `styles.css`.  We'll leave it empty for now.  To get the URL for a static file we'll use a special function called `url_for` which is provided by Flask.  This function specifies 'static' as the directory to find the 'filename' `styles.css` in.  Since the function call is in double curly braces, the return value (the URL of the filename) will be rendered as text.  The `<head>` tag should now look like this:

```html
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.4/css/bootstrap.min.css" type="text/css" />
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}" type="text/css" />
</head>
```

Now refresh the site.  It already looks better!

![Bootstrap 1](readme_images/bootstrap1.png)

Next we'll use the grid layout that Bootstrap gives us to make the form look better.  All grids are placed in a `<div>` tag with a class of `container`.  For this simple page, I'll wrap everything in the `<body>`.

```html
<body>
    <div class="container">
        ...
    </div>
</body>
```

> To quickly create the `<div>` tag with a `container` class, simply type `div.container` and then press the TAB key in the Cloud9 editor.

Grids have rows and columns.  With Bootstrap, each row is a `<div>` tag with a class of `row`.  Place each label and text box in the form in a `<div>`.  Be sure to remove the `<br>` tag.

```html
<div class="container">
    ...
    <div class="row">
        Task: <input type="text" name="task">
    </div>
    ...
</div>
```

The label and text box should each be in a column.  The class for a column that we are using is 'col-md-2'.  The 'col' is for 'column', the 'md' is for 'medium', and the '2' is for width of 2 units.  All rows in Bootstrap have a width of 12 'units.  The length of a unit is relative to the width of the page because Bootstrap is responsive.  The 'md' has some effect on this as well.  (We eon't get into responsive design here.  Recall I am not a designer.)  The template should start looking like this:

```html
<div class="container">
    ...
    <div class="row">
        <div class="col-md-2">Task:</div>
        <div class="col-md-2"><input type="text" name="task"></div>
    </div>
    ...
    <div class="row">
        <div class="col-md-4"><input type="submit" value="Create Task"></div>
    </div>
</div>
```

Save the template and refresh the site again.  That is much better!

![Form styled](readme_images/formstyle.png)

Next we need to work on the list of tasks.  But there are some loose ends we need to tie up in the data model first.


####Refining our model class
We need to update the model class (`TodoItem`) so that it stores actual dates.  We also need to add some methods to determine the number of days until a task is due and if a task is overdue.

MongoEngine has a `DateTimeField` type that we can use for the due date.  So remove the `duedays` field in `TodoItem` and replace it with:


```python
due_date = DateTimeField()
```

> Don't forget to import `DateTimeField` from `mongoengine`.

Now in the entry point, just before creating the new `TodoItem`, add the following line:


```python
due_date = datetime.datetime.now() + datetime.timedelta(days=duedays)
```

This code uses the `datetime` module (so it needs to be imported) to get the current date and time.  Then it creates a `timedelta` which can be added to a datetime.  When we create the `timedelta` we specify its length in days.  So if `duedays` were 7, then `due_date` would be one week in the future.

Back in `TodoItem`, let's add a couple of methods.  Remember this is still just a Python class.  The first one will be called `is_overdue`.  We'll simply compare the `due_date` of the `TodoItem` with the current `datetime`.  If `due_date` is less, the task is overdue, otherwise it is not.

```python
def is_overdue(self):
    return self.due_date.date() < datetime.datetime.now().date() #>
```

Note that we are using the `date()` method to compare just the day as opposed to a specific hour and minute.

The other method is called `days_till_due` and will just return the number of days left until the task is due.  

```python
def days_till_due(self):
    delta = self.due_date.date() - datetime.datetime.now().date()
    return delta.days
```

Here we are subtracting the dates of two `datetime` objects and the difference between them is a `timedelta`.  The `timedelta` has a `days` property which is what we want to return.

One last method that we need to create is a method to determine what CSS style is represented by different `TodoItem` states such as high priority or overdue.  (We'll create the styles soon.)

```python
def compute_style(self):
    the_class = ''
    if self.priority > 5:
        the_class += ' hi-priority'
    if self.days_till_due() == 0:
        the_class += ' due-today'
    if self.is_overdue():
        the_class = ' overdue'

    return the_class
```

This function just looks at the state of the `TodoItem` and returns a string representing the class to reflect the state.  There is no style for completed tasks as they will not be shown in the list.

####Styles
Here is the `styles.css` file.  It's short and should be self explanatory.

```css
.hi-priority {
    color: blue;
}

.overdue {
    color: red;
    font-weight: bold;
}

.due-today {
    font-weight: bold;
}

.spacer {
    margin-bottom: 5px;
}
```

####Styling the todo list
Let's make the list of `TodoItem` more readable.  First we'll add a header to say what each column is.  Put this right after the `<h3>` tag at the top of the page:

```html
<div class="row">
    <div class="col-md-2">Task</div>
    <div class="col-md-2">Due Date</div>
    <div class="col-md-2">Priority</div>
</div>
```

Now for the list.  Remove the `<ul>` and the line with the `<li>` tag.  Inside the for loop add an if statement to make sure the `TodoItem` is not complete.  If it is not complete, we will display it:

```html
{% for item in todos %}
    {% if not item.complete %}
        ...
    {% endif %}
{% endfor %}
```

Next add a row for each `TodoItem` with a column for the `task`, `due_date` and `priority`:

```html
<div class="row spacer">
    <div class="col-md-2">{{ item.task }}</div>
    <div class="col-md-2">{{ item.due_date }}</div>
    <div class="col-md-2">{{ item.priority }}</div>
</div>
```

We need to add a call to the `strftime()` method on the `due_date`.  This will format the date in a readable string.  The format I will use is 'month/day/year': (For a great reference on the `strftime()` format string, check out [this page](http://strftime.org).

```html
<div class="col-md-2">{{ item.due_date.strftime('%m/%d/%Y') }}</div>
```

Finally, let's add a call to the `compute_style` method of `TodoItem` that will get the style to reflect the item's state:

```html
<div class="row spacer{{ item.compute_style() }}">
    ...
</div>
```

One last thing.  We changed the data model and the easiest way to deal with this is to just drop the database.  This is not how you would handle a production application but in this case it will suffice.  Open the `mongo` shell in a terminal and run:

```
use mempydemo
db.dropDatabase()
```

Now you can refresh the site.  It has no items so let's a add few:

 * Task: Very important, Days until due: 7, Priority: 10
 * Task: Overdue, Days until due: -1, Priority: 2
 * Task: Due today, Days until due: 0, Priority: 5
 * Task: Nothing special, Days until due: 14, Priority : 5

> In a production application, you might add validation to prevent a due date for a new task from being in the past (as in the second task).  However, for our purposes it is a convenient way to create overdue tasks. :)

Take a look at our list now:

![List with states](readme_images/statelist.png)

This is getting somewhere!  We have a few more things to do to finish up.  First we need to be able to mark tasks as complete.  Second, we'd like to sort tasks by priority or due date.  Finally, we would like to be able to view which tasks have been completed.  This requires a little more Bootstrap but is most about querying MongoDB.  We'll cover that in the next sections.








