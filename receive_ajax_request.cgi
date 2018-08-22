#!/usr/bin/perl

use strict;
use warnings;
use CGI;

my $cgi = CGI->new();

# read the CGI params
my $id = $cgi->param("id");
my $age = $cgi->param("age");

my $message = "ID: $id, age:$age";

print $cgi->header('text/plain;charset=UTF-8');
print $message;


