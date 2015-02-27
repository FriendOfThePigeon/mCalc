#!/usr/bin/perl
package PowerOperator;
use strict;

use BinaryOperator;

our @ISA = qw( BinaryOperator );

sub get_symbol {
	return '^';
}

sub binary_apply {
	my ($self, $value1, $value2) = @_;
	return ($value2 ** $value1);
}

1;
