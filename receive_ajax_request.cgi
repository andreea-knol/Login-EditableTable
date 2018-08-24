#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use DBI;

my $cgi = CGI->new();

print $cgi->header();

# These variables contain the values received from the AJAX call
my $id = $cgi->param('data_id'); 
my $age = $cgi->param('data_age');

update_table();

#-------------------------------------------------

# This function updates the table using the values the user changed in 
# the browser
sub update_table{
    # Obtain a database handle
    my $dbh = connectToMySql();
    # set the value of the select query
    my $query = "UPDATE participants SET age = $age WHERE participant_id = $id";
    # prepare the statement for connecting to the database
    my $statement = $dbh -> prepare($query);
    # execute the query
    $statement -> execute()
        or die "Couldn't execute statement: $DBI::errstr";
    $dbh -> disconnect();
}


# This subroutine is used to connect to the database.
# It returns a database handle

sub connectToMySql{
    my $dsn = "dbi:mysql:users:localhost";
    my $username = "root";
    my $password = "157000";
    my $dbh = DBI->connect($dsn, $username, $password)
        or die "Couldn't connect to database: $DBI::errstr";
    return $dbh;
}
