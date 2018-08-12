# Frontend

### Adding javascript dependencies

To add javascript dependencies that are specific to your project, you can simply:

    $ yarn add --dev some-package
    
If you want to add a package that will be required as runtime (a.k.a your webserver needs to serve it to your
visitors), don't mark it as dev:

    $ yarn add jquery
