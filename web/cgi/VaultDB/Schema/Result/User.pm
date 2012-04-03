package VaultDB::Schema::Result::User;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

use strict;
use warnings;

use base 'DBIx::Class::Core';

__PACKAGE__->load_components("InflateColumn::DateTime");

=head1 NAME

VaultDB::Schema::Result::User

=cut

__PACKAGE__->table("user");

=head1 ACCESSORS

=head2 userid

  data_type: 'integer'
  is_auto_increment: 1
  is_nullable: 0

=head2 username

  data_type: 'varchar'
  is_nullable: 1
  size: 512

=head2 salt

  data_type: 'char'
  is_nullable: 1
  size: 22

=head2 cost

  data_type: 'integer'
  default_value: 14
  is_nullable: 1

=head2 hash

  data_type: 'char'
  is_nullable: 1
  size: 31

=head2 email_address

  data_type: 'varchar'
  is_nullable: 1
  size: 512

=head2 timeout

  data_type: 'integer'
  default_value: 900
  is_nullable: 1

=head2 validation_string

  data_type: 'char'
  is_nullable: 1
  size: 32

=cut

__PACKAGE__->add_columns(
  "userid",
  { data_type => "integer", is_auto_increment => 1, is_nullable => 0 },
  "username",
  { data_type => "varchar", is_nullable => 1, size => 512 },
  "salt",
  { data_type => "char", is_nullable => 1, size => 22 },
  "cost",
  { data_type => "integer", default_value => 14, is_nullable => 1 },
  "hash",
  { data_type => "char", is_nullable => 1, size => 31 },
  "email_address",
  { data_type => "varchar", is_nullable => 1, size => 512 },
  "timeout",
  { data_type => "integer", default_value => 900, is_nullable => 1 },
  "validation_string",
  { data_type => "char", is_nullable => 1, size => 32 },
);
__PACKAGE__->set_primary_key("userid");
__PACKAGE__->add_unique_constraint("username", ["username"]);


# Created by DBIx::Class::Schema::Loader v0.07000 @ 2012-04-03 20:37:24
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:dNt2d8MeM7IcRrXK01ojaw


# You can replace this text with custom content, and it will be preserved on regeneration
1;
