#!/usr/bin/perl 

use warnings;
use strict;
use CGI;
use DBI;

# Obtain a database handle
my $dbh = connectToMySql();

my $cgi = CGI->new();
main();

#-----------------------------------------------------------------

# This is the main function which does most of the work.
sub main{

# set the value of the select query
my $query = "SELECT * FROM participants";

# prepare the statement for connecting to the database
my $statement = $dbh -> prepare($query);

# execute the query
$statement -> execute()
    or die "Couldn't execute statement: $DBI::errstr";

# this is the variable that contains all the html code
my $html = <<HTML;
<html>
    <head>
        <title>View Participants</title>
        <link rel="stylesheet" href="/style1.css">
        <script type="text/javascript" src="http://code.jquery.com/jquery-1.4.4.min.js"></script>
        <script type="text/javascript" src="/script.js"></script>
    </head>
    <body>
        <h1>Participants table</h1>
        <table>
            <tr>
                <th>Participant ID</th>
                <th>Age</th>
                <th>Gender</th>
                <th>Address</th>
                <th>Date&Time</th>
                <th>User ID</th>
            </tr>
HTML

print "Content-type: text/html\n\n";
print $html;
    
# iterate through the results and dynamically create the table rows
while (my ($partID, $age, $gender, $address, $dateTime, $userID) = 
            $statement->fetchrow_array()) {
             
                print "<tr>
                        <td>$partID</td>
                        <td><input type='text' id='$partID' name='age' value=$age onChange='changeAge($partID)'/></td>
                        <td>$gender</td>
                        <td>$address</td>
                        <td>$dateTime</td>
                        <td>$userID</td></tr>";
}
print "</table>\n";

print "<p id='demo'></p>";

print "</body></html>";


$dbh->disconnect();

exit;
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
