#!/usr/bin/perl
 
use strict;
use warnings;
 
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use Template;
$| = 1;
 
#--------------------------------------------------
# configuration
#--------------------------------------------------
 
my $ROOTDIR = '/home/vault';
my $ROOTURL = 'https://stage.transformativeworks.org/';
my $ROOTCGI = '/vault_cgi/index2.cgi';
 
my $cgi = CGI->new(  );
 
my ($param, $template);
my $vars = { 
    rootdir => $ROOTDIR,
    rooturl => $ROOTURL,
    rootcgi => $ROOTCGI,
};
 
#--------------------------------------------------
# application
#--------------------------------------------------
 
if ($param = $cgi->param('name')) {
    $vars->{ entry } = "test";
    $template = 'entry.html';
}
else {
    $template = 'login.html';
}
 
#------------------------------------------------------------------------
# presentation
#------------------------------------------------------------------------
 
my $tt  = Template->new({
    INCLUDE_PATH => [
        "$ROOTDIR/templates/cgi",
        "$ROOTDIR/templates/lib",
    ],
    PRE_PROCESS => 'config',
    WRAPPER     => 'wrapper',
});
 
print $cgi->header(  );
 
$tt->process($template, $vars)
    || die $tt->error(  );
