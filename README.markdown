Automated tools for engaging with server infrastructure on AWS.

To install use:

    pip install git+git://github.com/Proteus-tech/profab.git


# Configuring profab #

You will need to give profab EC2 API keys for each client in order for it to be able to manage EC2 infrastructure. I.e. for a client you wish to refer to as 'acme-widgets' use:

    mkdir -p ~/.profab/acme-widgets
    $EDITOR ~/.profab/acme-widgets/ec2.json

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

For all commands `client-name` is the same as the configuration folder used above, (acme-widgets)..

Command line arguments are given as names after the script. For roles they come in two types: either with or without a parameter. This is either as `role` or `--role parameter`. Roles are processed in the order specified.

## pf-server-start ##

    pf-server-start client-name _roles_

Starts a new server. Roles that control the region, size or AMI are only effective when an instance is started. Instances cannot be moved between regions, cannot be re-sized and the AMI cannot be changed once launched.

If multiple roles set an AMI, instance size or region then the last one that does so controls which is actually used.

## pf-server-list ##

    pf-server-list client-name

## pf-server-role-add ##

    pf-server-role-add client-name hostname _roles_

## pf-server-update ##

    pf-server-update client-name hostname

## pf-server-terminate ##

    pf-server-terminate client-name hostname

# Roles #

## ami ##

    --ami ami-code

Allows the AMI that is to be launched to be controlled. The AMI must be available in the region requested.

    ami.lucid

Will choose an Ubuntu Lucid (10.04) AMI. This is the default AMI if no other one is chosen.

Instances are chosen from http://uec-images.ubuntu.com/releases/10.04/release/

## bits ##

    bits

Automatically determines the number of bits that are to be used for a new server. This role is added automatically by profab, so there is no need to add it explicitly.

    --bits 32|64

Set the number of bits. profab will determine the correct number of bits for all current instance sizes automatically. You will need to use `--bits 64` to run a micro instance using a 64 bit operating system as profab will default to 32 bits.

## eip ##

    --eip ip-number

Binds the Elastic IP number to the instance. Adding this to a running server along with other configuration may cause connection problems.

## munin ##

    munin

Configures the machine as a Munin server. Installs Apache 2 as the web server and the default web site is set to be Munin.

    --munin server

Configures the machine to be monitored by Munin at the specified server. Only basic monitoring is configured.

## postgres ##

    postgres

Installs the Postgres packages on the machine. It also sets up Postgres users (roles and default databases) for the `ubuntu` and `www-data` users so they can both access the database using ident authentication.

## region ##

    --region region-name

Allows the region that the instance is to be run in to be chosen. The default region is us-east-1 (Virginia).

## security_group ##

    --security_group group-name

Adds a new security group to the instance as it is launched. If no security groups are set then the server will get the default security group.

This can be specified more than once in order to add more than one security group. It has no effect when used on a server instance that has already been started.

## size ##

    --size size-code

Sets the instance size to be launched to the requested size. Current valid sizes can be found at http://aws.amazon.com/ec2/instance-types/

Unlike the normal EC2 default, profab has a default size of `t1.micro`.

## smarthost ##

    smarthost

Installs and configures exim to relay email for the machine. Emails are sent to recipients directly from the machine. The machine will only relay for mail sent from the local host.


# Doing development #

_This project uses git flow. Don't forget to do `git flow init`_ (use defaults for all options).

You should run the devenv/paths script in order to set up your command line environment to be able to use profab straight from the check out.

    . devenv/paths

To run the tests, create and activate a new virtual environment and then use the `runtests` script.

    mkvirtualenv --no-site-packages profabdev
    pip install -r devenv/setup.pip
    ./runtests

## Customising roles ##

A role is a Python module that contains a definition for either `AddRole` or `Configure` depending on whether there is a parameter or not. These should inherit from `profab.role.Role` and may include any of the following members:

    packages

The packages that are to be installed as part of this role.

    region(self)

Returns the region that should be used for starting an instance.

    ami(self, region)

Returns the AMI for the region that is to be used.

    started(self, server)

Can do configuration of the machine within EC2 after the reservation has been made and the instance started, but before it is first connected to.

    configure(self, server)

Can do any configuration that is required in order to get the role working.

