#!/usr/bin/perl

use lib "/home/vault/lib";
use strict;
use CGI::Carp qw (fatalsToBrowser);
use Vault;

my $webapp = Vault->new(
    tmpl_path => "/home/vault/tmpl/plain"
    );

$webapp->run();
