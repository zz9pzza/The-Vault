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
my ($param, $template,$cookie,$session,$vault,$menu,$time_to_expire);
 
#--------------------------------------------------
# application
#--------------------------------------------------
my  $script_add= '';
my  $html_add= '';
$menu=1;
$vault = Vault::core->new();
# Set the default action to be the login page.
my $action='display_login_page';
if ( defined $cgi->param('action') ) {
	$action=$cgi->param('action') ;
}
 
if ( $action eq 'display_login_page' ) {
    $template = 'login.html';
    $menu=0;
} else {
   $cookie=$cgi->cookie("VAULTID") || undef;
   $session = new CGI::Session("driver:MySQL", $cookie, {Handle=>$vault->dbi()});
   $time_to_expire=$session->atime()+$session->expire()-time;
   # Display an error if we do not have a valid session
   if ( !defined ( $session->param("username") ) ) {
	$vault->log_event("Attempt to access $action with no session( $cookie )",$Vault::core::LOG_APP_INFORM);
	print 'Location: '.$vault->get_default_value('cgi_path')."/index.cgi\n\n" ;
	exit 0 ;
   }

}
if ( $action eq 'front_page' ) {
	$template = 'file_view.html';
}


my $vars = {
    rootdir => $ROOTDIR,
    rooturl => $ROOTURL,
    rootcgi => $ROOTCGI,
    script_add => $script_add,
    html_add => $html_add,
    footer_text => $vault->get_default_value('footer_text','NONE'),
    menu => $menu,
    time_to_expire => $time_to_expire,
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
