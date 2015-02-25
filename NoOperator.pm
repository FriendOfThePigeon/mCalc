#!/usr/bin/perl
package NoOperator;
use strict;

use Operator;

our @ISA = qw( Operator );

sub apply {
	# Do nothing!
}

1;
