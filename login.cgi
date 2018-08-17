#!/usr/bin/perl -T

use strict;
use warnings;
use DBI;
use CGI qw/:standard/;
use CGI::Carp qw/fatalsToBrowser/;

# This variable counts the number of records that matched the 
# username that the user entered on the form.
# If it remains 0, it means the username was not found.
my $no_of_rows = 0;

# This variable contains the ID of the user that is currently logged in
my $user_id;

# Obtain a database handle
my $dbh = connectToMySql();

print header;

# First we need to check where we are in the process

# Check if the user is already signed in and filled in the extra info form
if (param('submit') && param('age')){
    # obtain the data from the form
    my $age = param('age');
    my $gender = param('gender');
    my $address = param('address');
    $user_id = param('user_id');

    # TO DO: untaint the data

    # obtain the current time and format it to the SQL datetime format
    my $date_time = do {
        my ($s, $m, $h, $D, $M, $Y) = localtime;
        $Y+=1900;
        $M++;
        "$Y-$M-$D $h:$m:$s"};
    
    # set the value of the insert query
    my $query = "INSERT INTO participants 
                    (age, gender, address, date_time, user_id)
                    values (?, ?, ?, ?, ?)";

    # prepare the statement for connecting to the database
    my $statement = $dbh -> prepare($query);

    # execute the SQL query
    $statement -> execute($age, $gender, $address, $date_time, $user_id)
        or die "Cannot execute statement: $DBI::errstr";    
    
    print start_html('Submitted'),
        h1("Success!"),
        p("Your information has been submitted.");

} elsif (param('submit') && !param('age')){

    # in this case the user has pressed the 'Submit' button but did not fill in the age.
    # tell him about that and give him the chance to fill it in.

    print start_html('More Info'),
            h1("Hi ".param('username')."!"), p, hr,
            p("Please fill in the following form."),
            start_form,
            p("Age *"), textfield('age'),
            p("Gender"), textfield('gender'),
            p("Address"), textfield('address'), p,
            submit(-value => 'SUBMIT', -name => 'submit'),
            p({-style=>'Color: red;'},"The fields marked with (*) are mandatory."),
            end_form;
}

# check whether the user has filled in the username and password
elsif (param('username') && param('password')){

    # in this case, we fetch data from the 'users' table and check
    # if the username exists and if the password is correct
    my $username = param('username');
    my $password = param('password');
    
    my $credentials_ok = check_credentials($username, $password);

    # if the username was not found in the table, inform the user about it
    # and give him the opportunity to enter it again.    
    if ($no_of_rows == 0){
        print start_html('Login'),
        h1("Login"),
        start_form,
        p("Username"),
        textfield('username'),
        p({-style=>'Color: red;'},"The username was not recognized."),
        p("Password"),
        password_field('password'), p,
        submit(-value => 'LOGIN', -name => 'login'),
        end_form;

    } elsif ($credentials_ok) {
        # in this case the username was found in the table 
        # and the password was correct
        print start_html('More Info'),
            h1("Hi ".param('username')."!"), p, hr,
            p("Please fill in the following form."),
            start_form,
            # we have a hidden form variable that contains 
            # the 'username' parameter from the previous step
            hidden(-name=>'username', -value=>param('username')),
            # and another hidden variable that contains the user_id
            hidden(-name=>'user_id', -value=>$user_id),
            p("Age *"), textfield('age'),
            p("Gender"), textfield('gender'),
            p("Address"), textfield('address'), p,
            submit(-value => 'SUBMIT', -name => 'submit'),
            end_form;

    } else {
        # in this case the username was found in the table 
        # but the password was incorrect
        print start_html('Login'),
        h1("Login"),
        start_form,
        p("Username"),
        textfield('username'),
        p("Password"),
        password_field('password'), p,
        p({-style=>'Color: red;'},"Incorrect password."),
        submit(-value => 'LOGIN', -name => 'login'),
        end_form;
    }
        
} elsif(param('login') && (!param('username') || !param('password'))){ 

    # if the user has pressed the 'Login' button but left one of the fields blank, 
    # display a message to say that he has to fill in all the textfields
    # and give him that chance.

    print start_html('Login'),
        h1("Login"),
        start_form,
        p("Username"),
        textfield('username'),
        p("Password"),
        password_field('password'), p,
        p({-style=>'Color: red;'},"All fields are required to login."),
        submit(-value => 'LOGIN', -name => 'login'),
        end_form;

} else {

    # in this case, the user is attempting to login for the first time
    print start_html('Login'),
        h1("Login"),
        start_form,
        p("Username"),
        textfield('username'),
        p("Password"),
        password_field('password'), p,
        submit(-value => 'LOGIN', -name => 'login'),
        end_form;
}

print end_html;

$dbh -> disconnect();

exit;

#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------

# This subroutine is used to:
# - select the row from the 'users' table that matches the username entered by the user
# - return 1 if the username and password match or 0 if they don't

sub check_credentials{
    # retrieve the parameters that were passed to the subroutine
    my ($user, $passw) = @_;

    # select only the record that matches the username entered by the user
    my $sth = $dbh->prepare("SELECT user_id, password 
        FROM users.users WHERE username = '$user'");    
    $sth->execute()
        or die "Couldn't execute sth: $DBI::errstr";

    # This variable will have the value 1 if the username and password match
    # or 0 if they don't.
    my $credentials_ok = 0;
    
    # This is the information obtained from the 'users' table.
    my $correct_password;
    ($user_id, $correct_password) = $sth->fetchrow_array();
    
    # If the user_id is defined, it means that there was one row in the table that
    # matched the username.
    if (defined $user_id){
        $no_of_rows = 1;
    }   
    
    if ($no_of_rows != 0){
        # if the username was found, check the password
        if ($passw eq $correct_password){
            $credentials_ok = 1;            
        } else {
            $credentials_ok = 0;
        }
    }   
    return $credentials_ok;
}

