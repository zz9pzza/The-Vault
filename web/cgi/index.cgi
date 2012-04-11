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
my  $script_add= '';
my  $html_add= '';
my $registered_state='' ;
if ( defined $cgi->param('registered_state' ) ) {
	$registered_state=$cgi->param('registered_state' )  ;
}
 
if ($param = $cgi->param('name')) {
    $vars->{ entry } = "test";
    $template = 'entry.html';
}
else {
    $template = 'login.html';
    if ( $registered_state eq 'notregisted' ) {
    	$script_add= '';
    	$html_add= '';
	} 
    if ( $registered_state eq 'registed' ) {
        $script_add= '';
        $html_add= '';
        }
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
