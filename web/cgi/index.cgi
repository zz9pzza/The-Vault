#!/usr/bin/perl
 
use strict;
use warnings;
 
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session qw/-ip-match/;
use Vault::core;
use Template;
$| = 1;
 
#--------------------------------------------------
# configuration
#--------------------------------------------------
 
my $ROOTDIR = '/home/vault';
my $ROOTURL = 'https://stage.transformativeworks.org/';
my $ROOTCGI = '/vault_cgi/index.cgi';
 
my $cgi = CGI->new(  );
my ($param, $template,$cookie,$session,$vault);
 
#--------------------------------------------------
# application
#--------------------------------------------------
my  $script_add= '';
my  $html_add= '';
my $registered_state='' ;
if ( defined $cgi->param('registered_state' ) ) {
	$registered_state=$cgi->param('registered_state' )  ;
}
# Set the default action to be the login page.
my $action='display_login_page';
if ( defined $cgi->param('action') ) {
	$action=$cgi->param('action') ;
}
 
if ( $action eq 'display_login_page' ) {
    $template = 'login.html';
} else {
   $vault = Vault::core->new();
   $cookie=$cgi->cookie("VAULTID") || undef;
   $session = new CGI::Session("driver:MySQL", $cookie, {Handle=>$vault->dbi()});
   # Display an error if we do not have a valid session
   if ( !defined ( $session->param("username") ) ) {
	$vault->log_event("Attempt to access $action with no session( $cookie )",$Vault::core::LOG_APP_INFORM);
	print 'Location: '.$vault->get_default_value('cgi_path')."/index.cgi\n\n" ;
	exit 0 ;
   }

}
if ( $action eq 'front_page' ) {
	$template = 'front_page.html';
}


my $vars = {
    rootdir => $ROOTDIR,
    rooturl => $ROOTURL,
    rootcgi => $ROOTCGI,
    script_add => $script_add,
    html_add => $html_add,
};

 
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
