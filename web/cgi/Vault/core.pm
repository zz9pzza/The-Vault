package Vault::core;

use VaultDB::Schema;
use DBI;
use YAML qw(LoadFile);
use MIME::Lite;
use Template;
use Template::Config;
use Carp;
use Readonly;
use Error qw(:try);
use Data::Dumper ;

Readonly our $LOG_FATAL      => '1000';
Readonly our $LOG_APP_INFORM => '0800';
Readonly our $LOG_LIB_INFORM => '0700';
Readonly our $LOG_LIB_ERROR  => '0300';
Readonly our $LOG_SQL        => '0100';
Readonly our $LOG_DEFAULT    => '0000';

sub new {
    my ( $class, %args ) = @_;

    my $settings_file =
      exists $args{settings_file} ? $args{settings_file} : '/etc/vault';

    my $self = {};
    if ( !-f $settings_file ) {
	croak "Can't read $settings_file";
    }

    $self->{'settings'}    = LoadFile($settings_file);
    $self->{'config_file'} = $settings_file;
    my $dsn='DBI:mysql:vault:' . $self->{'settings'}->{'host'} . ':' . $self->{'settings'}->{'port'} ;
    $self->{'schema'}      = VaultDB::Schema->connect(
 	$dsn,
	$self->{'settings'}->{database},
	$self->{'settings'}->{password}
    );
	
    $self->{'dbi'}=DBI->connect ($dsn,$self->{'settings'}->{database},$self->{'settings'}->{password}) ;

    bless $self, $class;
    return $self;
}

sub dbi {
    my ($self)=@_;

    return $self->{'dbi'};
}

sub get_default_value {
    my ( $self, $request, $result ) = @_;

    my $new_result = $self->{'settings'}->{$request};
    if ( defined $new_result ) {
	return $new_result;
    }
    if ( $result eq "NONE" ) {
	return '';
    }
    if ( defined($result) ) {
	return $result;
    }
    croak "Config option ($request) not set in config file ("
      . $self->{'config_file'} . ')';
}

sub send_validation_email {
    my ( $self, $email, $email_validation, $username ) = @_;

    my $tt = Template->new(
	EVAL_PERL    => 1,
	INCLUDE_PATH => $self->get_default_value('email_template_dir')
    );
    my $data = "";
    my $vars = {
	url      => $self->get_default_value('cgi_path') . 'confirm_email',
	username => $username,
	email_validation => $email_validation
    };

    if ( !$tt->process( 'email_registration.html', $vars, \$data ) ) {
	$data = '<p>There has been an error: ' . $tt->error() . '<p>';
    }

    my $msg = MIME::Lite->new(
	Subject =>
	  $self->get_default_value( 'register_subject', 'Vault registration' ),
	From => $self->get_default_value('register_from'),
	To   => $email,
	Cc   => $self->get_default_value( 'register_cc', 'NONE' ),
	Type => 'multipart/related',
    );

    $msg->attach(
	Type => 'text/html',
	Data => $data
    );

    $msg->attach(
	Type => 'image/png',
	Id   => 'logo.png',
	Path => $self->get_default_value('email_template_image')
    );

    return $msg->send();

}

sub log_event {
    my ( $self, $text, $priority, $userid ) = @_;

    try {
	my $new_event = $self->{schema}->resultset('Event')->create(
	    {
		userid   => $userid,
		text     => $text,
		stamp    => time,
		priority => $priority
	    }
	);
    }
}

1;

