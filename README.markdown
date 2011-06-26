Automated tools for engaging with server infrastructure on AWS.

To install use:

    pip install git+git://github.com/Proteus-tech/profab.git


# Configuring profab #

You will need to give profab EC2 API keys for each client in order for it to be able to manage EC2 infrastructure. I.e. for a client you wish to refer to as 'acme-widgets' use:

    mkdir -p ~/.profab/acme-widgets
    $EDITOR ~/.profab/adme-widgets/ec2.json

In the configuration file you will need a minimum of:

    {
        "host": "ec2",
        "keys": {
            "api":"paste API key here",
            "secret": "paste API secret here"
        }
    }

The first time you connect to an EC2 region to start a machine a new private/public key pair will be created with the private key being stored in the client folder.


# Command line scripts #

## pf-server-start ##

    pf-server-start client-name

## pf-server-update ##

    pf-server-update client-name hostname

## pf-server-terminate ##

    pf-server-terminate client-name hostname


# Doing development #

_This project uses git flow. Don't forget to do `git flow init`_ (use defaults for all options).

You should run the devenv/paths script in order to set up your command line environment to be able to use profab straight from the check out.

    . devenv/paths

